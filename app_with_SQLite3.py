import sqlite3 as sql

# Connect to the database
connection = sql.connect('instance/posts.db')
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)"
)

a = cursor.execute("SELECT * FROM posts").fetchall()
post = {}

for i in range(1, len(a)+1):
    post[i] = {'title': a[i-1][1], 'content': a[i-1][2]}

print(post)