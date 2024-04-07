import inspect
import sqlite3
import typing
from bookkeeper.repository import abstract_repository
from bookkeeper.models import category


class SQLiteRepository(
        abstract_repository.AbstractRepository[abstract_repository.T]):

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.data_type = cls
        self.table_name = self.data_type.__name__.lower()
        self.fields = inspect.get_annotations(self.data_type, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: abstract_repository.T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({p})', values)
            con.commit()
            obj.pk = cursor.lastrowid
            cursor.close()
        return obj.pk

    def add_empty(self) -> int:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f"INSERT INTO {self.table_name} DEFAULT VALUES")
            con.commit()
            cursor.close()
        return cursor.lastrowid

    def update(self, obj: abstract_repository.T) -> None:
        names = ' = ?, '.join(self.fields.keys()) + ' = ?'
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(
                f'UPDATE {self.table_name} SET {names} WHERE ROWID = {obj.pk}',
                values)
            con.commit()
            cursor.close()

    def update_item(self, row: int, col: str, value: typing.Any) -> None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(
                f'UPDATE {self.table_name} SET {col} = ? WHERE rowid = ?',
                (value, row))
            con.commit()
            cursor.close()

    def get(self, pk: int) -> abstract_repository.T | None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name} LIMIT 1 OFFSET ?',
                           (pk - 1, ))
            res = self.data_type(*cursor.fetchone())
            res.pk = pk
            cursor.close()
        return res

    def get_all(
        self,
        where: dict[str, typing.Any] | None = None
    ) -> list[abstract_repository.T]:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            if where == None:
                cursor.execute(f'SELECT rowid,  * FROM {self.table_name}')
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            elif next(iter(where.values())) == None:
                cursor.execute(
                    f'SELECT rowid, * FROM {self.table_name} WHERE {next(iter(where.keys()))} IS NULL'
                )
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            else:
                cursor.execute(
                    f'SELECT rowid, * FROM {self.table_name} WHERE {next(iter(where.keys()))} = ?',
                    (next(iter(where.values())), ))
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            cursor.close()
        return res

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            #deleting category we need delete all subcatogories
            if self.data_type == category.Category:
                values = tuple([pk] + [
                    cate.pk for cate in category.Category(
                        'name', pk=pk).get_subcategories(self)
                ])
                condition = 'ROWID IN (' + ', '.join("?" * len(values)) + ')'
                cursor.execute(
                    f"DELETE FROM {self.table_name} WHERE {condition}", values)
                con.commit()
                #update rowid
                counts = {}
                cursor.execute(f"SELECT rowid FROM {self.table_name}")
                rowids = cursor.fetchall()
                for row in rowids:
                    count = sum(1 for value in values if value < row[0])
                    counts[row[0]] = count
                for rowid in counts:
                    cursor.execute(
                        f'UPDATE {self.table_name} set ROWID = ROWID - ? WHERE ROWID = ?',
                        (counts[rowid], rowid))
                    con.commit()
            else:
                cursor.execute(
                    f'DELETE FROM {self.table_name} WHERE ROWID = ?', (pk, ))
                con.commit()
                #update rowid
                cursor.execute(
                    f'UPDATE {self.table_name} set ROWID = ROWID - 1 WHERE ROWID > ?',
                    (pk, ))
                con.commit()
            cursor.close()

    def del_all(self) -> None:
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM {self.table_name}")
            con.commit()
            cursor.close()
