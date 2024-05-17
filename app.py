from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

# Connect to the database
# with open("instance/posts.db", "w") as db:
conn = sql.connect('instance/posts.db')
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)"
)
conn.commit()
conn.close()



app = Flask(__name__)



@app.route('/')
def home():
    """
    This is the home page of the blog.
    This contains hyperlinks to all the posts in the database.
    """
    conn = sql.connect('instance/posts.db')
    cursor = conn.cursor()
    a = cursor.execute("SELECT * FROM posts").fetchall()
    posts = {}
    for i in range(1, len(a) + 1):
        posts[i] = {'title': a[i - 1][1], 'content': a[i - 1][2]}
    conn.close()
    return render_template('home.jinja2', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    """
    :type post_id: int
    :param post_id:
    Helps users to view a specific post, from the database
    """
    # post = posts.get(post_id)
    # Gets the post from the database
    conn = sql.connect('instance/posts.db')
    cursor = conn.cursor()
    a = cursor.execute("SELECT * FROM posts").fetchall()
    posts = {}
    for i in range(1, len(a) + 1):
        posts[i] = {'title': a[i - 1][1], 'content': a[i - 1][2]}
    conn.close()
    post = posts.get(post_id)
    if not post:
        return render_template('404.jinja2', message=f'A post with id {post_id} was not found.')
    return render_template('post.jinja2', post=post)


@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        conn = sql.connect('instance/posts.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        post_id = cursor.lastrowid
        return redirect(url_for('post', post_id=post_id))
    return render_template('create.jinja2')


if __name__ == '__main__':
    app.run(debug=True,port=os.getenv("PORT", default=5000))
