import sqlite3
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from inspect import get_annotations
from datetime import datetime

# # with sqlite3.connect("tutorial.db") as con:
# #     cursor = con.cursor()
# #     cursor.execute("SELECT * FROM category")
# #     print(cursor.fetchall())
# #     cursor.close()
# # con = sqlite3.connect("tutorial.db")
# # cur = con.cursor()
# # cur.execute("CREATE TABLE expense (amount INTERGER, category INTERGER, expense_date TEXT, date TEXT, comment TEXT)")
# # cur.execute("CREATE TABLE category (name TEXT, parent INTERGER)")
# repo = SQLiteRepository[Expense]("tutorial.db", Expense)
# repo.del_all()
# repo.add(Expense(50, 1))
# repo.add(Expense(50, 2))
# repo.add(Expense(50, 3))

repo = SQLiteRepository[Expense]("tutorial.db", Expense)
# repo.del_all()
# repo.add(Category('food'))
# repo.add(Category('fish', 1))
# repo.delete(4)
# repo.add(Category('meat', 1))
print(repo.get_all())
