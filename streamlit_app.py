import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 0) SAYFA AYARLARI
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Pro Dashboard", layout="wide", page_icon="🏎️")

# =========================================================
# 1) LOGIN CONFIG (DEMO)
# =========================================================
VALID_USERS = {
    # email/username : {password, firm}
    "demo@betterway.com": {"password": "betterway123", "firm": "Demo Firma"},
    # "shell@firma.com": {"password":"xxxx", "firm":"Shell"},
    # "ford@firma.com": {"password":"yyyy", "firm":"Ford Trucks"},
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769850715/Black_and_Red_Car_Animated_Logo-8_ebzsvo.png"


def inject_login_css(bg_url: str, logo_url: str):
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* ✅ Scroll tamamen kapalı */
        html, body {{
            height: 100% !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            font-family: 'Inter', sans-serif !important;
            background: #0f1115 !important;
        }}

        .stApp {{
            height: 100vh !important;
            overflow: hidden !important;
            background: #0f1115 !important;
        }}

        /* Streamlit default boşlukları */
        .block-container {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }}

        /* Header/footer gizle */
        header, footer {{ visibility: hidden; }}

        /* Login sırasında sidebar kapalı */
        section[data-testid="stSidebar"] {{ display: none !important; }}

        /* ✅ Fullscreen background */
        .login-stage {{
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            background:
              linear-gradient(0deg, rgba(15,17,21,0.60), rgba(15,17,21,0.60)),
              url('{bg_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}

        /* ✅ Center card */
        .login-card {{
            width: min(560px, 92vw);
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(255,255,255,0.70);
            border-radius: 22px;
            box-shadow: 0 25px 90px rgba(0,0,0,0.45);
            padding: 34px 34px 26px 34px;
            backdrop-filter: blur(12px);
        }}

        .login-head {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 12px;
            margin-bottom: 18px;
        }}

        .login-logo {{
            width: 100px;
            height: auto;
            opacity: 0.95;
            filter: drop-shadow(0 12px 28px rgba(0,0,0,0.22));
        }}

        .login-title {{
            font-size: 34px;
            line-height: 1.12;
            font-weight: 800;
            color: #0b1220;
            margin: 0;
        }}

        .login-sub {{
            font-size: 14px;
            color: #334155;
            margin: 0;
            margin-top: 6px;
            font-weight: 650;
        }}

        /* Inputs */
        div[data-baseweb="input"] input {{
            background: rgba(255,255,255,0.96) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(2, 6, 23, 0.10) !important;
            padding: 14px 12px !important;
        }}

        /* Labels */
        label, .stTextInput label {{
            color: #0b1220 !important;
            font-weight: 750 !important;
        }}

        /* Button (example style) */
        div.stButton > button, .stForm button {{
            width: 100% !important;
            border-radius: 14px !important;
            padding: 0.95rem 1rem !important;
            border: none !important;
            background: #0b74ff !important;
            color: #fff !important;
            font-weight: 850 !important;
            box-shadow: 0 12px 30px rgba(11,116,255,0.28) !important;
            transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
        }}
        div.stButton > button:hover, .stForm button:hover {{
            background: #1b82ff !important;
            transform: translateY(-1px);
            box-shadow: 0 16px 40px rgba(11,116,255,0.35) !important;
        }}

        .login-foot {{
            margin-top: 16px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
            font-weight: 650;
        }}

        .login-msg {{
            margin-top: 10px;
            padding: 10px 12px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 800;
        }}
        .login-err {{
            background: rgba(230,57,70,0.10);
            color: #b4232f;
            border: 1px solid rgba(230,57,70,0.20);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def login_screen():
    inject_login_css(LOGIN_BG_URL, LOGO_URL)

    # session init
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "firm" not in st.session_state:
        st.session_state.firm = None

    st.markdown('<div class="login-stage"><div class="login-card">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="login-head">
          <img class="login-logo" src="{LOGO_URL}" />
          <h1 class="login-title">Welcome back</h1>
          <p class="login-sub">BetterWay Akademi • Kurumsal Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Email *", placeholder="Enter your email")
        password = st.text_input("Password *", placeholder="Enter your password", type="password")
        submitted = st.form_submit_button("Continue")

    if submitted:
        u = (username or "").strip().lower()
        p = password or ""
        if u in VALID_USERS and VALID_USERS[u]["password"] == p:
            st.session_state.auth = True
            st.session_state.user = u
            st.session_state.firm = VALID_USERS[u].get("firm", "Firma")
            st.rerun()
        else:
            st.markdown('<div class="login-msg login-err">⛔ Email veya şifre hatalı.</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-foot">BetterWay Akademi Management Dashboard © 2026</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# =========================================================
# 2) AUTH GUARD
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# =========================================================
# 3) DASHBOARD CSS (SENİN MEVCUT TASARIMIN)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f1115;
}

.stApp {
    background: radial-gradient(circle at top right, #1d1f27, #0f1115);
}

/* Sidebar Tasarımı */
[data-testid="stSidebar"] {
    background-color: #161920;
    border-right: 1px solid #2d3139;
}

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
.hero-profile::after {
    content: "";
    position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(230, 57, 70, 0.1);
    border-radius: 50%; blur: 60px;
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
}
.status-success {
    background: rgba(34, 197, 94, 0.1);
    color: #4ade80;
    padding: 12px 20px;
    border-radius: 12px;
    border-left: 4px solid #22c55e;
    font-weight: 500;
}

/* İndirme Butonu */
.download-btn {
    background: #e63946;
    color: white !important;
    padding: 10px 20px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
    transition: 0.3s all ease;
    box-shadow: 0 4px 12px rgba(230, 57, 70, 0.3);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border: none;
}
.download-btn:hover {
    background: #ff4d4d;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 57, 70, 0.5);
    color: white !important;
}

/* Divider Custom */
hr { border: 0; border-top: 1px solid #2d3139; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 4) VERİ ÇEKME
# =========================================================
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
GENEL_GID = "0"
SURUCU_GID = "395204791"
HATA_OZETI_GID = "2078081831"

@st.cache_data(ttl=60)
def load_data(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# =========================================================
# 5) SIDEBAR
# =========================================================
with st.sidebar:
    st.image(LOGO_URL, width=180)

    firm = st.session_state.get("firm") or "Firma"
    user = st.session_state.get("user") or "user"
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10); padding:10px 12px; border-radius:14px; margin-bottom:14px;">
            <div style="color:#94a3b8; font-size:12px; font-weight:700;">GİRİŞ YAPILDI</div>
            <div style="color:#e2e8f0; font-size:14px; font-weight:800;">{firm}</div>
            <div style="color:#94a3b8; font-size:12px; margin-top:2px;">Kullanıcı: <b style="color:#e2e8f0;">{user}</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Çıkış Yap"):
        st.session_state.auth = False
        st.session_state.user = None
        st.session_state.firm = None
        st.rerun()

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
    st.caption("BetterWay Intelligence v6.0")

# =========================================================
# 6) ANA PANEL
# =========================================================
if menu == "🔍 Sürücü Sorgula" and secilen_surucu != "Seçiniz..." and not df_surucu.empty:
    row = df_surucu[df_surucu["Sürücü Adı"] == secilen_surucu].iloc[0]

    st.markdown(f"""
        <div class="hero-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color:#e63946; font-weight:700; font-size:12px; letter-spacing:2px;">AKADEMİ PERSONEL KARTI</span>
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
                    <h4 style="margin-bottom:15px; color:#e63946; display:flex; align-items:center; gap:10px;">📊 Performans Analizi</h4>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Ön Test:</b> {row.get('EĞİTİM ÖNCESİ TEST', '-')}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Son Test:</b> {row.get('EĞİTİM SONRASI TEST', '-')}</p>
                    <p style="margin:5px 0; color:#cbd5e1;"><b>Eğitim Tarihi:</b> {row.get('EĞİTİM TARİHİ', '-')}</p>
                </div>
                <div class="glass-card">
                    <h4 style="margin-bottom:15px; color:#e63946; display:flex; align-items:center; gap:10px;">⚠️ Gelişim Alanları</h4>
                    <p style="color:#cbd5e1; line-height:1.6;">{row.get('ZAYIF YÖNLER', 'Kritik bir zayıf yön tespit edilmemiştir.')}</p>
                </div>
            </div>
            <div style="margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; display:flex; justify-content:space-between;">
                <span style="color:#94a3b8;">📅 Geçerlilik: <b>{row.get('EĞİTİM GEÇERLİLİK TARİHİ', '-')}</b></span>
                <span style="color:#e63946; font-weight:700;">⏳ {row.get('EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?', '-')} GÜN KALDI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # KPI
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        v = int(df_genel["KATILIMCI SAYISI"].sum()) if (not df_genel.empty and "KATILIMCI SAYISI" in df_genel.columns) else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{v}</div><div class="kpi-trend" style="color:#22c55e;">▲ Aktif Eğitim</div></div>', unsafe_allow_html=True)

    with k2:
        ise = pd.to_numeric(df_genel["İŞE ALIM"], errors="coerce").sum() if (not df_genel.empty and "İŞE ALIM" in df_genel.columns) else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">İşe Alım</div><div class="kpi-value">{int(ise)}</div><div class="kpi-trend" style="color:#e63946;">● Akademi Çıktısı</div></div>', unsafe_allow_html=True)

    with k3:
        if not df_surucu.empty and "EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?" in df_surucu.columns:
            k_gun = pd.to_numeric(df_surucu["EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?"], errors="coerce")
            k_sayi = (k_gun < 30).sum()
        else:
            k_sayi = 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{k_sayi}</div><div class="kpi-trend" style="color:#94a3b8;">⏱️ < 30 Gün</div></div>', unsafe_allow_html=True)

    with k4:
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel) if not df_genel.empty else 0}</div><div class="kpi-trend" style="color:#94a3b8;">📋 Toplam Oturum</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # ANALİZ
    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>⚠️ En Sık Rastlanan Uygunsuzluklar</h3>", unsafe_allow_html=True)
        if not df_hata.empty:
            df_h_plot = df_hata.sort_values(by=df_hata.columns[1], ascending=True).tail(8)
            fig = px.bar(
                df_h_plot,
                x=df_hata.columns[1],
                y=df_hata.columns[0],
                orientation="h",
                template="plotly_dark",
                color_discrete_sequence=["#e63946"],
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0, b=0, l=0, r=0),
                xaxis=dict(showgrid=False, title="Vaka Sayısı"),
                yaxis=dict(title=None),
                height=350,
                font=dict(family="Inter", size=12),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_r:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>🗓️ Yenileme Takvimi</h3>", unsafe_allow_html=True)
        if not df_surucu.empty and "EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?" in df_surucu.columns:
            df_t = df_surucu.copy()
            df_t["kg"] = pd.to_numeric(df_t["EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?"], errors="coerce")
            df_t = df_t.sort_values(by="kg", ascending=True)

            crit_df = df_t[df_t["kg"] < 30]
            if not crit_df.empty:
                for _, rr in crit_df.head(4).iterrows():
                    st.markdown(f"""<div class="status-alert">🚨 {rr.get('Sürücü Adı','-')} - <span style="float:right;">{int(rr['kg'])} Gün</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-success">✅ Tüm personel süreleri güncel.</div>', unsafe_allow_html=True)

            with st.expander("🔻 TAM LİSTEYİ GÖRÜNTÜLE"):
                cols = [c for c in ["Sürücü Adı", "EĞİTİM YERİ", "EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?"] if c in df_t.columns]
                if cols:
                    st.dataframe(df_t[cols].dropna(), use_container_width=True, hide_index=True)

    # ARŞİV
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; margin-bottom:25px;'>📂 Gerçekleştirilen Eğitimler Arşivi</h3>", unsafe_allow_html=True)

    h_cols = st.columns([1, 1, 2, 1, 1, 0.8])
    labels = ["TARİH", "LOKASYON", "EĞİTİM TÜRÜ", "KATILIMCI", "İŞE ALIM", "DOKÜMAN"]
    for i, lab in enumerate(labels):
        h_cols[i].markdown(f"<small style='color:#64748b; font-weight:700;'>{lab}</small>", unsafe_allow_html=True)

    if not df_genel.empty:
        if "EĞİTİM TARİHİ" in df_genel.columns:
            df_genel["DT"] = pd.to_datetime(df_genel["EĞİTİM TARİHİ"], dayfirst=True, errors="coerce")

        for _, rr in df_genel.sort_values(by="DT", ascending=False).iterrows():
            with st.container():
                r = st.columns([1, 1, 2, 1, 1, 0.8])
                r[0].write(f"<span style='font-size:13px;'>{rr.get('EĞİTİM TARİHİ','-')}</span>", unsafe_allow_html=True)
                r[1].write(f"<span style='font-size:13px;'>{rr.get('EĞİTİM YERİ','-')}</span>", unsafe_allow_html=True)
                r[2].write(f"<b style='font-size:14px; color:#e2e8f0;'>{rr.get('EĞİTİM TÜRÜ','-')}</b>", unsafe_allow_html=True)
                r[3].write(f"<span style='font-size:13px;'>{rr.get('KATILIMCI SAYISI','0')} Kişi</span>", unsafe_allow_html=True)
                r[4].write(f"<span style='font-size:13px;'>{int(rr.get('İŞE ALIM', 0)) if pd.notnull(rr.get('İŞE ALIM')) else 0} Aday</span>", unsafe_allow_html=True)

                link = str(rr.get("RAPOR VE SERTİFİKALAR", "#"))
                if link != "nan" and link != "#":
                    r[5].markdown(f'<a href="{link}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)
                else:
                    r[5].write("")

                st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
