import streamlit as st
import google.generativeai as genai
import sqlite3
import hashlib
import os
import base64
import warnings
import io
from docx import Document
from dotenv import load_dotenv

# Tắt các cảnh báo không cần thiết để log Docker chuyên nghiệp hơn
warnings.filterwarnings("ignore", category=FutureWarning)

# --- 1. CẤU HÌNH HỆ THỐNG ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Không tìm thấy API Key! Vui lòng kiểm tra file .env hoặc cấu hình Docker.")
    st.stop()

genai.configure(api_key=api_key)
DB_NAME = 'smart_lesson.db'

# Sử dụng bản 1.5-flash-latest để đảm bảo 100% không lỗi 404 khi demo
MODEL_NAME = 'gemini-1.5-flash'

# --- 2. QUẢN TRỊ DATABASE (ANTI-LOCK & THREAD-SAFE) ---
def get_db_connection():
    """Kết nối SQLite với chế độ WAL để tránh lỗi 'database is locked'"""
    conn = sqlite3.connect(DB_NAME, timeout=30)
    conn.execute('PRAGMA journal_mode=WAL;') 
    return conn

def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, 
                      password_hash TEXT, fullname TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS lesson_plans 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, 
                      grade INTEGER, subject TEXT, publisher TEXT, content_md TEXT, 
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        # Tạo tài khoản Admin mặc định (Pass: 123)
        admin_pass = hashlib.sha256('123'.encode()).hexdigest()
        c.execute('INSERT OR IGNORE INTO users (username, password_hash, fullname) VALUES (?,?,?)', 
                  ('admin', admin_pass, 'Quản trị viên Hệ thống'))
        conn.commit()

init_db()

# --- 3. TIỆN ÍCH HỆ THỐNG ---
LOGO_PATH = "picture/logo.png"
def get_img_64(path):
    try:
        with open(path, "rb") as f: 
            return base64.b64encode(f.read()).decode()
    except: 
        return ""

img_64 = get_img_64(LOGO_PATH)

def export_to_docx(content, title):
    doc = Document()
    doc.add_heading(title, 0)
    for line in content.split('\n'):
        doc.add_paragraph(line)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. GIAO DIỆN (UI/UX) - XÓA NÚT DEPLOY & MAIN MENU ---
st.set_page_config(page_title="SmartLesson AI", page_icon=LOGO_PATH, layout="wide")

