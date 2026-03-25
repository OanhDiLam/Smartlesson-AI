import streamlit as st
import google.generativeai as genai
import sqlite3
import hashlib
import os
import base64
from docx import Document
import io
from dotenv import load_dotenv

# --- 1. CẤU HÌNH & BẢO MẬT ---
load_dotenv()
# Bảo mật: Ưu tiên lấy từ .env, nếu không có mới dùng dự phòng (nên giấu Key đi nhé bro)
api_key = os.getenv("GOOGLE_API_KEY") 
if not api_key:
    st.error("⚠️ Thiếu API Key! Vui lòng kiểm tra file .env")
    st.stop()

genai.configure(api_key=api_key)
DB_NAME = 'smart_lesson.db'

# Tên Model chuẩn xác nhất cho Gemini hiện tại
MODEL_NAME = 'gemini-3-flash' 

# --- 2. TỰ ĐỘNG KHỞI TẠO DATABASE ---
def init_db_auto():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, fullname TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS lesson_plans (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, grade INTEGER, subject TEXT, publisher TEXT, content_md TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        # Tạo Admin mặc định
        c.execute('INSERT OR IGNORE INTO users (username, password_hash, fullname) VALUES (?,?,?)', 
                  ('admin', hashlib.sha256('123'.encode()).hexdigest(), 'Quản trị viên'))
        conn.commit()
        conn.close()

init_db_auto()

# --- 3. TIỆN ÍCH ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return ""

LOGO_PATH = r"picture\logo.png" # Đường dẫn tương đối cho dễ quản lý trên Git
img_base64 = get_base64_image(LOGO_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def export_to_docx(content, title):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. GIAO DIỆN (Đã tối ưu CSS căn giữa & Xóa Top Bar) ---
st.set_page_config(page_title="SmartLesson AI", page_icon=LOGO_PATH, layout="wide")

st.markdown(f"""
    <style>
    [data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ padding-top: 1rem !important; margin-top: -20px; }}
    footer {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}

    html, body, [data-testid="stAppViewContainer"] {{ background-color: #FFFFFF !important; color: #6D28D9 !important; }}

    [data-testid="stSidebarContent"] {{ display: flex; flex-direction: column; align-items: center; }}
    .profile-container {{ display: flex; flex-direction: column; align-items: center; text-align: center; padding: 20px 0; }}
    .sidebar-logo {{ width: 110px; mix-blend-mode: multiply; margin-bottom: 10px; }}
    
    [data-testid="stSidebar"] .stButton {{ display: flex; justify-content: center; width: 100%; }}
    [data-testid="stSidebar"] .stButton>button {{ width: 160px !important; background-color: #7C3AED !important; color: white !important; border-radius: 20px !important; }}

    .main-header {{ background-color: #F5F3FF; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 4px solid #7C3AED; margin-bottom: 20px; }}
    .logo-img-main {{ width: 160px; mix-blend-mode: multiply; }}

    .lesson-content {{ color: #000000 !important; background-color: #FFFFFF; padding: 30px; border: 1px solid #E5E7EB; border-radius: 12px; line-height: 1.8; }}
    .lesson-content * {{ color: #000000 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIC ỨNG DỤNG ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown(f"<div class='main-header'><img src='data:image/png;base64,{img_base64}' class='logo-img-main'><h1>SmartLesson AI</h1></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    with t1:
        u = st.text_input("Tên đăng nhập", key="lu")
        p = st.text_input("Mật khẩu", type="password", key="lp")
        if st.button("ĐĂNG NHẬP"):
            conn = get_db_connection()
            user = conn.execute("SELECT id, fullname FROM users WHERE username=? AND password_hash=?", (u, hash_password(p))).fetchone()
            conn.close()
            if user:
                st.session_state.update({'logged_in': True, 'user_id': user[0], 'name': user[1]})
                st.rerun()
            else: st.error("Sai tài khoản.")
else:
    with st.sidebar:
        st.markdown(f'<div class="profile-container"><img src="data:image/png;base64,{img_base64}" class="sidebar-logo"><div style="color:#6D28D9;">👤 <b>Thầy/Cô:</b><br>{st.session_state["name"]}</div></div>', unsafe_allow_html=True)
        if st.button("Đăng xuất"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        menu = st.radio("Chức năng", ["📖 Soạn giáo án", "📁 Kho lưu trữ"])

    if "Soạn giáo án" in menu:
        st.markdown(f"<div class='main-header'><img src='data:image/png;base64,{img_base64}' class='logo-img-main'><h2>Thiết lập bài giảng mới</h2></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            grade = st.selectbox("Khối lớp", [10, 11, 12])
            sub = st.selectbox("Môn học", ["Tiếng Anh", "Tin học", "Toán học", "Ngữ văn", "Vật lý", "Hóa học"])
            topic = st.text_input("Tên bài học")
        with c2:
            pub = st.selectbox("Bộ sách", ["Global Success", "Kết Nối Tri Thức", "Cánh Diều", "Chân Trời Sáng Tạo"])
            dur = st.number_input("Thời lượng (phút)", value=45)
            style = st.selectbox("Phong cách", ["Chi tiết", "Trọng tâm"])
        
        notes = st.text_area("🗒️ Ghi chú yêu cầu cụ thể")
        if st.button("BẮT ĐẦU SOẠN THẢO", icon="📝"):
            if topic:
                with st.spinner('⏳ AI đang soạn bài...'):
                    try:
                        model = genai.GenerativeModel(MODEL_NAME)
                        prompt = f"Soạn giáo án {sub} {grade}, bài {topic}, sách {pub}. Chuẩn 5512. Yêu cầu: {notes}"
                        response = model.generate_content(prompt)
                        st.session_state['res'], st.session_state['top'] = response.text, topic
                        st.markdown(f"<div class='lesson-content'>{response.text}</div>", unsafe_allow_html=True)
                        conn = get_db_connection()
                        conn.execute("INSERT INTO lesson_plans (user_id, title, grade, subject, publisher, content_md) VALUES (?,?,?,?,?,?)", (st.session_state['user_id'], topic, grade, sub, pub, response.text))
                        conn.commit()
                        conn.close()
                    except Exception as e: st.error(f"Lỗi: {e}")
        
        if 'res' in st.session_state:
            btn_data = export_to_docx(st.session_state['res'], st.session_state['top'])
            st.download_button("📝 Tải file Word (.docx)", data=btn_data, file_name=f"GiaoAn_{st.session_state['top']}.docx")

    elif "Kho lưu trữ" in menu:
        st.header("📁 Lịch sử giáo án")
        conn = get_db_connection()
        plans = conn.execute("SELECT title, created_at, content_md FROM lesson_plans WHERE user_id=? ORDER BY created_at DESC", (st.session_state['user_id'],)).fetchall()
        conn.close()
        for p in plans:
            with st.expander(f"📚 {p[0]} ({p[1]})"):
                st.markdown(f"<div class='lesson-content'>{p[2]}</div>", unsafe_allow_html=True)