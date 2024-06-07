import sqlite3

# Connect to the database
conn = sqlite3.connect('book.db')

# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON")

# Create a cursor object
cur = conn.cursor()

# Create Customers table
cur.execute("CREATE TABLE category (id INTEGER PRIMARY KEY, name TEXT, parent INTERGER)")
conn.commit()
# Create Orders table with a foreign key
cur.execute("CREATE TABLE expense (id INTEGER PRIMARY KEY, amount INTERGER, category INTERGER, expense_date TEXT, date TEXT, comment TEXT, FOREIGN KEY (category) REFERENCES category (id) ON DELETE CASCADE ON UPDATE CASCADE)")
cur.execute("INSERT INTO category (name) VALUES ('Uncategorized')")
conn.commit()