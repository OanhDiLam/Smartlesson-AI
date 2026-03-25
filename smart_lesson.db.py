import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect('smart_lesson.db')
    c = conn.cursor()

    # Bảng Người dùng (Giáo viên)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    fullname TEXT NOT NULL)''')

    # Bảng Lưu Giáo án (Liên kết với người dùng qua user_id)
    c.execute('''CREATE TABLE IF NOT EXISTS lesson_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    grade TEXT,
                    subject TEXT,
                    publisher TEXT,
                    content_md TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')

    # Chèn dữ liệu mẫu nếu chưa có
    try:
        # Tài khoản mặc định: admin / 123456
        c.execute("INSERT INTO users (username, password_hash, fullname) VALUES (?,?,?)", 
                  ("admin", hash_password("123456"), "Giáo viên Quản trị"))
        conn.commit()
        print("✅ Đã khởi tạo CSDL SmartLesson thành công!")
    except sqlite3.IntegrityError:
        print("⚠️ CSDL đã tồn tại.")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()