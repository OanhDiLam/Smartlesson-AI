import sqlite3
import os

DB_DIR = "storage"
DB_PATH = os.path.join(DB_DIR, "smart_lesson_v4.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def run_query(query, params=(), fetch=False):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(query, params)
        if fetch: 
            return cursor.fetchall()  # Phải có dòng này để lấy dữ liệu về app.py
        conn.commit()
        return None

def init_db():
    run_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, fullname TEXT)')
    run_query('CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, subject TEXT, grade TEXT, book_series TEXT, lesson_title TEXT, duration TEXT, content_md TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')