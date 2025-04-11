import sqlite3

conn = sqlite3.connect("db/aptly.db")  # Make sure this matches database.py path
cursor = conn.cursor()

cursor.execute("SELECT * FROM shortlist_results")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
