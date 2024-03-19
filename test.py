import sqlite3
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from inspect import get_annotations
# with sqlite3.connect("tutorial.db") as con:
#     cursor = con.cursor()
#     cursor.execute("SELECT * FROM category")
#     print(cursor.fetchall())
#     cursor.close()
# con = sqlite3.connect("tutorial.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE expense (amount, category, expense_date, date, comment)")
# cur.execute("CREATE TABLE category (name, parent)")
repo = SQLiteRepository[Category]("tutorial.db", Category)
repo.del_all()
repo.add(Category('food', None))
repo.add(Category('meat', parent=1))
repo.add(Category('fish', parent=1))
print(repo.get_all())