st.markdown(f"""
    <style>
    /* Xóa sạch các thành phần thừa của Streamlit (Deploy, Menu, Header) */
    [data-testid="stHeader"] {{ display: none !important; }}
    .stAppDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    
    /* Ép tông màu Light Mode (Trắng - Tím) bất chấp cài đặt máy tính */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }}

    /* Tùy chỉnh các ô nhập liệu (Input/Select/TextArea) */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div, 
    div[data-baseweb="textarea"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #7C3AED !important;
        border-radius: 10px !important;
    }}
    
    /* Fix lỗi chữ tàng hình trong các ô nhập liệu */
    input, textarea, span {{ 
        color: #000000 !important; 
        -webkit-text-fill-color: #000000 !important; 
    }}
    
    label p {{ 
        color: #4B5563 !important; 
        font-weight: bold !important; 
        font-size: 1rem !important; 
    }}

    /* Header Box màu Tím Gradient */
    .header-box {{
        background: linear-gradient(135deg, #6D28D9 0%, #8B5CF6 100%);
        padding: 40px; 
        border-radius: 20px; 
        text-align: center; 
        color: white !important; 
        margin-bottom: 30px;
    }}
    .header-box h1, .header-box p {{ color: white !important; }}

    /* Sidebar xám nhạt */
    [data-testid="stSidebar"] {{ 
        background-color: #F8FAFC !important; 
        border-right: 1px solid #E2E8F0; 
    }}

    /* Nút bấm Tím Sư phạm */
    .stButton>button {{
        background-color: #7C3AED !important; 
        color: white !important;
        border-radius: 12px !important; 
        font-weight: bold !important; 
        width: 100%; 
        height: 50px;
        border: none !important;
    }}

    /* Khung hiển thị giáo án AI */
    .lesson-output {{
        background-color: #FFFFFF; 
        color: #111827 !important; 
        padding: 35px;
        border: 1px solid #E5E7EB; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-size: 1.1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIC CHƯƠNG TRÌNH ---
if 'auth' not in st.session_state: 
    st.session_state['auth'] = False

if not st.session_state['auth']:
    # --- MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ ---
    st.markdown(f"""<div class='header-box'>
        <img src='data:image/png;base64,{img_64}' style='width:120px; filter: brightness(0) invert(1);'>
        <h1>SmartLesson AI</h1>
        <p>Nền tảng trợ lý soạn bài giảng thông minh chuẩn Công văn 5512</p>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 Đăng nhập hệ thống", "📝 Đăng ký tài khoản mới"])
    
    with t1:
        u = st.text_input("Tên đăng nhập", key="login_u")
        p = st.text_input("Mật khẩu", type="password", key="login_p")
        if st.button("XÁC NHẬN ĐĂNG NHẬP"):
            with get_db_connection() as conn:
                res = conn.execute("SELECT id, fullname FROM users WHERE username=? AND password_hash=?", 
                                   (u, hashlib.sha256(p.encode()).hexdigest())).fetchone()
                if res:
                    st.session_state.update({'auth': True, 'uid': res[0], 'uname': res[1]})
                    st.rerun() # Lệnh làm mới trang chuẩn của Streamlit 2026
                else: 
                    st.error("❌ Tài khoản hoặc mật khẩu không chính xác!")

    with t2:
        nu = st.text_input("Tên người dùng mới")
        nn = st.text_input("Họ và tên giáo viên")
        np = st.text_input("Mật khẩu bảo mật", type="password")
        if st.button("HOÀN TẤT ĐĂNG KÝ"):
            try:
                with get_db_connection() as conn:
                    conn.execute("INSERT INTO users (username, password_hash, fullname) VALUES (?,?,?)", 
                                 (nu, hashlib.sha256(np.encode()).hexdigest(), nn))
                    conn.commit()
                    st.success("✅ Đăng ký thành công! Mời Thầy/Cô quay lại tab Đăng nhập.")
            except: 
                st.error("❌ Tên đăng nhập đã tồn tại trong hệ thống.")

else:
    # --- MÀN HÌNH LÀM VIỆC CHÍNH ---
    with st.sidebar:
        st.markdown(f"""<div style='text-align:center; padding-bottom:20px;'>
            <img src='data:image/png;base64,{img_64}' style='width:100px;'>
            <h3 style='color:#7C3AED;'>Thầy/Cô: {st.session_state['uname']}</h3>
        </div>""", unsafe_allow_html=True)
        
        menu = st.radio("ĐIỀU HƯỚNG", ["📝 Soạn giáo án mới", "📁 Kho lưu trữ giáo án"])
        st.divider()
        if st.button("🚪 Đăng xuất khỏi hệ thống"):
            st.session_state['auth'] = False
            st.rerun()

    if "Soạn giáo án" in menu:
        st.markdown("<div class='header-box'><h2>Thiết kế kế hoạch bài dạy</h2></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            grade = st.selectbox("Chọn khối lớp", [10, 11, 12])
            sub = st.selectbox("Môn học giảng dạy", ["Tin học", "Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học"])
            topic = st.text_input("Nhập tên bài học (Ví dụ: Cấu trúc lặp)")
        with c2:
            pub = st.selectbox("Bộ sách sử dụng", ["Cánh Diều", "Kết Nối Tri Thức", "Chân Trời Sáng Tạo"])
            dur = st.number_input("Thời lượng tiết dạy (phút)", value=45, step=45)
            style = st.selectbox("Phong cách soạn thảo", ["Chi tiết từng hoạt động", "Tập trung kiến thức cốt lõi"])
        
        notes = st.text_area("🗒️ Ghi chú bổ sung cho AI (Ví dụ: Tổ chức thảo luận nhóm, tích hợp trò chơi...)")
        
        if st.button("🚀 BẮT ĐẦU SOẠN THẢO VỚI AI"):
            if not topic: 
                st.warning("⚠️ Vui lòng nhập tên bài học để AI có dữ liệu soạn thảo.")
            else:
                with st.spinner("⏳ AI đang nghiên cứu chương trình và thiết kế giáo án chuẩn 5512..."):
                    try:
                        model = genai.GenerativeModel(MODEL_NAME)
                        # Prompt tối ưu hóa cho giáo dục Việt Nam
                        prompt = (f"Hãy đóng vai chuyên gia giáo dục. Soạn giáo án môn {sub}, lớp {grade}, bài: {topic}. "
                                  f"Ngữ liệu sách: {pub}. Thời lượng: {dur} phút. Phong cách: {style}. "
                                  f"Yêu cầu: Tuân thủ cấu trúc Công văn 5512 (Mục tiêu, Thiết bị dạy học, "
                                  f"Tiến trình dạy học: Khởi động, Kiến thức mới, Luyện tập, Vận dụng). "
                                  f"Ghi chú riêng: {notes}")
                        
                        response = model.generate_content(prompt)
                        res_text = response.text
                        st.session_state['res'], st.session_state['top'] = res_text, topic
                        
                        # Lưu giáo án vào cơ sở dữ liệu
                        with get_db_connection() as conn:
                            conn.execute("""INSERT INTO lesson_plans 
                                            (user_id, title, grade, subject, publisher, content_md) 
                                            VALUES (?,?,?,?,?,?)""", 
                                         (st.session_state['uid'], topic, grade, sub, pub, res_text))
                            conn.commit()
                    except Exception as e: 
                        st.error(f"❌ Lỗi kết nối AI: {e}")

        # Hiển thị kết quả và nút tải file
        if 'res' in st.session_state:
            st.divider()
            st.markdown(f"### 📄 Kết quả bài soạn: {st.session_state['top']}")
            st.markdown(f"<div class='lesson-output'>{st.session_state['res']}</div>", unsafe_allow_html=True)
            
            doc_data = export_to_docx(st.session_state['res'], st.session_state['top'])
            st.download_button(label="📥 Tải xuống giáo án (.docx)", 
                               data=doc_data, 
                               file_name=f"GiaoAn_{st.session_state['top']}.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    else:
        # --- KHO LƯU TRỮ ---
        st.markdown("<div class='header-box'><h2>📁 Kho lưu trữ giáo án cá nhân</h2></div>", unsafe_allow_html=True)
        with get_db_connection() as conn:
            plans = conn.execute("""SELECT title, created_at, content_md FROM lesson_plans 
                                    WHERE user_id=? ORDER BY created_at DESC""", 
                                 (st.session_state['uid'],)).fetchall()
        
        if not plans:
            st.info("Hiện tại Thầy/Cô chưa có giáo án nào được lưu trong kho.")
        else:
            for p in plans:
                with st.expander(f"📚 {p[0]} (Ngày soạn: {p[1]})"):
                    st.markdown(f"<div class='lesson-output'>{p[2]}</div>", unsafe_allow_html=True)
                    doc_data = export_to_docx(p[2], p[0])
                    st.download_button(f"📥 Tải lại bản Word bài {p[0]}", 
                                       data=doc_data, 
                                       file_name=f"Re_{p[0]}.docx", 
                                       key=f"dl_{p[1]}")