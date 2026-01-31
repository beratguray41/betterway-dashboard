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

# Görsel Kaynakları
LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://assets.softr-files.com/applications/0d7745a6-552f-4fe6-a9dc-29570cb0f7b7/assets/a0e627e0-5a38-4798-9b07-b1beca18b0a4.png"

# =========================================================
# 2) LOGIN CSS (GÜNCELLENMİŞ - COMPACT & MODERN)
# =========================================================
def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* --- GENEL SAYFA --- */
        .stApp {{
            background: linear-gradient(rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.8)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
        }}
        
        /* Gereksiz Streamlit elemanlarını gizle */
        header, footer, [data-testid="stSidebar"] {{
            display: none !important;
        }}

        /* --- LOGIN KARTI --- */
        /* Padding düşürüldü, kart daraltıldı */
        [data-testid="stVerticalBlock"] > div:has(.login-container) {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            
            padding: 30px 25px !important; /* Dikey: 30px, Yatay: 25px */
            
            border-radius: 20px !important;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.4);
            max-width: 420px; /* Kart genişliği ideal boyuta çekildi */
            margin: auto;
            margin-top: 10vh;
            gap: 0.5rem !important;
        }}
        
        /* ✅ GİZLİ DIV SORUNU ÇÖZÜMÜ: */
        /* Login container içeren elementin sayfada yer kaplamasını engelle */
        div[data-testid="stElementContainer"]:has(.login-container) {{
            display: none !important;
        }}
        
        /* --- LOGO --- */
        .logo-container {{
            display: flex; 
            justify-content: center; 
            margin-bottom: 20px;
        }}
        .logo-container img {{
            width: 160px;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}

        /* --- INPUTS --- */
        .custom-label {{
            font-size: 13px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 4px;
            display: block;
        }}

        div[data-testid="stTextInput"] input {{
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            color: #1e293b !important;
            border-radius: 10px !important;
            padding: 0 14px !important;
            font-size: 14px !important;
            height: 44px !important;
            transition: all 0.2s ease;
        }}
        
        div[data-testid="stTextInput"] input:focus {{
            background-color: #ffffff !important;
            border: 1px solid #ff7b00 !important;
            box-shadow: 0 0 0 3px rgba(255, 123, 0, 0.15) !important;
        }}

        /* Göz ikonunu gizle */
        div[data-testid="stTextInput"] button {{
            display: none !important;
        }}

        /* --- TOGGLE CHECKBOX --- */
        div[data-testid="stCheckbox"] {{
            margin-top: 8px;
            display: flex;
            justify-content: flex-end; /* Sağa yasla */
        }}
        
        div[data-testid="stCheckbox"] label {{
            color: #64748b !important;
            font-size: 12px !important;
        }}
        
        /* Checkbox kutusu */
        div[data-testid="stCheckbox"] div[role="checkbox"] {{
            width: 34px !important;
            height: 18px !important;
            border-radius: 10px !important;
        }}
        
        div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {{
            background-color: #ff7b00 !important; 
        }}

        /* --- BUTTON --- */
        div.stButton > button {{
            background: linear-gradient(135deg, #ff7b00 0%, #ff5500 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            width: 100% !important;
            margin-top: 20px !important;
            box-shadow: 0 8px 20px rgba(255, 123, 0, 0.25) !important;
            height: 48px !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(255, 123, 0, 0.35) !important;
        }}

        .footer-text {{
            text-align: center;
            margin-top: 25px;
            font-size: 10px;
            color: #94a3b8;
            font-weight: 500;
            letter-spacing: 0.5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 3) LOGIN EKRANI
# =========================================================
def login_screen():
    inject_login_css()

    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    col1, col2, col3 = st.columns([1, 1, 1]) # Ortalamak için kolonlar

    with col2:
        # CSS Hedefleyici (Görünmez ama gerekli)
        st.markdown('<div class="login-container"></div>', unsafe_allow_html=True)
        
        # Logo
        st.markdown(f'''
            <div class="logo-container">
                <img src="{LOGO_URL}">
            </div>
        ''', unsafe_allow_html=True)

        # Kullanıcı Adı
        st.markdown('<span class="custom-label">Kullanıcı Adı</span>', unsafe_allow_html=True)
        username = st.text_input(
            "username",
            placeholder="E-posta veya kullanıcı adı",
            key="u_field",
            label_visibility="collapsed"
        )
        
        st.write("") # Küçük boşluk

        # Şifre
        st.markdown('<span class="custom-label">Şifre</span>', unsafe_allow_html=True)
        
        # Şifre Göster Toggle
        show_pw = st.checkbox("Şifreyi Göster", key="pw_toggle")
        
        password = st.text_input(
            "password",
            type="default" if show_pw else "password",
            placeholder="Şifreniz",
            key="p_field",
            label_visibility="collapsed"
        )

        # Giriş Butonu
        if st.button("SİSTEME GİRİŞ YAP"):
            u = username.strip().lower()
            if u in VALID_USERS and VALID_USERS[u]["password"] == password:
                st.session_state.auth = True
                st.session_state.user = u
                st.session_state.firm = VALID_USERS[u]["firm"]
                st.rerun()
            else:
                st.error("Giriş bilgileri hatalı!")

        st.markdown('<div class="footer-text">BETTERWAY AKADEMİ GÜVENLİ ERİŞİM © 2026</div>', unsafe_allow_html=True)

# =========================================================
# 4) APP LOGIC & DASHBOARD
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# BURADAN SONRASI: DASHBOARD (Giriş Başarılıysa Çalışır)
# ---------------------------------------------------------

# Dashboard CSS (Karanlık Mod)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body { overflow: auto !important; height: auto !important; }
.stApp { background: radial-gradient(circle at top right, #1d1f27, #0f1115) !important; }
[data-testid="stSidebar"] { background-color: #161920; border-right: 1px solid #2d3139; display: flex !important; visibility: visible !important; }
header { visibility: visible !important; display: block !important; }

.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
}
.kpi-title { color: #94a3b8; font-size: 14px; font-weight: 600; text-transform: uppercase; }
.kpi-value { color: #ffffff; font-size: 32px; font-weight: 700; margin-top: 8px; }

.hero-profile {
    background: linear-gradient(135deg, #1e222d 0%, #161920 100%);
    border-radius: 24px;
    padding: 40px;
    border: 1px solid #2d3139;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}
.score-ring {
    background: transparent;
    border: 4px solid #e63946;
    color: #e63946;
    width: 100px; height: 100px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 800;
}
.download-btn {
    background: #e63946;
    color: white !important;
    padding: 8px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
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
    except:
        return pd.DataFrame()

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
        if not df_surucu.empty and 'Sürücü Adı' in df_surucu.columns:
            ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
            secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)

    st.markdown("---")
    st.caption("BetterWay Intelligence v8.7")

# --- MAIN CONTENT ---
if menu == "🔍 Sürücü Sorgula" and 'secilen_surucu' in locals() and secilen_surucu != "Seçiniz..." and not df_surucu.empty:
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
    # KPI SATIRI
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        total_katilimci = int(pd.to_numeric(df_genel.get("KATILIMCI SAYISI", pd.Series([0])), errors="coerce").fillna(0).sum()) if not df_genel.empty else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{total_katilimci}</div></div>', unsafe_allow_html=True)

    with k2:
        total_ise_alim = int(pd.to_numeric(df_genel.get("İŞE ALIM", pd.Series([0])), errors="coerce").fillna(0).sum()) if not df_genel.empty else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam İşe Alım</div><div class="kpi-value">{total_ise_alim}</div></div>', unsafe_allow_html=True)

    with k3:
        if not df_surucu.empty and 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns:
            k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            val = int((k_gun < 30).fillna(False).sum())
        else:
            val = 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{val}</div></div>', unsafe_allow_html=True)

    with k4:
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel) if not df_genel.empty else 0}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GRAFİKLER
    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.subheader("⚠️ Uygunsuzluk Özeti")
        if not df_hata.empty and df_hata.shape[1] >= 2:
            fig = px.bar(df_hata.tail(10), x=df_hata.columns[1], y=df_hata.columns[0], orientation='h', template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Hata özeti verisi bulunamadı.")

    with col_r:
        st.subheader("🗓️ Yenileme Takvimi")
        if not df_surucu.empty and 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns and 'Sürücü Adı' in df_surucu.columns:
            df_t = df_surucu.copy()
            df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='kg', ascending=True)
            crit = df_t[df_t['kg'] < 30]
            if not crit.empty:
                for _, r in crit.head(3).iterrows():
                    st.error(f"🚨 {r.get('Sürücü Adı','-')} - {int(r.get('kg',0))} Gün")
            else:
                st.success("✅ Tüm personel süreleri güncel.")
        else:
            st.info("Yenileme takvimi için veri bulunamadı.")

    st.divider()
    st.subheader("📂 Eğitim Arşivi")

    # TABLO
    if not df_genel.empty and 'EĞİTİM TARİHİ' in df_genel.columns:
        df_genel = df_genel.copy()
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')

        for _, r in df_genel.sort_values(by='DT', ascending=False).iterrows():
            cols = st.columns([1, 1.5, 2, 1, 0.8])
            cols[0].write(r.get('EĞİTİM TARİHİ', '-'))
            cols[1].write(r.get('EĞİTİM YERİ', '-'))
            cols[2].write(f"**{r.get('EĞİTİM TÜRÜ','-')}**")
            cols[3].write(f"{r.get('KATILIMCI SAYISI','-')} Kişi")
            link = str(r.get('RAPOR VE SERTİFİKALAR', '#'))
            if link and link != "nan" and link != "#":
                cols[4].markdown(f'<a href="{link}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)
            st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)
    else:
        st.info("Eğitim arşivi verisi bulunamadı.")

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
