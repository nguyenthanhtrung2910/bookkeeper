from inspect import get_annotations
import sqlite3
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls:type) -> None:
        self.db_file = db_file
        self.data_type = cls
        self.table_name = self.data_type.__name__.lower()
        self.fields = get_annotations(self.data_type, eval_str=True)
        self.fields.pop('pk')
        
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f'INSERT INTO {self.table_name} ({names}) VALUES({p})', values)
            con.commit()
            obj.pk = cursor.lastrowid
            cursor.close()
        return obj.pk
    
    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name} LIMIT 1 OFFSET ?', (pk - 1,))
            res = self.data_type(*cursor.fetchone())
            res.pk = pk 
            cursor.close()
        return res
    
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            if where == None:
                cursor.execute(f'SELECT rowid,  * FROM {self.table_name}')
                res = [self.data_type(*(list(data[1:])+[data[0]])) for data in cursor.fetchall()] 
            elif next(iter(where.values())) == None: 
                cursor.execute(f'SELECT rowid, * FROM {self.table_name} WHERE {next(iter(where.keys()))} IS NULL')
                res = [self.data_type(*(list(data[1:])+[data[0]])) for data in cursor.fetchall()] 
            else:
                cursor.execute(f'SELECT rowid, * FROM {self.table_name} WHERE {next(iter(where.keys()))} = ?',
                               (next(iter(where.values())), ))
                res = [self.data_type(*(list(data[1:])+[data[0]])) for data in cursor.fetchall()] 
            cursor.close()        
        return res


    def update(self, obj: T) -> None:
        names = ' = ?, '.join(self.fields.keys()) + ' = ?'
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f'UPDATE {self.table_name} SET {names} WHERE ROWID = {obj.pk}', values)
            con.commit()
            cursor.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f'DELETE FROM {self.table_name} WHERE ROWID = ?', (pk,))
            con.commit()
            cursor.close()

    def del_all(self) -> None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM {self.table_name}")
            con.commit()
            cursor.close()