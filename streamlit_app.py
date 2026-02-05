import streamlit as st
import pandas as pd
import plotly.express as px
import time
import extra_streamlit_components as stx  # pip install extra-streamlit-components
import re
import html

# =========================================================
# 0) SAYFA AYARLARI
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Pro Dashboard", layout="wide", page_icon="🏎️")

# =========================================================
# FORCE DARK MODE (Login background'ını ezmeden)
# =========================================================
st.markdown("""
<style>
:root, html, body { color-scheme: dark !important; }
:root{
  --bg:#0f1115; --panel:#161920; --panel2:#1e222d;
  --text:#e2e8f0; --muted:#94a3b8; --border:#2d3139;
}
/* .stApp background'ını burada ZORLAMIYORUZ (login bg için) */

section[data-testid="stSidebar"]{
  background: var(--panel) !important;
  border-right: 1px solid var(--border) !important;
}

div, span, p, label, h1,h2,h3,h4,h5,h6 { color: var(--text); }

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div,
div[data-testid="stDateInput"] > div{
  background: rgba(255,255,255,0.06) !important;
  color: var(--text) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  border-radius: 12px !important;
}

div[role="listbox"]{
  background:#11141a !important;
  border:1px solid rgba(255,255,255,0.14) !important;
}
div[role="option"]{ color: var(--text) !important; }

details, summary{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px !important;
}

.js-plotly-plot, .plot-container{ background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 1) FİRMA KONFİG (ŞİFRE -> SHEET + AYARLAR)
# =========================================================
FIRMS = {
    # KARINCA
    "Karınca2025.": {
        "name": "KARINCA LOJİSTİK",
        "sheet_id": "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU",
        "has_ise_alim": True,
        "gids": {"GENEL": "0", "SURUCU": "395204791", "HATA": "2078081831"},
    },
    # ACAPET
    "Acapet2025..": {  # <- şifreyi buradan değiştir
        "name": "ACAPET LOJİSTİK",
        "sheet_id": "1K3MBqT2I7I_a_mDhByXX1G1kMVp_VpWXqzyHBiqplLY",
        "has_ise_alim": False,  # ACAPET’te İŞE ALIM yok
        "gids": {"GENEL": "0", "SURUCU": "395204791", "HATA": "2078081831"},
    },
    # DEMO (opsiyonel)
    "betterway123": {
        "name": "Demo Firma",
        "sheet_id": "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU",
        "has_ise_alim": True,
        "gids": {"GENEL": "0", "SURUCU": "395204791", "HATA": "2078081831"},
    },
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769926229/betterway_logo_arkaplan_2_jpdrgg.png"

# =========================================================
# 2) COOKIE MANAGER
# =========================================================
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# =========================================================
# 3) PERSONEL SAYFASI KİRLİ HTML TEMİZLİĞİ (FIX)
# =========================================================
_TAG_RE = re.compile(r"<[^>]+>")

def clean_cell(val, default="-"):
    s = "" if val is None else str(val)
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not s or s.lower() == "nan":
        s = default
    # tag temizle (kart HTML’i hücreye yapıştıysa DOM’u kırmasın)
    s = _TAG_RE.sub("", s)
    # whitespace toparla
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s

def safe_text(val, default="-"):
    return html.escape(clean_cell(val, default=default))

def safe_multiline(val, default="Kritik bir zayıf yön tespit edilmemiştir."):
    s = clean_cell(val, default=default)
    return html.escape(s).replace("\n", "<br/>")

# =========================================================
# 4) LOADING (SPLASH)
# =========================================================
def show_loading_animation(placeholder):
    loading_css = f"""
    <style>
        .loading-container {{
            position: fixed; top: 0; left: 0;
            width: 100vw; height: 100vh;
            background-color: #0f1115;
            z-index: 99999;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }}
        .loading-logo {{
            width: 180px;
            margin-bottom: 30px;
            animation: pulse-animation 2s infinite ease-in-out;
            filter: drop-shadow(0 0 20px rgba(255, 69, 0, 0.4));
        }}
        @keyframes pulse-animation {{
            0% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.05); opacity: 1; filter: drop-shadow(0 0 30px rgba(255, 69, 0, 0.6)); }}
            100% {{ transform: scale(1); opacity: 0.8; }}
        }}
        .loader-bar-container {{
            width: 250px; height: 4px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 2px; overflow: hidden; position: relative;
        }}
        .loader-bar {{
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, #e63946, transparent);
            position: absolute;
            animation: loading-swipe 1.5s infinite linear;
            transform: translateX(-100%);
        }}
        @keyframes loading-swipe {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        .loading-text {{
            color: #94a3b8;
            margin-top: 15px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            letter-spacing: 2px;
            text-transform: uppercase;
            animation: fade-text 2s infinite;
        }}
        @keyframes fade-text {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}
    </style>
    <div class="loading-container">
        <img src="{LOGO_URL}" class="loading-logo">
        <div class="loader-bar-container"><div class="loader-bar"></div></div>
        <div class="loading-text">Güvenli Bağlantı Kuruluyor...</div>
    </div>
    """
    placeholder.markdown(loading_css, unsafe_allow_html=True)

# =========================================================
# 5) LOGIN CSS + SCREEN
# =========================================================
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

        [data-testid="stVerticalBlock"] > div:has(.login-card) {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 60px 60px !important;
            border-radius: 24px !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.15);
            max-width: 580px;
            margin: auto;
            margin-top: 10vh;
        }}

        div[data-testid="stElementContainer"]:has(.login-card) {{ display: none !important; }}

        .logo-container {{ text-align: center; margin-bottom: 30px; }}
        .logo-container img {{ width: 220px; filter: drop-shadow(0 0 25px rgba(255,255,255,0.15)); }}

        .login-header {{
            color: white;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}

        .login-desc-1 {{
            color: #e2e8f0;
            text-align: center;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
            font-weight: 500;
        }}

        .login-desc-2 {{
            color: #94a3b8;
            text-align: center;
            font-size: 13px;
            margin-bottom: 40px;
            font-weight: 400;
        }}

        div[data-testid="stTextInput"] label {{ display: none !important; }}

        div[data-testid="stTextInput"] input {{
            background-color: rgba(255, 255, 255, 0.07) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border-radius: 16px !important;
            padding: 0 25px !important;
            font-size: 20px !important;
            height: 65px !important;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            text-align: center;
            letter-spacing: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        div[data-testid="stTextInput"] input:focus {{
            border-color: #ff7b00 !important;
            background-color: rgba(255, 255, 255, 0.12) !important;
            box-shadow: 0 0 25px rgba(255, 123, 0, 0.3), inset 0 0 0 1px rgba(255, 123, 0, 0.1) !important;
            transform: scale(1.02);
            letter-spacing: 8px;
        }}

        div[data-testid="stTextInput"] input::placeholder {{
            color: rgba(255, 255, 255, 0.4);
        }}

        div.stButton {{ width: 100%; padding-top: 20px; }}

        div.stButton > button {{
            background: linear-gradient(135deg, #ff7b00 0%, #ff4500 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0px !important;
            font-size: 17px !important;
            font-weight: 700 !important;
            width: 100% !important;
            height: 60px !important;
            box-shadow: 0 10px 30px rgba(255, 69, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        div.stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(255, 69, 0, 0.5) !important;
            filter: brightness(1.1);
        }}

        .footer-text {{
            text-align: center;
            margin-top: 45px;
            font-size: 11px;
            color: rgba(255,255,255,0.3);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def login_screen():
    inject_login_css()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-header">Sisteme Giriş</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="login-desc-1">
                BetterWay Akademi yönetim paneline erişmek için lütfen yetkili şifrenizi giriniz.
            </div>
            <div class="login-desc-2">
                Oturumunuz bu cihazda güvenli bir şekilde saklanacaktır.
            </div>
        """, unsafe_allow_html=True)

        password = st.text_input("Şifre", type="password", placeholder="••••••••", label_visibility="collapsed")

        if st.button("GÜVENLİ GİRİŞ YAP", use_container_width=True):
            if password in FIRMS:
                cfg = FIRMS[password]
                st.session_state.auth = True
                st.session_state.firm = cfg["name"]
                st.session_state.sheet_id = cfg["sheet_id"]
                st.session_state.has_ise_alim = bool(cfg.get("has_ise_alim", False))
                st.session_state.gids = cfg.get("gids", {})
                cookie_manager.set("betterway_auth_token", password, key="set_auth_token", expires_at=None)
                st.success("Giriş başarılı, yönlendiriliyorsunuz...")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("Hatalı şifre!")

        st.markdown('<div class="footer-text">BetterWay Intelligence Secure Access © 2026</div>', unsafe_allow_html=True)

