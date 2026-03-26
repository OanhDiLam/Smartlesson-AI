import streamlit as st
import hashlib
import os
from styles import apply_custom_css
from database import init_db, run_query
from utils import get_b64_image, export_word
from ai_engine import generate_lesson_plan

# 1. CẤU HÌNH TRANG (Dùng đúng cấu hình cũ của thầy)
st.set_page_config(
    page_title="SmartLesson AI - GV Thạch Lâm Oanh Đi",
    layout="wide",
    page_icon="picture/logo.png",
    initial_sidebar_state="expanded"
)

# 2. KHỞI TẠO HỆ THỐNG
init_db()
apply_custom_css()
logo_64 = get_b64_image("picture/logo.png")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- PHẦN 1: GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.auth:
    # Tạo khoảng cách phía trên cho cân đối
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.5, 1]) # Tỉ lệ 1.5 giúp khung đăng nhập rộng rãi hơn
    
    with col:
        # ĐÂY LÀ PHẦN CODE CŨ LÀM NÊN VẺ ĐẸP:
        st.markdown(f'''
            <div style="text-align:center; background:white; padding:40px; border-radius:20px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <img src="data:image/png;base64,{logo_64}" width="120">
                <h1 style="color:#7B2CBF; margin-top:10px;">SmartLesson AI</h1>
                <p style="color:#64748B; font-weight:normal;">Hệ thống hỗ trợ giảng dạy 4.0</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # Các Tab đăng nhập nằm ngay bên dưới khối trắng
        tab_login, tab_reg = st.tabs(["🔐 Đăng nhập hệ thống", "📝 Tạo tài khoản mới"])
        
        with tab_login:
            u = st.text_input("Tên đăng nhập", key="login_username", placeholder="Nhập tài khoản...")
            p = st.text_input("Mật khẩu", type="password", key="login_password", placeholder="••••••••")
            
            if st.button("XÁC NHẬN ĐĂNG NHẬP", use_container_width=True):
                phash = hashlib.sha256(p.encode()).hexdigest()
                res = run_query("SELECT id, fullname FROM users WHERE username=? AND password_hash=?", (u, phash), True)
                if res:
                    st.session_state.update({'auth': True, 'uid': res[0][0], 'name': res[0][1]})
                    st.rerun()
                else:
                    st.error("⚠️ Tài khoản hoặc mật khẩu không chính xác!")

        with tab_reg:
            nu = st.text_input("Tên người dùng mới", key="reg_username")
            nn = st.text_input("Họ và tên giáo viên", key="reg_fullname", placeholder="Ví dụ: Thạch Lâm Oanh Đi")
            np = st.text_input("Mật khẩu bảo mật", type="password", key="reg_password")
            
            if st.button("HOÀN TẤT ĐĂNG KÝ", use_container_width=True):
                try:
                    run_query("INSERT INTO users (username, password_hash, fullname) VALUES (?,?,?)", 
                             (nu, hashlib.sha256(np.encode()).hexdigest(), nn))
                    st.success("✨ Đăng ký thành công! Mời thầy quay lại tab Đăng nhập.")
                except:
                    st.error("❌ Tên đăng nhập này đã được sử dụng!")
# --- PHẦN 2: GIAO DIỆN CHÍNH (SAU ĐĂNG NHẬP) ---
else:
    # SIDEBAR: Chứa Logo, Tên GV và Menu
    with st.sidebar:
        # Dùng đúng cấu trúc HTML cũ để khớp với CSS trong styles.py
        st.markdown(f'''
            <div class="logo-container">
                <center>
                    <img src="data:image/png;base64,{logo_64}" class="sidebar-img">
                </center>
            </div>
            <h3 class="sidebar-name-label">GV: {st.session_state.name}</h3>
        ''', unsafe_allow_html=True)
        
        menu = st.radio("CHỨC NĂNG", ["📝 Soạn giáo án", "📁 Lịch sử"])
        
        if 'last_res' in st.session_state:
            st.markdown("---")
            st.download_button(
                "📄 Tải bản Word", 
                data=export_word(st.session_state.lesson_title, st.session_state.last_res), 
                file_name=f"{st.session_state.lesson_title}.docx", 
                use_container_width=True
            )
            
        if st.button("🚪 THOÁT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # NỘI DUNG CHÍNH (Nằm ngoài khối sidebar)
    if menu == "📝 Soạn giáo án":
        st.markdown("<div class='banner-top'><h1>Thiết kế bài dạy thông minh</h1></div>", unsafe_allow_html=True)
        
        with st.form("lesson_form"):
            c1, c2 = st.columns(2)
            with c1:
                mon = st.selectbox("Môn học", ["Tin học", "Toán", "Văn", "Anh", "Lý", "Hóa"])
                lop = st.selectbox("Khối lớp", [str(i) for i in range(1, 13)])
            with c2:
                nxb = st.selectbox("Bộ sách", ["Cánh Diều", "Kết nối", "Chân trời"])
                ten = st.text_input("Tên bài dạy")
                tg = st.text_input("Thời lượng (ví dụ: 2 tiết)")
            
            note = st.text_area("Yêu cầu thêm (VD: Chia nhóm, thảo luận, giấy A0...)", height=100)
            
            if st.form_submit_button("BẮT ĐẦU SOẠN BÀI", use_container_width=True):
                if ten:
                    with st.spinner("AI đang soạn bài cho thầy..."):
                        content = generate_lesson_plan(mon, lop, nxb, ten, tg, note)
                        st.session_state.update({'last_res': content, 'lesson_title': ten})
                        # Lưu vào lịch sử
                        run_query("INSERT INTO lessons (user_id, subject, grade, book_series, lesson_title, duration, content_md) VALUES (?,?,?,?,?,?,?)", 
                                 (st.session_state.uid, mon, lop, nxb, ten, tg, content))
                        st.rerun()
                else:
                    st.warning("Thầy cần nhập tên bài dạy trước ạ!")
        
        # Hiển thị kết quả soạn bài
        if 'last_res' in st.session_state:
            st.info("Nội dung giáo án đã soạn:")
            st.markdown(st.session_state.last_res)
            
    else:
        # TRANG LỊCH SỬ
        st.markdown("## 📁 Lịch sử giáo án của thầy")
        history = run_query("SELECT lesson_title, created_at, content_md FROM lessons WHERE user_id=? ORDER BY id DESC", (st.session_state.uid,), fetch=True)
        if history:
            for h in history:
                with st.expander(f"📙 {h[0]} ({h[1]})"):
                    st.markdown(h[2])
        else:
            st.write("Thầy chưa có giáo án nào được lưu.")