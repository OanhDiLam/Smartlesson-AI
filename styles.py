import streamlit as st

def apply_custom_css():
    """Hàm thiết lập toàn bộ giao diện: Nền trắng, chữ tím, nút tím, banner Gemini"""
    st.markdown("""
        <style>
        /* 🛠 ĐỊNH DẠNG CHỮ TÍM CHO NỘI DUNG TRONG CARD ĐĂNG NHẬP */
        div.login-content-box {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important; /* Đảm bảo màu tím trên mọi trình duyệt */
            text-align: center !important;
        }

        /* ÉP CẢ CÁC THẺ CON (NẾU CÓ) CŨNG PHẢI MÀU TÍM */
        div.login-content-box .login-title, 
        div.login-content-box .login-subtitle,
        div.login-content-box div {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
        }
                
                [data-testid="stSidebar"] {
            border-right: 2px solid #7B2CBF33 !important; /* Viền tím nhạt 20% độ trong suốt */
            box-shadow: 2px 0 5px rgba(0,0,0,0.05) !important; /* Đổ bóng nhẹ sang phải */
        }

        /* Đảm bảo đường viền chạy xuyên suốt từ trên xuống */
        section[data-testid="stSidebar"] > div {
            height: 100vh !important;
        }

        /* 🛠 ĐỒNG BỘ BANNER: DÍNH MÉP VÀ KHÔNG ĐÈ SIDEBAR */
        div.gemini-banner {
            background: linear-gradient(135deg, #4285F4 0%, #9b72f3 35%, #d96570 70%, #f8e6e7 100%) !important;
            padding: 15px 10px !important;
            border-radius: 0 0 20px 20px !important;
            text-align: center !important;
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            /* Tính toán để né Sidebar (thường là 21rem ~ 336px) */
            left: 336px !important; 
            z-index: 99 !important;
            margin: 0 !important;
            /* Thêm một đường viền dưới cho banner để khớp với sidebar */
            border-bottom: 1px solid #7B2CBF33 !important;
        }

        /* Xử lý khoảng cách nội dung chính */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 2rem !important; /* Thêm chút khoảng trống để chữ không dính sát viền mới */
        }
        /* 🛠 BANNER GEMINI: DÍNH MÉP TRÊN VÀ NÉ SIDEBAR */
        div.gemini-banner {
            background: linear-gradient(135deg, #4285F4 0%, #9b72f3 35%, #d96570 70%, #f8e6e7 100%) !important;
            padding: 15px 10px !important;
            border-radius: 0 0 20px 20px !important;
            text-align: center !important;
            
            /* Kỹ thuật né Sidebar */
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            /* Sidebar mặc định của Streamlit rộng khoảng 21rem hoặc 300px */
            left: 336px !important; 
            
            z-index: 99 !important; /* Đủ cao để nổi nhưng không đè lên các thông báo hệ thống */
            margin: 0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }

        /* Điều chỉnh cho màn hình nhỏ/di động để Banner không bị lệch */
        @media (max-width: 768px) {
            div.gemini-banner {
                left: 0 !important; /* Trên điện thoại sidebar ẩn đi nên cho banner tràn ra */
            }
        }

        /* 🛠 XÓA THẺ SPAN DƯ THỪA */
        span.st-emotion-cache-gi0tri.et2r {
            display: none !important;
        }
        /* 🛠 KHÓA CHẶT THAO TÁC CLICK CHO NÚT CỤ THỂ */
        button.st-emotion-cache-1v1639i {
            pointer-events: none !important; /* Quan trọng: Chặn mọi sự kiện chuột/click */
            cursor: not-allowed !important;  /* Hiện biểu tượng vòng tròn gạch chéo khi rà chuột */
            opacity: 0.6 !important;         /* Làm mờ nút để người dùng biết là đang bị khóa */
            filter: grayscale(50%) !important; /* Làm nhạt màu tím đi một chút */
        }
        button.st-emotion-cache-pk19r {
            pointer-events: none !important; /* Chặn click chuột */
            cursor: not-allowed !important;  /* Hiện biểu tượng cấm */
            opacity: 0.5 !important;         /* Làm mờ để báo hiệu đang khóa */
            filter: saturate(0) !important;  /* Biến nút thành màu xám (mất màu tím) để dễ nhận biết */
        }       


         div.stAppToolbar.st-emotion-cache-15ec60s, /* Mã cache phổ biến của Toolbar */
        div[data-testid="stToolbar"],
        header[data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* Đẩy nội dung chính lên sát trên cùng sau khi ẩn Header */
        .main .block-container {
            padding-top: 1rem !important;
        }       

        .st-emotion-cache-1j22a0 {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }        

        /* Nhắm mục tiêu đích danh theo ID thầy đã cung cấp */
        input#text_input_6, 
        input#text_input_7 {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important; /* Ép chữ đen trên Chrome/Safari */
            border: 2px solid #7B2CBF55 !important;
            border-radius: 10px !important;
            opacity: 1 !important; /* Đảm bảo không bị mờ */
        }

        /* Giữ nguyên trạng thái khi thầy nhấn chuột vào để gõ (Focus) */
        input#text_input_6:focus, 
        input#text_input_7:focus {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border-color: #7B2CBF !important;
            box-shadow: 0 0 0 2px rgba(123, 44, 191, 0.2) !important;
            outline: none !important;
        }

        /* Xử lý trường hợp trình duyệt tự động điền (Autofill) cũng phải nền trắng */
        input#text_input_6:-webkit-autofill,
        input#text_input_6:-webkit-autofill:hover, 
        input#text_input_6:-webkit-autofill:focus,
        input#text_input_7:-webkit-autofill,
        input#text_input_7:-webkit-autofill:hover, 
        input#text_input_7:-webkit-autofill:focus {
            -webkit-box-shadow: 0 0 0px 1000px white inset !important;
            -webkit-text-fill-color: #000000 !important;
        }        

        button.st-emotion-cache-6ms01g {
            background-color: #7B2CBF !important;
            border: 1px solid #7B2CBF !important;
            border-radius: 10px !important;
            transition: all 0.3s ease-in-out !important;
            height: 3.5em !important;
            width: 100% !important;
        }

        /* Ép chữ trắng in đậm cho nội dung bên trong nút */
        button.st-emotion-cache-6ms01g p, 
        button.st-emotion-cache-6ms01g span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
        }

        /* 2. Trạng thái Hover (Di chuột): Nền xám, chữ đổi sang tím */
        button.st-emotion-cache-6ms01g:hover {
            background-color: #F0F2F6 !important; /* Màu xám nhạt */
            border: 1px solid #7B2CBF !important;
        }

        /* Khi hover, chữ phải chuyển sang màu tím thương hiệu */
        button.st-emotion-cache-6ms01g:hover p, 
        button.st-emotion-cache-6ms01g:hover span {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
        }        

         div.st-emotion-cache-467cry {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* Đảm bảo các thẻ con bên trong (p, li, span, h3) cũng phải màu đen */
        div.st-emotion-cache-467cry p, 
        div.st-emotion-cache-467cry li, 
        div.st-emotion-cache-467cry span,
        div.st-emotion-cache-467cry h3 {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 500 !important;
        }       

        h3#noi-dung-giao-an-chi-tiet {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
            text-align: center !important; /* Thêm dòng này nếu thầy muốn căn giữa cho đẹp */
            margin-bottom: 20px !important;
            border-bottom: 2px solid #7B2CBF33 !important; /* Tạo gạch chân mờ cho trang trọng */
            padding-bottom: 10px !important;
        }        

        [data-testid="stSidebar"] .stButton > button {
            background-color: #7B2CBF !important;
            border: 1px solid #7B2CBF !important;
            border-radius: 10px !important;
            transition: all 0.3s ease-in-out !important;
            width: 100% !important;
            height: 3.5em !important;
        }

        /* Ép chữ trắng in đậm cho nút tải file */
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
        }

        /* 2. Trạng thái Hover (Di chuột): Nền xám, chữ tím */
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #F0F2F6 !important; /* Màu xám nhạt của Streamlit */
            border: 1px solid #7B2CBF !important;
        }

        /* Khi di chuột, chữ và icon bên trong phải chuyển sang tím */
        [data-testid="stSidebar"] .stButton > button:hover p,
        [data-testid="stSidebar"] .stButton > button:hover span {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
        }        

        .sidebar-name-label {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
            font-size: 1.2rem !important;
            text-align: center !important;
            display: block !important; /* Cần thiết để lệnh căn giữa có tác dụng */
            margin: 10px auto !important;
            width: 100% !important;
        }

        /* Bổ sung cho thẻ h3 chung trong Sidebar để đảm bảo không sót mục nào */
        [data-testid="stSidebar"] h3 {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            text-align: center !important;
            font-weight: 900 !important;
        }

        /* 1. NỀN TRẮNG TOÀN APP */
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }

        /* 2. BANNER GEMINI */
        .gemini-banner {
            background: linear-gradient(135deg, #4285F4 0%, #9b72f3 35%, #d96570 70%, #f8e6e7 100%) !important;
            padding: 30px 15px !important;
            border-radius: 20px !important;
            text-align: center !important;
            margin-bottom: 30px !important;
            box-shadow: 0 8px 32px rgba(155, 114, 243, 0.2) !important;
        }
        .gemini-banner h1 {
            color: #FFFFFF !important; 
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 38px !important;
            font-weight: 900 !important;
        }

        /* 3. Ô NHẬP LIỆU (TEXTBOX, AREA, SELECTBOX) - ÉP NỀN TRẮNG TUYỆT ĐỐI */
        /* Sửa lỗi ô nhập liệu bị đen trong image_49e8dc.png */
        div[data-testid="stTextInput"] input, 
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stNumberInput"] input {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 2px solid #7B2CBF55 !important;
            border-radius: 10px !important;
        }

        /* 4. ĐỊNH DẠNG NÚT BẤM (BUTTON & FORM SUBMIT) */
        .stButton > button, 
        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stTabs"] .stButton > button {
            background-color: #7B2CBF !important;
            border: 1px solid #7B2CBF !important;
            border-radius: 10px !important;
            width: 100% !important; 
            height: 3.5em !important;
            transition: all 0.3s ease !important;
        }

        /* Cấp độ 2: ÉP CHỮ TRẮNG (Dùng bộ chọn cực mạnh để thắng màu tím của thẻ p) */
        .stButton > button p, 
        .stButton > button span,
        div[data-testid="stFormSubmitButton"] button p,
        div[data-testid="stFormSubmitButton"] button span,
        div[data-testid="stTabs"] .stButton > button p,
        div[data-testid="stTabs"] .stButton > button span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important; /* Quan trọng để thắng Dark Mode */
            font-weight: 900 !important;
            text-transform: uppercase !important;
            font-size: 16px !important;
        }

        /* 4.5. HIỆU ỨNG HOVER: NỀN XÁM CHỮ TÍM */
        .stButton > button:hover, 
        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stTabs"] .stButton > button:hover {
            background-color: #F0F2F6 !important;
            border: 1px solid #7B2CBF !important;
        }

        /* Khi di chuột vào thì chữ mới được phép chuyển sang tím */
        .stButton > button:hover p, 
        div[data-testid="stFormSubmitButton"] button:hover p,
        div[data-testid="stTabs"] .stButton > button:hover p {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
        }
                
        /* Nhắm mục tiêu chính xác vào các ô Input (Text và Number) */
        div[data-testid="stTextInput"] input, 
        div[data-testid="stNumberInput"] input {
            background-color: #FFFFFF !important; /* Nền trắng tinh khôi */
            color: #000000 !important;            /* Chữ đen rõ nét */
            -webkit-text-fill-color: #000000 !important; /* Fix lỗi chữ bị mờ trên một số trình duyệt */
            
            border: 2px solid #7B2CBF55 !important; /* Viền tím nhạt đồng bộ */
            border-radius: 10px !important;
            padding: 10px !important;
            font-weight: 500 !important;
        }

        /* Hiệu ứng khi thầy nhấn chuột vào ô để nhập (Focus) */
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            border-color: #7B2CBF !important; /* Viền tím đậm hơn khi đang nhập */
            box-shadow: 0 0 0 2px rgba(123, 44, 191, 0.2) !important;
            outline: none !important;
        }

        /* Đảm bảo Label (nhãn phía trên ô) vẫn giữ màu tím đặc trưng của thầy */
        div[data-testid="stWidgetLabel"] p {
            color: #7B2CBF !important;
            font-weight: bold !important;
        }

        /* 5. VĂN BẢN & TAB (MÀU TÍM CHỦ ĐẠO) */
        label, [data-testid="stWidgetLabel"] p {
            color: #7B2CBF !important;
            font-weight: bold !important;
        }

        /* Nhuộm tím thẻ p nhưng chừa các p trong nút ra */
        p:not(button p):not(div[data-testid="stTabs"] p) {
            color: #7B2CBF !important;
            font-weight: bold !important;
            -webkit-text-fill-color: #7B2CBF !important;
        }

        /* Chữ trên thanh Tab */
        div[data-testid="stTabs"] button p {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background-color: #7B2CBF !important;
        }

        /* 6. CARD ĐĂNG NHẬP */
        .login-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #7B2CBF33; text-align: center; overflow: hidden; }
        .login-title { color: #7B2CBF !important; font-weight: 900; font-size: 34px; }
        </style>
    """, unsafe_allow_html=True)

def render_login_logo(logo_64):
    """Hàm hiển thị logo tràn viền và nội dung chữ dưới card"""
    html_code = f'''
        <div class="login-card">
            <img src="data:image/png;base64,{logo_64}" class="login-banner">
            <div class="login-content-box" style="padding: 25px 15px; background: white;">
                <div class="login-title">SmartLesson AI</div>
                <div class="login-subtitle">Hệ thống hỗ trợ giảng dạy 4.0</div>
            </div>
        </div>
    '''
    st.markdown(html_code, unsafe_allow_html=True)