# =========================================================
# 6) AUTH & COOKIE
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    loading_placeholder = st.empty()
    show_loading_animation(loading_placeholder)

    time.sleep(1.2)
    cookie_val = cookie_manager.get("betterway_auth_token")

    if cookie_val and cookie_val in FIRMS:
        cfg = FIRMS[cookie_val]
        st.session_state.auth = True
        st.session_state.firm = cfg["name"]
        st.session_state.sheet_id = cfg["sheet_id"]
        st.session_state.has_ise_alim = bool(cfg.get("has_ise_alim", False))
        st.session_state.gids = cfg.get("gids", {})
        loading_placeholder.empty()
        st.rerun()
    else:
        loading_placeholder.empty()
        login_screen()
        st.stop()

# =========================================================
# 7) DASHBOARD CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: #0f1115;
}

.stApp {
  background: radial-gradient(circle at top right, #1d1f27, #0f1115) !important;
}

[data-testid="stSidebar"]{
  background-color:#161920;
  border-right: 1px solid #2d3139;
  display:flex !important;
}
header { display:block !important; }

.glass-card{
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}
.glass-card:hover{
  border-color: rgba(230, 57, 70, 0.4);
  background: rgba(255, 255, 255, 0.05);
}
.kpi-title{ color:#94a3b8; font-size:14px; font-weight:600; text-transform:uppercase; letter-spacing:1px; }
.kpi-value{ color:#fff; font-size:32px; font-weight:700; margin-top:8px; }
.kpi-trend{ font-size:12px; margin-top:4px; }

.hero-profile{
  background: linear-gradient(135deg, #1e222d 0%, #161920 100%);
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #2d3139;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
}
.hero-profile::after{
  content:"";
  position:absolute; top:-50px; right:-50px;
  width:150px; height:150px;
  background: rgba(230, 57, 70, 0.1);
  border-radius:50%; blur:60px;
}
.score-ring{
  background: transparent;
  border: 4px solid #e63946;
  color: #e63946;
  width:100px; height:100px;
  border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:32px; font-weight:800;
  box-shadow: 0 0 20px rgba(230, 57, 70, 0.2);
}

.status-alert{
  background: rgba(230, 57, 70, 0.1);
  color: #ff4d4d;
  padding: 12px 20px;
  border-radius: 12px;
  border-left: 4px solid #e63946;
  font-weight: 500;
  margin-bottom: 10px;
}
.status-success{
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  padding: 12px 20px;
  border-radius: 12px;
  border-left: 4px solid #22c55e;
  font-weight: 500;
}

.download-btn{
  background:#e63946;
  color:white !important;
  padding:10px 20px;
  border-radius:10px;
  text-decoration:none;
  font-size:14px;
  font-weight:700;
  transition:0.3s all ease;
  box-shadow:0 4px 12px rgba(230, 57, 70, 0.3);
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  border:none;
}
.download-btn:hover{
  background:#ff4d4d;
  transform: translateY(-2px);
  box-shadow:0 6px 20px rgba(230, 57, 70, 0.5);
  color:white !important;
}

.archive-header{
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}
hr{ border:0; border-top:1px solid #2d3139; margin:30px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 8) VERİ ÇEKME
# =========================================================
SHEET_ID = st.session_state.get("sheet_id")
HAS_ISE_ALIM = bool(st.session_state.get("has_ise_alim", False))
GIDS = st.session_state.get("gids", {})

GENEL_GID = str(GIDS.get("GENEL", "0"))
SURUCU_GID = str(GIDS.get("SURUCU", "395204791"))
HATA_OZETI_GID = str(GIDS.get("HATA", "2078081831"))

@st.cache_data(ttl=30)
def load_data(sheet_id: str, gid: str) -> pd.DataFrame:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return pd.DataFrame()

df_genel = load_data(SHEET_ID, GENEL_GID)
df_surucu = load_data(SHEET_ID, SURUCU_GID)
df_hata = load_data(SHEET_ID, HATA_OZETI_GID)

# =========================================================
# 9) SIDEBAR
# =========================================================
with st.sidebar:
    st.image("https://res.cloudinary.com/dkdgj03sl/image/upload/v1769850715/Black_and_Red_Car_Animated_Logo-8_ebzsvo.png", width=180)

    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:12px; margin-bottom:20px; border:1px solid rgba(255,255,255,0.1);">
            <div style="color:#94a3b8; font-size:10px; font-weight:700; letter-spacing:1px;">AKTİF KURUM</div>
            <div style="color:white; font-weight:700; font-size:14px; margin-top:4px;">{safe_text(st.session_state.get('firm','Müşteri'))}</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio("NAVİGASYON", options=["🏠 Genel Bakış", "🔍 Sürücü Sorgula"], index=0)

    if menu == "🔍 Sürücü Sorgula":
        if not df_surucu.empty and "Sürücü Adı" in df_surucu.columns:
            ismler = sorted(df_surucu["Sürücü Adı"].dropna().unique().tolist())
            secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)
        else:
            secilen_surucu = "Seçiniz..."
    else:
        secilen_surucu = "Seçiniz..."

    st.markdown("---")
    st.caption("BetterWay Intelligence v6.1")

# =========================================================
# 10) SAYFA 1: SÜRÜCÜ SORGULAMA (FIX UYGULANDI)
# =========================================================
if menu == "🔍 Sürücü Sorgula" and secilen_surucu != "Seçiniz..." and not df_surucu.empty:
    rr = df_surucu[df_surucu["Sürücü Adı"] == secilen_surucu].iloc[0]

    driver_name = safe_text(rr.get("Sürücü Adı", "-"))
    egitim_yeri = safe_text(rr.get("EĞİTİM YERİ", "-"))
    egitim_turu = safe_text(rr.get("EĞİTİM TÜRÜ", "-"))
    puan = safe_text(rr.get("SÜRÜŞ PUANI", "0"))
    on_test = safe_text(rr.get("EĞİTİM ÖNCESİ TEST", "-"))
    son_test = safe_text(rr.get("EĞİTİM SONRASI TEST", "-"))
    egitim_tarihi = safe_text(rr.get("EĞİTİM TARİHİ", "-"))
    zayif = safe_multiline(rr.get("ZAYIF YÖNLER", None))
    gecerlilik = safe_text(rr.get("EĞİTİM GEÇERLİLİK TARİHİ", "-"))
    kalan = safe_text(rr.get("EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?", "-"))

    st.markdown(f"""
        <div class="hero-profile">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:#e63946; font-weight:700; font-size:12px; letter-spacing:2px;">AKADEMİ PERSONEL KARTI</span>
                    <h1 style="margin:8px 0; font-size:42px; color:white;">{driver_name}</h1>
                    <p style="color:#94a3b8; font-size:18px;">
                        <span style="margin-right:20px;">📍 {egitim_yeri}</span>
                        <span>🎓 {egitim_turu}</span>
                    </p>
                </div>
                <div class="score-ring">{puan}</div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; margin-top:40px;">
                <div class="glass-card">
                    <h4 style="margin-bottom:15px; color:#e63946; display:flex; align-items:center; gap:10px;">📊 Performans Analizi</h4>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Ön Test:</b> {on_test}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Son Test:</b> {son_test}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Eğitim Tarihi:</b> {egitim_tarihi}</p>
                </div>

                <div class="glass-card">
                    <h4 style="margin-bottom:15px; color:#e63946; display:flex; align-items:center; gap:10px;">⚠️ Gelişim Alanları</h4>
                    <p style="color:#cbd5e1; line-height:1.6;">{zayif}</p>
                </div>
            </div>

            <div style="margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; display:flex; justify-content:space-between;">
                <span style="color:#94a3b8;">📅 Geçerlilik: <b>{gecerlilik}</b></span>
                <span style="color:#e63946; font-weight:700;">⏳ {kalan} GÜN KALDI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# 11) SAYFA 2: GENEL BAKIŞ
# =========================================================
else:
    # KPI sayısı: ACAPET’te 3 (İŞE ALIM yok)
    if HAS_ISE_ALIM:
        k1, k2, k3, k4 = st.columns(4)
    else:
        k1, k3, k4 = st.columns(3)

    with k1:
        v = int(pd.to_numeric(df_genel.get("KATILIMCI SAYISI", pd.Series([0])), errors="coerce").fillna(0).sum()) if not df_genel.empty else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{v}</div><div class="kpi-trend" style="color:#22c55e;">▲ Aktif Eğitim</div></div>', unsafe_allow_html=True)

    if HAS_ISE_ALIM:
        with k2:
            ise = pd.to_numeric(df_genel.get("İŞE ALIM", pd.Series([0])), errors="coerce").fillna(0).sum() if not df_genel.empty else 0
            st.markdown(f'<div class="glass-card"><div class="kpi-title">İşe Alım</div><div class="kpi-value">{int(ise)}</div><div class="kpi-trend" style="color:#e63946;">● Akademi Çıktısı</div></div>', unsafe_allow_html=True)

    with k3:
        k_gun = pd.to_numeric(df_surucu.get("EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?", pd.Series([])), errors="coerce") if not df_surucu.empty else pd.Series([])
        k_sayi = int((k_gun < 30).sum()) if len(k_gun) else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{k_sayi}</div><div class="kpi-trend" style="color:#94a3b8;">⏱️ &lt; 30 Gün</div></div>', unsafe_allow_html=True)

    with k4:
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel) if not df_genel.empty else 0}</div><div class="kpi-trend" style="color:#94a3b8;">📋 Toplam Oturum</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>⚠️ En Sık Rastlanan Uygunsuzluklar</h3>", unsafe_allow_html=True)
        if not df_hata.empty and df_hata.shape[1] >= 2:
            df_h_plot = df_hata.sort_values(by=df_hata.columns[1], ascending=False).head(8)
            cat_col = df_hata.columns[0]
            val_col = df_hata.columns[1]

            fig = px.pie(
                df_h_plot,
                values=val_col,
                names=cat_col,
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu_r
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=0, r=0),
                height=350,
                showlegend=False,
                annotations=[dict(text='Hatalar', x=0.5, y=0.5, font_size=18, showarrow=False, font_color='#94a3b8')]
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent',
                hovertemplate="<b>%{label}</b><br>Hata Sayısı: %{value}<br>Oran: %{percent}",
                marker=dict(line=dict(color='#0f1115', width=3))
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_r:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>🗓️ Yenileme Takvimi</h3>", unsafe_allow_html=True)
        if not df_surucu.empty and "EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?" in df_surucu.columns:
            df_t = df_surucu.copy()
            df_t["kg"] = pd.to_numeric(df_t["EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?"], errors="coerce")
            df_t = df_t.sort_values(by="kg", ascending=True)
            crit_df = df_t[df_t["kg"] < 30]

            if not crit_df.empty:
                for _, rrow in crit_df.head(4).iterrows():
                    st.markdown(f"""<div class="status-alert">🚨 {safe_text(rrow.get('Sürücü Adı','-'))} - <span style="float:right;">{int(rrow.get('kg',0) if pd.notnull(rrow.get('kg',0)) else 0)} Gün</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-success">✅ Tüm personel süreleri güncel.</div>', unsafe_allow_html=True)

            with st.expander("🔻 TAM LİSTEYİ GÖRÜNTÜLE"):
                cols_show = [c for c in ["Sürücü Adı", "EĞİTİM YERİ", "EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?"] if c in df_t.columns]
                st.dataframe(df_t[cols_show].dropna(), use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; margin-bottom:25px;'>📂 Gerçekleştirilen Eğitimler Arşivi</h3>", unsafe_allow_html=True)

    if not df_genel.empty and "EĞİTİM TARİHİ" in df_genel.columns:
        df_g = df_genel.copy()
        df_g["DT"] = pd.to_datetime(df_g["EĞİTİM TARİHİ"], dayfirst=True, errors="coerce")

        f1, f2 = st.columns(2)
        with f1:
            sort_order = st.selectbox("📅 Sıralama", ["Yeniden Eskiye", "Eskiden Yeniye"])
        with f2:
            locs = ["Tümü"] + (sorted(df_g["EĞİTİM YERİ"].dropna().unique().tolist()) if "EĞİTİM YERİ" in df_g.columns else [])
            selected_loc = st.selectbox("📍 Lokasyon Filtresi", locs)

        df_filtered = df_g.copy()
        if selected_loc != "Tümü" and "EĞİTİM YERİ" in df_filtered.columns:
            df_filtered = df_filtered[df_filtered["EĞİTİM YERİ"] == selected_loc]

        df_filtered = df_filtered.sort_values(by="DT", ascending=(sort_order != "Yeniden Eskiye"))

        st.markdown("<br>", unsafe_allow_html=True)

        # header dinamik
        widths = [1, 1, 2, 1] + ([1] if HAS_ISE_ALIM else []) + [0.9]
        labels = ["TARİH", "LOKASYON", "EĞİTİM TÜRÜ", "KATILIMCI"] + (["İŞE ALIM"] if HAS_ISE_ALIM else []) + ["BELGE"]

        h = st.columns(widths)
        for i, lab in enumerate(labels):
            h[i].markdown(f'<div class="archive-header">{lab}</div>', unsafe_allow_html=True)

        st.markdown("<div style='border-bottom: 2px solid #2d3139; margin-bottom: 15px; margin-top:5px;'></div>", unsafe_allow_html=True)

        for _, row in df_filtered.iterrows():
            r = st.columns(widths)
            r[0].write(f"<span style='font-size:13px;'>{safe_text(row.get('EĞİTİM TARİHİ','-'))}</span>", unsafe_allow_html=True)
            r[1].write(f"<span style='font-size:13px;'>{safe_text(row.get('EĞİTİM YERİ','-'))}</span>", unsafe_allow_html=True)
            r[2].write(f"<b style='font-size:14px; color:#e2e8f0;'>{safe_text(row.get('EĞİTİM TÜRÜ','-'))}</b>", unsafe_allow_html=True)
            r[3].write(f"<span style='font-size:13px;'>{safe_text(row.get('KATILIMCI SAYISI','0'))} Kişi</span>", unsafe_allow_html=True)

            idx = 4
            if HAS_ISE_ALIM:
                ise_val = row.get("İŞE ALIM", 0)
                try:
                    ise_val = int(pd.to_numeric(ise_val, errors="coerce") or 0)
                except Exception:
                    ise_val = 0
                r[4].write(f"<span style='font-size:13px;'>{ise_val} Aday</span>", unsafe_allow_html=True)
                idx = 5

            link = str(row.get("RAPOR VE SERTİFİKALAR", "#"))
            if link and link != "nan" and link != "#":
                r[idx].markdown(f'<a href="{link}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)

            st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
