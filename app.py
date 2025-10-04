
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'journal.db'

QUOTES = [
    "No act of kindness, no matter how small, is ever wasted. — Aesop",
    "Kindness is a language which the deaf can hear and the blind can see. — Mark Twain",
    "Carry out a random act of kindness, with no expectation of reward. — Princess Diana",
    "Wherever there is a human being, there is an opportunity for a kindness. — Seneca",
    "A single act of kindness throws out roots in all directions. — Amelia Earhart"
]

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT NOT NULL,
        mood TEXT,
        date TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.context_processor
def inject_datetime():
    from datetime import datetime
    return {'datetime': datetime}


@app.route('/')
def index():

    quote = random.choice(QUOTES)
    return render_template('index.html', quote=quote)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        mood = request.form.get('mood', '').strip()
        date = request.form.get('date', '').strip() or datetime.now().strftime('%Y-%m-%d')
        if not description:
            return redirect(url_for('add'))
        conn = get_db_connection()
        conn.execute('INSERT INTO entries (title, description, mood, date) VALUES (?, ?, ?, ?)',
                     (title, description, mood, date))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    return render_template('add.html')

@app.route('/view')
def view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM entries ORDER BY date DESC, id DESC').fetchall()
    conn.close()
    return render_template('view.html', entries=rows)

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('success.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if username and password:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                return render_template('register.html', error='Username already exists')
            conn.close()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
