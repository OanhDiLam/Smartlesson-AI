import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. VÔ HIỆU HÓA CÁC NÚT MẶC ĐỊNH */
        .stDeployButton, [data-testid="stAppToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
        }

        /* 2. SIDEBAR: LOGO TO KHÍT VÀ TÊN GV TÁCH BIỆT */
        .logo-container {
            width: 100%;
            margin: 0;
            padding: 0;
        }
        
        .sidebar-img {
            width: 100% !important;
            max-width: 259px !important; 
            height: auto !important;
            border-radius: 8px;
            display: block;
        }

        .sidebar-name-label {
            font-family: 'Times New Roman', Times, serif;
            color: #7B2CBF !important;
            font-size: 0.9rem !important;
            font-weight: bold !important;
            text-align: center;
            margin-top: 12px !important;
            margin-bottom: 20px !important;
            display: block;
            width: 100%;
        }

        /* 3. MÀU TÍM ĐẬM VÀ IN ĐẬM */
        html, body, [data-testid="stWidgetLabel"] p, label, .stMarkdown p {
            color: #7B2CBF !important;
            font-weight: bold !important;
        }

        /* 4. Ô NHẬP LIỆU: VIỀN TÍM, CHỮ ĐEN */
        .stTextInput input, .stTextArea textarea {
            color: black !important;
            border: 2px solid #7B2CBF !important;
            border-radius: 8px !important;
            background-color: white !important;
            font-weight: normal !important;
        }

        /* 5. Ô CHỌN (SELECTBOX) */
        div[data-baseweb="select"] > div {
            border: 2px solid #7B2CBF !important;
            border-radius: 8px !important;
            background-color: white !important;
        }
        
        div[data-baseweb="select"] span, div[data-baseweb="select"] div {
            color: black !important;
            font-weight: normal !important;
        }

        /* 6. BANNER TIÊU ĐỀ CHÍNH */
        .banner-top {
            background: linear-gradient(135deg, #10B981, #3B82F6);
            padding: 30px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px;
        }
        .banner-top h1 { color: white !important; font-size: 2.2rem !important; margin: 0; }

        .stApp { background-color: #F1F5F9; }
        </style>
    """, unsafe_allow_html=True)