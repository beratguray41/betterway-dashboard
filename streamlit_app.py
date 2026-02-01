import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1) SAYFA AYARLARI
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Pro Dashboard", layout="wide", page_icon="🏎️")

# =========================================================
# 2) AUTH & LOGIN ALTYAPISI
# =========================================================
# Sadece şifre kontrolü için liste (Farklı şifrelere farklı firma yetkisi verilebilir)
PASSWORDS = {
    "betterway2026": "BetterWay Akademi",
    "betterway123": "Demo Firma"
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769924744/betterway_logo_arkaplan_xffybj.png"

def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        .stApp {{
            background: linear-gradient(rgba(10, 10, 15, 0.7), rgba(10, 10, 15, 0.9)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        
        header, footer, [data-testid="stSidebar"] {{ display: none !important; }}

        /* Login Kartı - Ultra Glassmorphism */
        [data-testid="stVerticalBlock"] > div:has(.login-card) {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 50px 40px !important;
            border-radius: 30px !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            max-width: 420px;
            margin: auto;
            margin-top: 12vh;
        }}
        
        div[data-testid="stElementContainer"]:has(.login-card) {{ display: none !important; }}
        
        .logo-container {{ text-align: center; margin-bottom: 35px; }}
        .logo-container img {{ width: 180px; filter: drop-shadow(0 0 15px rgba(255,255,255,0.2)); }}

        .login-header {{
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }}
        
        .login-subtitle {{
            color: #94a3b8;
            text-align: center;
            font-size: 14px;
            margin-bottom: 30px;
        }}

        /* Şifre Input Tasarımı */
        div[data-testid="stTextInput"] label {{ display: none !important; }}
        div[data-testid="stTextInput"] input {{
            background-color: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 15px !important;
            padding: 15px 20px !important;
            font-size: 16px !important;
            height: 55px !important;
            transition: all 0.3s ease;
            text-align: center;
            letter-spacing: 3px;
        }}
        
        div[data-testid="stTextInput"] input:focus {{
            border-color: #ff7b00 !important;
            background-color: rgba(255, 123, 0, 0.05) !important;
            box-shadow: 0 0 20px rgba(255, 123, 0, 0.2) !important;
        }}

        /* Giriş Butonu */
        div.stButton > button {{
            background: linear-gradient(135deg, #ff7b00 0%, #ff4500 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 0px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            width: 100% !important;
            height: 55px !important;
            margin-top: 20px !important;
            box-shadow: 0 10px 20px rgba(255, 69, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255, 69, 0, 0.4) !important;
            filter: brightness(1.1);
        }}

        .footer-text {{ 
            text-align: center; 
            margin-top: 35px; 
            font-size: 11px; 
            color: rgba(255,255,255,0.3); 
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        </style>
        """, unsafe_allow_html=True
    )

def login_screen():
    inject_login_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-header">Sistem Erişimi</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Lütfen size özel erişim şifresini giriniz.</div>', unsafe_allow_html=True)

        # Şifre girişi
        password = st.text_input("Şifre", type="password", placeholder="••••••••", label_visibility="collapsed")

        if st.button("SİSTEME GİRİŞ YAP"):
            if password in PASSWORDS:
                st.session_state.auth = True
                st.session_state.firm = PASSWORDS[password]
                st.rerun()
            else:
                st.error("Girdiğiniz şifre hatalı veya süresi dolmuş!")

        st.markdown('<div class="footer-text">BetterWay Intelligence Secure Access © 2026</div>', unsafe_allow_html=True)

# --- AUTH KONTROL ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# =========================================================
# 3) DASHBOARD (ANA İÇERİK)
# =========================================================

# --- PREMIUM MODERN CSS (SaaS Style) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Login temasını dashboard'da temizle */
    .stApp {
        background: radial-gradient(circle at top right, #1d1f27, #0f1115) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #161920;
        border-right: 1px solid #2d3139;
        display: flex !important;
    }
    
    header { display: block !important; }

    /* Modern Kart Yapısı */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(230, 57, 70, 0.4);
        background: rgba(255, 255, 255, 0.05);
    }

    /* KPI Metrikleri */
    .kpi-title { color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { color: #ffffff; font-size: 32px; font-weight: 700; margin-top: 8px; }
    .kpi-trend { font-size: 12px; margin-top: 4px; }
    
    /* Sürücü Profil Kartı */
    .hero-profile {
        background: linear-gradient(135deg, #1e222d 0%, #161920 100%);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid #2d3139;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    /* Skor Dairesi */
    .score-ring {
        background: transparent;
        border: 4px solid #e63946;
        color: #e63946;
        width: 100px; height: 100px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 32px; font-weight: 800;
        box-shadow: 0 0 20px rgba(230, 57, 70, 0.2);
    }

    /* Durum Kutuları */
    .status-alert {
        background: rgba(230, 57, 70, 0.1);
        color: #ff4d4d;
        padding: 12px 20px;
        border-radius: 12px;
        border-left: 4px solid #e63946;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .status-success {
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        padding: 12px 20px;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        font-weight: 500;
    }

    .download-btn {
        background: #e63946;
        color: white !important;
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    hr { border: 0; border-top: 1px solid #2d3139; margin: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ ÇEKME ---
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
GENEL_GID = "0"
SURUCU_GID = "395204791"
HATA_OZETI_GID = "2078081831"

@st.cache_data(ttl=300)
def load_data(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except: return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# --- SIDEBAR NAVİGASYON ---
with st.sidebar:
    st.image("https://res.cloudinary.com/dkdgj03sl/image/upload/v1769850715/Black_and_Red_Car_Animated_Logo-8_ebzsvo.png", width=180)
    
    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:12px; margin-bottom:20px; border:1px solid rgba(255,255,255,0.1);">
            <div style="color:#94a3b8; font-size:10px; font-weight:700; letter-spacing:1px;">AKTİF KURUM</div>
            <div style="color:white; font-weight:700; font-size:14px; margin-top:4px;">{st.session_state.get('firm', 'Müşteri')}</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "NAVİGASYON",
        options=["🏠 Genel Bakış", "🔍 Sürücü Sorgula"],
        index=0
    )
    
    if menu == "🔍 Sürücü Sorgula":
        if not df_surucu.empty:
            ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
            secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)
        else: secilen_surucu = "Seçiniz..."
    else: secilen_surucu = "Seçiniz..."

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Güvenli Çıkış", use_container_width=True):
        st.session_state.auth = False
        st.rerun()

    st.markdown("---")
    st.caption("BetterWay Intelligence v6.0")

# --- DURUM 1: SÜRÜCÜ SORGULAMA ---
if menu == "🔍 Sürücü Sorgula" and secilen_surucu != "Seçiniz...":
    row = df_surucu[df_surucu['Sürücü Adı'] == secilen_surucu].iloc[0]
    
    st.markdown(f"""
        <div class="hero-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color:#e63946; font-weight:700; font-size:12px; letter-spacing:2px;">PERSONEL ANALİZ KARTI</span>
                    <h1 style="margin:8px 0; font-size:42px; color:white;">{row['Sürücü Adı']}</h1>
                    <p style="color:#94a3b8; font-size:18px;">
                        <span style="margin-right:20px;">📍 {row.get('EĞİTİM YERİ', '-')}</span>
                        <span>🎓 {row.get('EĞİTİM TÜRÜ', '-')}</span>
                    </p>
                </div>
                <div class="score-ring">{row.get('SÜRÜŞ PUANI', '0')}</div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top:40px;">
                <div class="glass-card">
                    <h4 style="margin-bottom:15px; color:#e63946;">📊 Performans Analizi</h4>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Ön Test Skoru:</b> {row.get('EĞİTİM ÖNCESİ TEST', '-')}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Son Test Skoru:</b> {row.get('EĞİTİM SONRASI TEST', '-')}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Eğitim Tarihi:</b> {row.get('EĞİTİM TARİHİ', '-')}</p>
                </div>
                <div class="glass-card">
                    <h4 style="margin-bottom:15px; color:#e63946;">⚠️ Gelişim Alanları</h4>
                    <p style="color:#cbd5e1; line-height:1.6;">{row.get('ZAYIF YÖNLER', 'Kritik bir zayıf yön tespit edilmemiştir.')}</p>
                </div>
            </div>
            <div style="margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; display:flex; justify-content:space-between;">
                <span style="color:#94a3b8;">📅 Sertifika Geçerlilik: <b>{row.get('EĞİTİM GEÇERLİLİK TARİHİ', '-')}</b></span>
                <span style="color:#e63946; font-weight:700;">⏳ {row.get('EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?', '-')} GÜN KALDI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- DURUM 2: ANASAYFA ---
else:
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        v = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{v}</div><div class="kpi-trend" style="color:#22c55e;">▲ Aktif</div></div>', unsafe_allow_html=True)
    with k2:
        ise = pd.to_numeric(df_genel['İŞE ALIM'], errors='coerce').sum() if 'İŞE ALIM' in df_genel.columns else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">İşe Alım</div><div class="kpi-value">{int(ise)}</div><div class="kpi-trend" style="color:#e63946;">● Akademi Çıktısı</div></div>', unsafe_allow_html=True)
    with k3:
        k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
        k_sayi = (k_gun < 30).sum() if not df_surucu.empty else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{k_sayi}</div><div class="kpi-trend" style="color:#94a3b8;">⏱️ < 30 Gün</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel)}</div><div class="kpi-trend" style="color:#94a3b8;">📋 Toplam Oturum</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])
    
    with col_l:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>⚠️ Sık Rastlanan Hatalar</h3>", unsafe_allow_html=True)
        if not df_hata.empty:
            df_h_plot = df_hata.sort_values(by=df_hata.columns[1], ascending=True).tail(8)
            fig = px.bar(df_h_plot, x=df_hata.columns[1], y=df_hata.columns[0], orientation='h', template="plotly_dark", color_discrete_sequence=['#e63946'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=350)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_r:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>🗓️ Yenileme Takvimi</h3>", unsafe_allow_html=True)
        if not df_surucu.empty:
            df_t = df_surucu.copy()
            df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='kg', ascending=True)
            crit_df = df_t[df_t['kg'] < 30]
            if not crit_df.empty:
                for _, r in crit_df.head(5).iterrows():
                    st.markdown(f"""<div class="status-alert">🚨 {r['Sürücü Adı']} - <span style="float:right;">{int(r['kg'])} Gün</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-success">✅ Tüm personel süreleri güncel.</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; margin-bottom:25px;'>📂 Eğitim Arşivi</h3>", unsafe_allow_html=True)
    
    if not df_genel.empty:
        st.dataframe(df_genel, use_container_width=True, hide_index=True)

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
