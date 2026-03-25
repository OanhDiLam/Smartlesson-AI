import streamlit as st
import google.generativeai as genai
import sqlite3
import hashlib
import os
import base64
from docx import Document
import io
from dotenv import load_dotenv
import warnings

# Tắt các cảnh báo không cần thiết để log Docker sạch sẽ
warnings.filterwarnings("ignore", category=FutureWarning)

# --- 1. CẤU HÌNH HỆ THỐNG ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Không tìm thấy API Key! Hãy kiểm tra file .env hoặc biến môi trường.")
    st.stop()

genai.configure(api_key=api_key)
DB_NAME = 'smart_lesson.db'
MODEL_NAME = 'gemini-2.0-flash' # Bản ổn định nhất cho giáo dục

# --- 2. TIỆN ÍCH HỆ THỐNG ---
def safe_rerun():
    """Hàm bổ trợ để chạy được trên cả Streamlit cũ và mới"""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, 
                  password_hash TEXT, fullname TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS lesson_plans 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, 
                  grade INTEGER, subject TEXT, publisher TEXT, content_md TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # Tạo Admin mặc định: admin / 123
    admin_hash = hashlib.sha256('123'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO users (username, password_hash, fullname) VALUES (?,?,?)', 
              ('admin', admin_hash, 'Quản trị viên Hệ thống'))
    conn.commit()
    conn.close()

init_db()

# Xử lý Logo cho Docker (Dùng gạch chéo xuôi)
LOGO_PATH = "picture/logo.png"
def get_img_64(path):
    try:
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return ""
img_64 = get_img_64(LOGO_PATH)

def export_to_docx(content, title):
    doc = Document()
    doc.add_heading(title, 0)
    for line in content.split('\n'):
        doc.add_paragraph(line)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 3. GIAO DIỆN (UI/UX) ---
st.set_page_config(page_title="SmartLesson AI", page_icon=LOGO_PATH, layout="wide")

