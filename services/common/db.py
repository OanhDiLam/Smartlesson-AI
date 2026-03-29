import os
import sqlite3


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join("storage", "smart_lesson_official_v4.db"),
)


def ensure_database_dir():
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)


def get_connection():
    ensure_database_dir()
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_auth_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                fullname TEXT,
                avatar_base64 TEXT DEFAULT '',
                avatar_content_type TEXT DEFAULT ''
            )
            """
        )
        user_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()
        }
        if "avatar_base64" not in user_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN avatar_base64 TEXT DEFAULT ''"
            )
        if "avatar_content_type" not in user_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN avatar_content_type TEXT DEFAULT ''"
            )
        connection.commit()


def init_lesson_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                grade TEXT,
                book_series TEXT,
                lesson_title TEXT,
                duration TEXT,
                content_md TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shared_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uploader_id INTEGER NOT NULL,
                uploader_name TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                subject TEXT,
                grade TEXT,
                file_name TEXT NOT NULL,
                content_type TEXT NOT NULL,
                file_base64 TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shared_lesson_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shared_lesson_id INTEGER NOT NULL,
                commenter_id INTEGER NOT NULL,
                commenter_name TEXT NOT NULL,
                comment TEXT NOT NULL,
                parent_comment_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(shared_lesson_id) REFERENCES shared_lessons(id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shared_lesson_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shared_lesson_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(shared_lesson_id, user_id),
                FOREIGN KEY(shared_lesson_id) REFERENCES shared_lessons(id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shared_lesson_comment_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(comment_id, user_id),
                FOREIGN KEY(comment_id) REFERENCES shared_lesson_comments(id)
            )
            """
        )

        comment_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(shared_lesson_comments)").fetchall()
        }
        if "parent_comment_id" not in comment_columns:
            connection.execute(
                "ALTER TABLE shared_lesson_comments ADD COLUMN parent_comment_id INTEGER"
            )

        connection.commit()
