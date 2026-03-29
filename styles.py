import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        .app-auth-body {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            text-align: center !important;
        }

        .app-auth-body .app-auth-title,
        .app-auth-body .app-auth-subtitle,
        .app-auth-body div {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
        }

        [data-testid="collapsedControl"] {
            position: fixed !important;
            top: 18px !important;
            left: 18px !important;
            z-index: 1001 !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        [data-testid="collapsedControl"] button {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 48px !important;
            height: 48px !important;
            min-height: 48px !important;
            padding: 0 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.35) !important;
            background: linear-gradient(135deg, #7B2CBF 0%, #9D4EDD 100%) !important;
            box-shadow: 0 10px 24px rgba(123, 44, 191, 0.25) !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="collapsedControl"] button:hover {
            transform: translateY(-1px) scale(1.03) !important;
            box-shadow: 0 14px 28px rgba(123, 44, 191, 0.32) !important;
            background: linear-gradient(135deg, #6A1FB0 0%, #8F3FE0 100%) !important;
        }

        [data-testid="collapsedControl"] button p,
        [data-testid="collapsedControl"] button span,
        [data-testid="collapsedControl"] svg {
            display: none !important;
        }

        [data-testid="collapsedControl"] button::before {
            content: "☰";
            color: #FFFFFF !important;
            font-size: 24px !important;
            line-height: 1 !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] {
            min-width: 350px !important;
            max-width: 350px !important;
            border-right: 2px solid #7B2CBF33 !important;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05) !important;
        }

        .main .block-container {
            padding-top: 4rem !important;
            padding-left: 2rem !important;
        }

        div.gemini-banner {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            left: 350px !important;
            z-index: 99 !important;
            margin: 0 !important;
            padding: 15px 10px !important;
            text-align: center !important;
            border-radius: 0 0 20px 20px !important;
            border-bottom: 1px solid #7B2CBF33 !important;
            background: linear-gradient(135deg, #4285F4 0%, #9B72F3 35%, #D96570 70%, #F8E6E7 100%) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }

        @media (max-width: 768px) {
            div.gemini-banner {
                left: 0 !important;
            }
        }

        div[data-testid="stToolbar"] {
            display: none !important;
            visibility: hidden !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 64px !important;
            min-height: 64px !important;
        }

        h3#noi-dung-giao-an-chi-tiet {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
            text-align: center !important;
            margin-bottom: 20px !important;
            padding-bottom: 10px !important;
            border-bottom: 2px solid #7B2CBF33 !important;
        }

        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button,
        .stButton > button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stTabs"] .stButton > button {
            width: 100% !important;
            height: 3.5em !important;
            border-radius: 10px !important;
            border: 1px solid #7B2CBF !important;
            background-color: #7B2CBF !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button p,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button span,
        .stButton > button p,
        .stButton > button span,
        div[data-testid="stDownloadButton"] button p,
        div[data-testid="stDownloadButton"] button span,
        div[data-testid="stFormSubmitButton"] button p,
        div[data-testid="stFormSubmitButton"] button span,
        div[data-testid="stTabs"] .stButton > button p,
        div[data-testid="stTabs"] .stButton > button span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
            font-size: 16px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button:hover,
        .stButton > button:hover,
        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stTabs"] .stButton > button:hover {
            background-color: #F0F2F6 !important;
            border: 1px solid #7B2CBF !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover p,
        [data-testid="stSidebar"] .stButton > button:hover span,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button:hover p,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button:hover span,
        .stButton > button:hover p,
        div[data-testid="stDownloadButton"] button:hover p,
        div[data-testid="stFormSubmitButton"] button:hover p,
        div[data-testid="stTabs"] .stButton > button:hover p {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
        }

        .app-sidebar-logo {
            margin: 0 auto 10px auto !important;
            text-align: center !important;
        }

        .app-sidebar-logo-img {
            width: 112px !important;
            height: 112px !important;
            object-fit: cover !important;
            border-radius: 50% !important;
            border: 4px solid rgba(123, 44, 191, 0.16) !important;
            box-shadow: 0 10px 24px rgba(123, 44, 191, 0.16) !important;
            background: #FFFFFF !important;
        }

        .app-sidebar-name,
        [data-testid="stSidebar"] h3 {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
            text-align: center !important;
        }

        .app-sidebar-name {
            display: block !important;
            width: 100% !important;
            margin: 10px auto !important;
            font-size: 1.2rem !important;
        }

        .stApp,
        [data-testid="stSidebar"],
        [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }

        .gemini-banner {
            padding: 30px 15px !important;
            margin-bottom: 30px !important;
            border-radius: 20px !important;
            text-align: center !important;
            background: linear-gradient(135deg, #4285F4 0%, #9B72F3 35%, #D96570 70%, #F8E6E7 100%) !important;
            box-shadow: 0 8px 32px rgba(155, 114, 243, 0.2) !important;
        }

        .gemini-banner h1 {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 38px !important;
            font-weight: 900 !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stNumberInput"] input {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #FFFFFF !important;
            border: 2px solid #7B2CBF55 !important;
            border-radius: 10px !important;
            padding: 10px !important;
            font-weight: 500 !important;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            border-color: #7B2CBF !important;
            box-shadow: 0 0 0 2px rgba(123, 44, 191, 0.2) !important;
            outline: none !important;
        }

        label,
        [data-testid="stWidgetLabel"] p {
            color: #7B2CBF !important;
            font-weight: bold !important;
        }

        p:not(button p):not(div[data-testid="stTabs"] p) {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: bold !important;
        }

        div[data-testid="stTabs"] button p {
            color: #7B2CBF !important;
            -webkit-text-fill-color: #7B2CBF !important;
            font-weight: 900 !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background-color: #7B2CBF !important;
        }

        .app-auth-card {
            overflow: hidden;
            text-align: center;
            background: #FFFFFF;
            border-radius: 20px;
            border: 1px solid #7B2CBF33;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .app-auth-title {
            color: #7B2CBF !important;
            font-size: 34px;
            font-weight: 900;
        }

        div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"][data-stale="false"] {
            border-radius: 22px !important;
        }

        .community-feed-card {
            padding: 4px 2px 6px 2px;
        }

        .community-feed-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .community-feed-avatar,
        .community-comment-avatar {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #cbd5e1;
            color: #1e3a8a;
            font-size: 1rem;
            font-weight: 900;
            flex-shrink: 0;
            overflow: hidden;
        }

        .community-feed-avatar-img,
        .community-comment-avatar-img {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            object-fit: cover;
            border: 1px solid #cbd5e1;
            background: #ffffff;
            flex-shrink: 0;
        }

        .community-feed-header-text {
            min-width: 0;
        }

        .community-feed-author {
            color: #111827;
            font-size: 1rem;
            font-weight: 900;
            line-height: 1.2;
        }

        .community-feed-meta {
            color: #6b7280;
            font-size: 0.83rem;
            font-weight: 600;
            margin-top: 2px;
        }

        .community-feed-title {
            color: #111827;
            font-size: 1.22rem;
            font-weight: 900;
            line-height: 1.35;
            margin-bottom: 10px;
        }

        .community-feed-caption {
            color: #374151;
            font-size: 0.98rem;
            font-weight: 500;
            line-height: 1.7;
            margin-bottom: 14px;
        }

        .community-feed-file {
            padding: 12px 14px;
            border-radius: 16px;
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            color: #374151;
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .community-feed-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }

        .community-feed-tag {
            display: inline-flex;
            align-items: center;
            padding: 7px 12px;
            border-radius: 999px;
            background: #eff6ff;
            border: 1px solid #dbeafe;
            color: #1d4ed8;
            font-size: 0.84rem;
            font-weight: 800;
        }

        .community-feed-stats {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            padding-top: 12px;
            margin-top: 2px;
            border-top: 1px solid #e5e7eb;
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .community-comment-content {
            flex: 1;
            padding: 10px 14px;
            border-radius: 18px;
            background: #f3f4f6;
            min-width: 0;
        }

        .community-comment-content-reply {
            background: #eef2f7;
        }

        .community-comment-author {
            color: #111827;
            font-size: 0.95rem;
            font-weight: 900;
            margin-bottom: 3px;
        }

        .community-comment-time {
            color: #6b7280;
            font-size: 0.76rem;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .community-comment-body {
            color: #374151;
            font-weight: 500;
            line-height: 1.58;
        }

        div[data-testid="stContainer"] {
            background: #ffffff;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04) !important;
        }

        div[data-testid="stContainer"] .stButton > button,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button {
            width: auto !important;
            height: 2.15em !important;
            min-height: 2.15em !important;
            max-width: fit-content !important;
            padding: 0.1rem 0.65rem !important;
            border-radius: 999px !important;
            font-size: 0.8rem !important;
            border: 1px solid #d1d5db !important;
            background: #f3f4f6 !important;
            color: #374151 !important;
        }

        div[data-testid="stContainer"] .stButton > button p,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button p,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button p,
        div[data-testid="stContainer"] .stButton > button span,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button span,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button span {
            color: #374151 !important;
            -webkit-text-fill-color: #374151 !important;
            font-size: 10.5px !important;
            font-weight: 700 !important;
            text-transform: none !important;
        }

        div[data-testid="stContainer"] .stButton > button:hover,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button:hover {
            background: #e5e7eb !important;
            border-color: #cbd5e1 !important;
        }

        div[data-testid="stContainer"] .stButton > button:hover p,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button:hover p,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button:hover p,
        div[data-testid="stContainer"] .stButton > button:hover span,
        div[data-testid="stContainer"] div[data-testid="stDownloadButton"] > button:hover span,
        div[data-testid="stContainer"] div[data-testid="stFormSubmitButton"] > button:hover span {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
        }

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stFormSubmitButton"] > button,
        .stButton > button {
            box-shadow: none !important;
        }

        @media (max-width: 768px) {
            .community-comment-reply {
                margin-left: 10px;
            }

            .community-feed-stats {
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_logo(logo_64):
    html_code = f'''
        <div class="app-auth-card">
            <img src="data:image/png;base64,{logo_64}" class="app-auth-banner">
            <div class="app-auth-body" style="padding: 25px 15px; background: white;">
                <div class="app-auth-title">SmartLesson AI</div>
                <div class="app-auth-subtitle">Hệ thống hỗ trợ giảng dạy 4.0</div>
            </div>
        </div>
    '''
    st.markdown(html_code, unsafe_allow_html=True)