# CSS "Hard-code" để ép giao diện luôn đẹp bất kể chế độ Dark/Light Mode của trình duyệt
st.markdown(f"""
    <style>
    /* Ép nền trắng toàn trang */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }}

    /* Ép màu cho các ô nhập liệu - Dùng Selector mạnh nhất */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div, 
    div[data-baseweb="textarea"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #7C3AED !important; /* Viền tím đậm cho rõ ràng */
    }}

    /* Sửa lỗi chữ trong ô nhập liệu bị trắng (khó nhìn) */
    input, textarea, span {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}

    /* Màu chữ tiêu đề (Labels) */
    label p {{
        color: #4B5563 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}

    /* Nút bấm "Xác nhận" */
    .stButton > button {{
        width: 100% !important;
        background: #7C3AED !important;
        color: white !important;
        border: none !important;
        padding: 15px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIC CHÍNH ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    # MÀN HÌNH ĐĂNG NHẬP
    st.markdown(f"""<div class='header-box'>
        <img src='data:image/png;base64,{img_64}' style='width:120px; filter: brightness(0) invert(1);'>
        <h1>SmartLesson AI</h1>
        <p>Hệ thống trợ lý soạn bài giảng theo chuẩn Công văn 5512</p>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    with t1:
        u = st.text_input("Tên đăng nhập", key="u_in")
        p = st.text_input("Mật khẩu", type="password", key="p_in")
        if st.button("XÁC NHẬN ĐĂNG NHẬP", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            user = conn.execute("SELECT id, fullname FROM users WHERE username=? AND password_hash=?", 
                                (u, hashlib.sha256(p.encode()).hexdigest())).fetchone()
            conn.close()
            if user:
                st.session_state.update({'auth': True, 'uid': user[0], 'uname': user[1]})
                safe_rerun()
            else: st.error("Tài khoản hoặc mật khẩu không chính xác!")

    with t2:
        nu = st.text_input("Tên đăng nhập mới")
        nn = st.text_input("Họ tên giáo viên")
        np = st.text_input("Mật khẩu mới", type="password")
        if st.button("TẠO TÀI KHOẢN MỚI", use_container_width=True):
            try:
                conn = sqlite3.connect(DB_NAME)
                conn.execute("INSERT INTO users (username, password_hash, fullname) VALUES (?,?,?)", 
                             (nu, hashlib.sha256(np.encode()).hexdigest(), nn))
                conn.commit(); conn.close()
                st.success("✅ Đăng ký thành công! Hãy quay lại tab Đăng nhập.")
            except: st.error("Tên đăng nhập này đã có người sử dụng.")

else:
    # MÀN HÌNH LÀM VIỆC
    with st.sidebar:
        st.markdown(f"""<div style='text-align:center; padding:20px;'>
            <img src='data:image/png;base64,{img_64}' style='width:100px;'>
            <h3 style='color:#7C3AED;'>Thầy/Cô: {st.session_state['uname']}</h3>
        </div>""", unsafe_allow_html=True)
        menu = st.radio("CHỨC NĂNG", ["📝 Soạn giáo án mới", "📁 Kho lưu trữ giáo án"])
        st.divider()
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state['auth'] = False
            safe_rerun()

    if "Soạn giáo án" in menu:
        st.markdown("<div class='header-box'><h2>Thiết lập bài giảng thông minh</h2></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            grade = st.selectbox("Khối lớp", [10, 11, 12])
            sub = st.selectbox("Môn học", ["Tin học", "Tiếng Anh", "Toán học", "Ngữ văn", "Vật lý", "Hóa học"])
            topic = st.text_input("Tên bài học cần soạn")
        with c2:
            pub = st.selectbox("Bộ sách", ["Cánh Diều", "Kết Nối Tri Thức", "Chân Trời Sáng Tạo"])
            dur = st.number_input("Thời lượng (phút)", value=45, step=45)
            style = st.selectbox("Phong cách", ["Chi tiết từng hoạt động", "Trọng tâm kiến thức"])
        
        notes = st.text_area("🗒️ Ghi chú thêm cho AI (ví dụ: Tập trung vào thực hành, tổ chức trò chơi...)")
        
        if st.button("🚀 BẮT ĐẦU SOẠN THẢO VỚI GEMINI AI", use_container_width=True):
            if not topic: st.warning("Vui lòng nhập tên bài học.")
            else:
                with st.spinner("AI đang nghiên cứu chương trình và soạn thảo..."):
                    try:
                        model = genai.GenerativeModel(MODEL_NAME)
                        prompt = f"""
                        Đóng vai chuyên gia giáo dục. Soạn giáo án môn {sub}, lớp {grade}, bài: {topic}. 
                        Sách: {pub}. Thời lượng: {dur} phút. Phong cách: {style}. 
                        Yêu cầu: Tuân thủ cấu trúc Công văn 5512 (Mục tiêu, Thiết bị, Hoạt động: Khởi động, Kiến thức mới, Luyện tập, Vận dụng). 
                        Ghi chú thêm: {notes}
                        """
                        res = model.generate_content(prompt).text
                        st.session_state['cur_res'], st.session_state['cur_top'] = res, topic
                        
                        conn = sqlite3.connect(DB_NAME)
                        conn.execute("INSERT INTO lesson_plans (user_id, title, grade, subject, publisher, content_md) VALUES (?,?,?,?,?,?)", 
                                     (st.session_state['uid'], topic, grade, sub, pub, res))
                        conn.commit(); conn.close()
                    except Exception as e: st.error(f"Lỗi AI: {e}")

        if 'cur_res' in st.session_state:
            st.markdown(f"<div class='lesson-output'>{st.session_state['cur_res']}</div>", unsafe_allow_html=True)
            doc = export_to_docx(st.session_state['cur_res'], st.session_state['cur_top'])
            st.download_button("📥 Tải file Word (.docx)", data=doc, file_name=f"GiaoAn_{st.session_state['cur_top']}.docx", use_container_width=True)

    else:
        st.markdown("<div class='header-box'><h2>📁 Kho lưu trữ giáo án cá nhân</h2></div>", unsafe_allow_html=True)
        conn = sqlite3.connect(DB_NAME)
        plans = conn.execute("SELECT title, created_at, content_md FROM lesson_plans WHERE user_id=? ORDER BY created_at DESC", (st.session_state['uid'],)).fetchall()
        conn.close()
        for p in plans:
            with st.expander(f"📚 {p[0]} (Soạn ngày: {p[1]})"):
                st.markdown(f"<div class='lesson-output'>{p[2]}</div>", unsafe_allow_html=True)
                doc = export_to_docx(p[2], p[0])
                st.download_button(f"Tải lại bài {p[0]}", data=doc, file_name=f"Re_{p[0]}.docx", key=f"dl_{p[1]}")