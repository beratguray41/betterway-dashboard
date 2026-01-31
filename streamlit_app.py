import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 0) SAYFA AYARLARI
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Giriş", layout="wide", page_icon="🏎️")

# =========================================================
# 1) CONFIG & AUTH
# =========================================================
VALID_USERS = {
    "admin": {"password": "betterway2026", "firm": "BetterWay Akademi"},
    "demo@betterway.com": {"password": "betterway123", "firm": "Demo Firma"},
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://assets.softr-files.com/applications/0d7745a6-552f-4fe6-a9dc-29570cb0f7b7/assets/a0e627e0-5a38-4798-9b07-b1beca18b0a4.png"

# =========================================================
# LOGIN CSS (TAM FIXLİ)
# =========================================================
def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.3)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            overflow: hidden !important;
        }}

        header, footer, [data-testid="stSidebar"] {{ 
            visibility: hidden !important; 
            display: none !important; 
        }}

        [data-testid="stVerticalBlock"] > div:has(.login-box) {{
            background: rgba(255, 255, 255, 0.98);
            padding: 30px 40px !important;
            border-radius: 30px !important;
            box-shadow: 0 40px 100px rgba(0,0,0,0.3) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.5);
            max-width: 460px;
            margin: auto;
            margin-top: 10vh;
        }}

        /* LABEL FIX */
        .login-label {{
            color: #1e293b;
            font-weight: 600;
            font-size: 14px;
            padding-top: 10px;
            text-align: right;
            white-space: nowrap;
            line-height: 1;
        }}

        /* INPUT FIX */
        div[data-testid="stTextInput"] input {{
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            background: #f8fafc !important;
            height: 2.8rem !important;
            color: #0f172a !important;
            padding-right: 3rem !important;
        }}

        div[data-testid="stTextInput"] button {{
            min-width: 44px !important;
            width: 44px !important;
            height: 44px !important;
            border-radius: 10px !important;
        }}

        /* BUTTON */
        div.stButton > button {{
            background: #ff7b00 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 700 !important;
            height: 3rem !important;
            width: 100% !important;
            margin-top: 15px !important;
            transition: 0.3s all !important;
            box-shadow: 0 4px 15px rgba(255, 123, 0, 0.2) !important;
        }}

        div.stButton > button:hover {{
            background: #e66f00 !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 123, 0, 0.3) !important;
        }}

        .login-footer {{
            text-align: center;
            font-size: 10px;
            color: #94a3b8;
            margin-top: 20px;
            letter-spacing: 1px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# LOGIN SCREEN
# =========================================================
def login_screen():
    inject_login_css()
    
    if "auth" not in st.session_state:
        st.session_state.auth = False

    _, mid, _ = st.columns([1, 1.4, 1])
    
    with mid:
        st.markdown('<div class="login-box"></div>', unsafe_allow_html=True)
        st.image(LOGO_URL, width=200)
        st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Kullanıcı
        l1, i1 = st.columns([0.65, 1])
        with l1:
            st.markdown('<p class="login-label">Kullanıcı Adı:</p>', unsafe_allow_html=True)
        with i1:
            username = st.text_input("U", placeholder="E-posta veya kullanıcı adı", label_visibility="collapsed")
        
        # Şifre
        l2, i2 = st.columns([0.65, 1])
        with l2:
            st.markdown('<p class="login-label">Şifre:</p>', unsafe_allow_html=True)
        with i2:
            password = st.text_input("P", type="password", placeholder="Şifreniz", label_visibility="collapsed")
        
        if st.button("SİSTEME GİRİŞ YAP"):
            u = username.strip().lower()
            if u in VALID_USERS and VALID_USERS[u]["password"] == password:
                st.session_state.auth = True
                st.session_state.user = u
                st.session_state.firm = VALID_USERS[u]["firm"]
                st.rerun()
            else:
                st.error("Giriş bilgileri hatalı!")
        
        st.markdown('<p class="login-footer">BETTERWAY AKADEMİ GÜVENLİ ERİŞİM © 2026</p>', unsafe_allow_html=True)

# =========================================================
# APP START
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

st.success("Giriş başarılı, dashboard buradan devam eder...")
