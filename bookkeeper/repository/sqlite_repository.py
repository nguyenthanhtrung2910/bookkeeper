import inspect
import sqlite3
import typing
from bookkeeper.repository import abstract_repository
from bookkeeper.models import category
from bookkeeper.models import expense


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
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            cursor.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({p})', values)
            con.commit()
            obj.pk = cursor.lastrowid
            cursor.close()
        return obj.pk

    def add_empty(self) -> int:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            if self.data_type == expense.Expense:
                cursor.execute(f"INSERT INTO {self.table_name} (category) VALUES (1)")
            else:
                cursor.execute(f"INSERT INTO {self.table_name} DEFAULT VALUES")
            con.commit()
            cursor.close()
        return cursor.lastrowid

    def update(self, obj: abstract_repository.T) -> None:
        names = ' = ?, '.join(self.fields.keys()) + ' = ?'
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            cursor.execute(
                f'UPDATE {self.table_name} SET {names} WHERE id = {obj.pk}',
                values)
            con.commit()
            cursor.close()

    def update_item(self, row: int, col: str, value: typing.Any) -> None:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            cursor.execute(
                f'UPDATE {self.table_name} SET {col} = ? WHERE id = ?',
                (value, row))
            con.commit()
            cursor.close()

    def get(self, pk: int) -> abstract_repository.T | None:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name} LIMIT 1 OFFSET ?',
                           (pk - 1, ))
            res = self.data_type(*cursor.fetchone()[1:])
            res.pk = pk
            cursor.close()
        return res

    def get_all(
        self,
        where: dict[str, typing.Any] | None = None
    ) -> list[abstract_repository.T]:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            if where is None:
                cursor.execute(f'SELECT * FROM {self.table_name}')
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            elif next(iter(where.values())) is None:
                cursor.execute(
                    f'SELECT * FROM {self.table_name} WHERE {next(iter(where.keys()))} IS NULL'
                )
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            else:
                cursor.execute(
                    f'SELECT * FROM {self.table_name} WHERE {next(iter(where.keys()))} = ?',
                    (next(iter(where.values())), ))
                res = [
                    self.data_type(*(list(data[1:]) + [data[0]]))
                    for data in cursor.fetchall()
                ]
            cursor.close()
        return res

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            #deleting category we need delete all subcatogories
            if self.data_type == category.Category:
                values = tuple([pk] + [
                    cate.pk for cate in category.Category(
                        'name', pk=pk).get_subcategories(self)
                ])
                condition = 'id IN (' + ', '.join("?" * len(values)) + ')'
                cursor.execute(
                    f"DELETE FROM {self.table_name} WHERE {condition}", values)
                con.commit()
                #update rowid
                counts = {}
                cursor.execute(f"SELECT id FROM {self.table_name}")
                rowids = cursor.fetchall()
                for row in rowids:
                    count = sum(1 for value in values if value < row[0])
                    counts[row[0]] = count
                for rowid in counts.keys():
                    cursor.execute(
                        f'UPDATE {self.table_name} set id = id - ? WHERE id = ?',
                        (counts[rowid], rowid))
                    con.commit()
                    cursor.execute(
                        f'UPDATE {self.table_name} set parent = parent - ? WHERE parent = ?',
                        (counts[rowid], rowid))
                    con.commit()
            else:
                cursor.execute(
                    f'DELETE FROM {self.table_name} WHERE id = ?', (pk, ))
                con.commit()
                #update rowid
                cursor.execute(
                    f'UPDATE {self.table_name} set id = id - 1 WHERE id > ?',
                    (pk, ))
                con.commit()
            cursor.close()

    def del_all(self) -> None:
        with sqlite3.connect(self.db_file) as con:
            con.execute("PRAGMA foreign_keys = ON")
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM {self.table_name}")
            con.commit()
            cursor.close()
