import streamlit as st
import google.generativeai as genai
import sqlite3, hashlib, os, base64, time
from dotenv import load_dotenv
from docx import Document
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from docx.shared import Pt
from docx.oxml.ns import qn

# --- IMPORT MODULE GIAO DIỆN ---
import styles

# --- 1. CẤU HÌNH HỆ THỐNG ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(
    page_title="SmartLesson AI",
    layout="wide",
    page_icon="picture/logo.png"
)

MODEL_NAME = 'models/gemini-flash-latest' 

# --- 2. QUẢN LÝ DATABASE ---
DB_DIR = "storage"
DB_PATH = os.path.join(DB_DIR, "smart_lesson_official_v4.db") 
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

def run_query(query, params=(), fetch=False):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(query, params)
        if fetch: return cursor.fetchall()
        conn.commit()

# Khởi tạo các bảng dữ liệu
run_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, fullname TEXT)')
run_query('CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, subject TEXT, grade TEXT, book_series TEXT, lesson_title TEXT, duration TEXT, content_md TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

# --- 3. CÁC HÀM HỖ TRỢ (BASE64 & XUẤT FILE) ---
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

logo_64 = get_b64("picture/logo.png")

def export_word(title, content):
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    r = style.element.rPr.get_or_add_rFonts()
    for tag in ['w:eastAsia', 'w:ascii', 'w:hAnsi', 'w:cs']: r.set(qn(tag), 'Times New Roman')
    doc.add_heading(title.upper(), 0)
    doc.add_paragraph(content)
    bio = BytesIO(); doc.save(bio); return bio.getvalue()

def export_pdf(title, content):
    bio = BytesIO(); p = canvas.Canvas(bio, pagesize=A4)
    p.setFont("Helvetica-Bold", 16); p.drawString(100, 800, "GIAO AN: " + title)
    p.setFont("Helvetica", 12); y = 770
    for line in content.split('\n'):
        if y < 50: p.showPage(); p.setFont("Helvetica", 12); y = 800
        p.drawString(100, y, line[:80]); y -= 20
    p.save(); return bio.getvalue()

# --- 4. ÁP DỤNG GIAO DIỆN TỪ STYLES.PY ---
styles.apply_custom_css()

# --- 5. LOGIC ĐĂNG NHẬP & ĐĂNG KÝ ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    #st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        # Gọi hàm hiển thị Logo và Tiêu đề tím từ styles.py
        styles.render_login_logo(logo_64) 
        
        tab_login, tab_reg = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab_login:
            u = st.text_input("Tên đăng nhập", key="login_username")
            p = st.text_input("Mật khẩu", type="password", key="login_password")
            if st.button("XÁC NHẬN ĐĂNG NHẬP", use_container_width=True):
                phash = hashlib.sha256(p.encode()).hexdigest()
                res = run_query("SELECT id, fullname FROM users WHERE username=? AND password_hash=?", (u, phash), True)
                if res:
                    st.session_state.update({'auth': True, 'uid': res[0][0], 'name': res[0][1]})
                    st.rerun()
                else: st.error("Tài khoản hoặc mật khẩu không chính xác!")
                
        with tab_reg:
            nu = st.text_input("Tạo tên người dùng", key="reg_username")
            nn = st.text_input("Nhập họ và tên giáo viên", key="reg_fullname")
            np = st.text_input("Tạo mật khẩu bảo mật", type="password", key="reg_password")
            if st.button("HOÀN TẤT ĐĂNG KÝ", use_container_width=True):
                try:
                    run_query("INSERT INTO users (username, password_hash, fullname) VALUES (?,?,?)", (nu, hashlib.sha256(np.encode()).hexdigest(), nn))
                    st.success("Đăng ký thành công! Mời thầy đăng nhập.")
                except: st.error("Tên đăng nhập này đã được sử dụng!")
else:
    # --- 6. GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
    with st.sidebar:
        # Hiển thị Logo Sidebar
        st.markdown(f'''
            <div class="logo-container">
                <center><img src="data:image/png;base64,{logo_64}" class="sidebar-img"></center>
            </div>
            <h3 class="sidebar-name-label">GV: {st.session_state.name}</h3>
        ''', unsafe_allow_html=True)
        
        menu_choice = st.radio("CHỨC NĂNG HỆ THỐNG", ["📝 Soạn giáo án mới", "📁 Lịch sử bài dạy"])
        
        # Nút xuất file nhanh nếu đã có kết quả soạn thảo
        if 'last_res' in st.session_state:
            st.markdown("---")
            st.markdown("### 📥 XUẤT GIÁO ÁN")
            st.download_button("📄 Tải bản Word", data=export_word(st.session_state.lesson_title, st.session_state.last_res), file_name=f"GiaoAn_{st.session_state.lesson_title}.docx", use_container_width=True)
            st.download_button("📑 Tải bản PDF", data=export_pdf(st.session_state.lesson_title, st.session_state.last_res), file_name=f"GiaoAn_{st.session_state.lesson_title}.pdf", use_container_width=True)
        
        st.markdown("---")
        if st.button("🚪 ĐĂNG XUẤT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- 7. CHỨC NĂNG SOẠN GIÁO ÁN ---
    if menu_choice == "📝 Soạn giáo án mới":
        st.markdown('''
    <div class="gemini-banner">
        <h1>Thiết kế bài dạy thông minh</h1>
    </div>
''', unsafe_allow_html=True)
        
        with st.form("main_lesson_form"):
            col1, col2 = st.columns(2)
            with col1:
                mon = st.selectbox("Chọn môn học", ["Tin học", "Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học"])
                lop = st.selectbox("Chọn khối lớp", [str(i) for i in range(1, 13)])
            with col2:
                sach = st.selectbox("Bộ sách giáo khoa", ["Cánh Diều", "Kết nối tri thức", "Chân trời sáng tạo"])
                ten = st.text_input("Nhập tên bài dạy")
                tg = st.text_input("Thời lượng (Ví dụ: 2 tiết)")
            
            note = st.text_area("Yêu cầu sư phạm cụ thể (Phương pháp dạy, hoạt động nhóm...)", height=120)
            
            if st.form_submit_button("BẮT ĐẦU SOẠN THẢO BẰNG AI", use_container_width=True):
                if ten:
                    with st.spinner("AI đang phân tích chương trình và soạn thảo..."):
                        try:
                            # Cấu trúc prompt chuẩn 5512
                            prompt = f"Hãy soạn giáo án môn {mon} lớp {lop} theo sách {sach}, bài dạy: {ten}. Yêu cầu thêm: {note}. Trình bày theo đúng cấu trúc Công văn 5512 của Bộ Giáo dục."
                            res = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
                            
                            st.session_state.update({'last_res': res.text, 'lesson_title': ten})
                            
                            # Lưu vào lịch sử
                            run_query("INSERT INTO lessons (user_id, subject, grade, book_series, lesson_title, duration, content_md) VALUES (?,?,?,?,?,?,?)", 
                                     (st.session_state.uid, mon, lop, sach, ten, tg, res.text))
                            st.rerun()
                        except Exception as e: st.error(f"Lỗi hệ thống AI: {str(e)}")
                else: st.warning("Thầy vui lòng điền Tên bài dạy trước khi bắt đầu!")

        # Hiển thị kết quả giáo án vừa tạo
        if 'last_res' in st.session_state:
            st.markdown("### 📄 NỘI DUNG GIÁO ÁN CHI TIẾT")
            st.info(st.session_state.last_res)

    # --- 8. CHỨC NĂNG LỊCH SỬ ---
    else:
        st.markdown("## 📁 DANH SÁCH GIÁO ÁN ĐÃ SOẠN")
        history = run_query("SELECT lesson_title, created_at, content_md, id FROM lessons WHERE user_id=? ORDER BY id DESC", (st.session_state.uid,), True)
        
        if not history:
            st.info("Thầy chưa thực hiện soạn giáo án nào trên hệ thống.")
        else:
            for item in history:
                with st.expander(f"📙 Bài: {item[0]} (Ngày soạn: {item[1]})"):
                    st.markdown(item[2])
                    st.download_button("Tải lại bản Word", data=export_word(item[0], item[2]), 
                                     file_name=f"ReDownload_{item[0]}.docx", key=f"re_dl_{item[3]}")