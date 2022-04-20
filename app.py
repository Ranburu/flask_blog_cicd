import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from psycopg2.extras import RealDictCursor
from werkzeug.exceptions import abort


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        cursor_factory=RealDictCursor)
    return conn


def get_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cur.fetchone()
    cur.close()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts;')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', 'alert alert-danger')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                        (title, content))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', 'alert alert-danger')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('UPDATE posts SET title = %s, content = %s'
                        ' WHERE id = %s',
                        (title, content, id))
            conn.commit()
            cur.close()
            conn.close()
            flash('"{}" was successfully edited!'.format(post['title']), 'alert alert-success')
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']), 'alert alert-success')
    return redirect(url_for('index'))
