import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 0) SAYFA AYARLARI
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Pro Dashboard", layout="wide", page_icon="🏎️")

# =========================================================
# 1) CONFIG & AUTH
# =========================================================
VALID_USERS = {
    "admin": {"password": "betterway2026", "firm": "BetterWay Akademi"},
    "demo@betterway.com": {"password": "betterway123", "firm": "Demo Firma"},
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://assets.softr-files.com/applications/0d7745a6-552f-4fe6-a9dc-29570cb0f7b7/assets/a0e627e0-5a38-4798-9b07-b1beca18b0a4.png"

def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ✅ Scroll ve Varsayılanları Sıfırla */
        html, body, [data-testid="stVerticalBlock"] {{
            overflow: hidden !important;
            height: 100vh !important;
            font-family: 'Inter', sans-serif !important;
        }}

        /* ✅ Arka Plan Görseli - En Altta */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.4)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Streamlit Bileşenlerini Gizle */
        header, footer {{ visibility: hidden !important; }}
        section[data-testid="stSidebar"] {{ display: none !important; }}

        /* ✅ Beyaz Yumuşak Köşeli Giriş Kartı Konteynırı */
        [data-testid="stVerticalBlock"] > div:has(.login-card-anchor) {{
            background: rgba(255, 255, 255, 0.98);
            padding: 50px 40px !important;
            border-radius: 40px !important;
            box-shadow: 0 40px 100px rgba(0,0,0,0.3) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.5);
            max-width: 440px;
            margin: auto;
        }}

        .login-text-center {{
            text-align: center;
            width: 100%;
        }}

        .login-card-h2 {{
            color: #0f172a;
            font-weight: 700;
            font-size: 28px;
            margin-bottom: 8px;
            letter-spacing: -1px;
            text-align: center;
        }}

        .login-card-p {{
            color: #64748b;
            font-size: 15px;
            margin-bottom: 30px;
            text-align: center;
        }}

        /* Input Tasarımları */
        .stTextInput input {{
            border-radius: 16px !important;
            border: 1px solid #e2e8f0 !important;
            background: #f8fafc !important;
            height: 3.5rem !important;
            color: #0f172a !important;
        }}

        /* Giriş Butonu */
        div.stButton > button {{
            background: #1e253d !important;
            color: white !important;
            border-radius: 16px !important;
            border: none !important;
            font-weight: 600 !important;
            height: 3.8rem !important;
            width: 100% !important;
            margin-top: 15px !important;
            transition: 0.3s all !important;
        }}

        div.stButton > button:hover {{
            background: #e63946 !important;
            box-shadow: 0 10px 20px rgba(230, 57, 70, 0.3) !important;
            transform: translateY(-2px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def login_screen():
    inject_login_css()
    
    # Sayfayı dikeyde ortalamak için boşluk
    st.write("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    
    _, mid, _ = st.columns([1, 1.2, 1])
    
    with mid:
        # Bu div CSS seçicisi için çapa görevi görür
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        
        st.markdown("<div class='login-text-center'>", unsafe_allow_html=True)
        st.image(LOGO_URL, width=240)
        st.markdown("<h2 class='login-card-h2'>Hoş Geldiniz</h2>", unsafe_allow_html=True)
        st.markdown("<p class='login-card-p'>Akademi paneline erişmek için giriş yapın</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        username = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adınız", key="u_field", label_visibility="collapsed")
        password = st.text_input("Şifre", type="password", placeholder="Şifreniz", key="p_field", label_visibility="collapsed")
        
        if st.button("Sisteme Giriş Yap"):
            u = username.strip().lower()
            if u in VALID_USERS and VALID_USERS[u]["password"] == password:
                st.session_state.auth = True
                st.session_state.user = u
                st.session_state.firm = VALID_USERS[u]["firm"]
                st.rerun()
            else:
                st.error("Giriş bilgileri hatalı!")
        
        st.markdown('<p style="text-align:center; margin-top:25px; font-size:12px; color:#94a3b8; font-weight:500;">BetterWay Intelligence © 2026</p>', unsafe_allow_html=True)

# =========================================================
# 2) APP LOGIC
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# --- DASHBOARD CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body {{
    overflow: auto !important;
    height: auto !important;
}}

.stApp {{
    background: radial-gradient(circle at top right, #1d1f27, #0f1115) !important;
}}

[data-testid="stSidebar"] {{
    background-color: #161920;
    border-right: 1px solid #2d3139;
    display: flex !important;
}}

header, footer {{ visibility: visible !important; }}

.glass-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
}}

.kpi-title {{ color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase; }}
.kpi-value {{ color: #ffffff; font-size: 32px; font-weight: 700; margin-top: 8px; }}

.hero-profile {{
    background: linear-gradient(135deg, #1e222d 0%, #161920 100%);
    border-radius: 24px;
    padding: 40px;
    border: 1px solid #2d3139;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}}

.score-ring {{
    background: transparent;
    border: 4px solid #e63946;
    color: #e63946;
    width: 100px; height: 100px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 800;
}}

.download-btn {{
    background: #e63946;
    color: white !important;
    padding: 10px 20px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}}
</style>
""", unsafe_allow_html=True)

# --- VERİ ÇEKME ---
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
    except: return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# --- SIDEBAR ---
with st.sidebar:
    st.image(LOGO_URL, width=180)
    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; margin-bottom:20px; border:1px solid rgba(255,255,255,0.1);">
            <div style="color:#94a3b8; font-size:11px; font-weight:700;">AKTİF OTURUM</div>
            <div style="color:white; font-weight:600; font-size:14px;">{st.session_state.get('firm', 'Firma')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Güvenli Çıkış"):
        st.session_state.auth = False
        st.rerun()

    menu = st.radio("NAVİGASYON", options=["🏠 Genel Bakış", "🔍 Sürücü Sorgula"])
    
    if menu == "🔍 Sürücü Sorgula":
        if not df_surucu.empty:
            ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
            secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)
    
    st.markdown("---")
    st.caption("BetterWay Intelligence v8.7")

# --- MAIN PANEL CONTENT ---
if menu == "🔍 Sürücü Sorgula" and 'secilen_surucu' in locals() and secilen_surucu != "Seçiniz...":
    # PERSONEL KARTI
    row = df_surucu[df_surucu['Sürücü Adı'] == secilen_surucu].iloc[0]
    st.markdown(f"""
        <div class="hero-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color:#e63946; font-weight:700; font-size:12px; letter-spacing:2px;">PERSONEL ANALİZ KARTI</span>
                    <h1 style="margin:8px 0; font-size:42px; color:white;">{row['Sürücü Adı']}</h1>
                    <p style="color:#94a3b8; font-size:18px;">📍 {row.get('EĞİTİM YERİ', '-')} | 🎓 {row.get('EĞİTİM TÜRÜ', '-')}</p>
                </div>
                <div class="score-ring">{row.get('SÜRÜŞ PUANI', '0')}</div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top:40px;">
                <div class="glass-card">
                    <h4 style="color:#e63946; margin-bottom:15px;">📊 Performans Skoru</h4>
                    <p><b>Ön Test:</b> {row.get('EĞİTİM ÖNCESİ TEST', '-')}</p>
                    <p><b>Son Test:</b> {row.get('EĞİTİM SONRASI TEST', '-')}</p>
                </div>
                <div class="glass-card">
                    <h4 style="color:#e63946; margin-bottom:15px;">⚠️ Zayıf Yönler</h4>
                    <p>{row.get('ZAYIF YÖNLER', 'Kayıt bulunamadı.')}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # DASHBOARD
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{int(df_genel["KATILIMCI SAYISI"].sum())}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam İşe Alım</div><div class="kpi-value">{int(pd.to_numeric(df_genel["İŞE ALIM"], errors="coerce").sum())}</div></div>', unsafe_allow_html=True)
    with k3:
        k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{(k_gun < 30).sum()}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.subheader("⚠️ Uygunsuzluk Özeti")
        fig = px.bar(df_hata.tail(10), x=df_hata.columns[1], y=df_hata.columns[0], orientation='h', template="plotly_dark", color_discrete_sequence=['#e63946'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("🗓️ Yenileme Takvimi")
        df_t = df_surucu.copy()
        df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
        df_t = df_t.sort_values(by='kg', ascending=True)
        crit = df_t[df_t['kg'] < 30]
        if not crit.empty:
            for _, r in crit.head(3).iterrows(): st.error(f"🚨 {r['Sürücü Adı']} - {int(r['kg'])} Gün")
        else: st.success("✅ Tüm personel süreleri güncel.")

    st.divider()
    st.subheader("📂 Eğitim Arşivi")
    df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
    for _, r in df_genel.sort_values(by='DT', ascending=False).iterrows():
        cols = st.columns([1, 1.5, 2, 1, 0.8])
        cols[0].write(r['EĞİTİM TARİHİ'])
        cols[1].write(r['EĞİTİM YERİ'])
        cols[2].write(f"**{r['EĞİTİM TÜRÜ']}**")
        cols[3].write(f"{r['KATILIMCI SAYISI']} Kişi")
        link = str(r.get('RAPOR VE SERTİFİKALAR','#'))
        if link != "nan" and link != "#": cols[4].markdown(f'<a href="{link}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)
        st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
