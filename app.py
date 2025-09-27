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