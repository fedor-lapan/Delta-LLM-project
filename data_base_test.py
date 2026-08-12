import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

print("Tables:")

for table in tables:
    print(table[0])

db.close()