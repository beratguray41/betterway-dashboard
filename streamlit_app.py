import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ⚙️ YAPILANDIRMA (AYARLAR)
# Kullanıcı adı ve şifreyi buradan değiştirebilirsiniz
# ==========================================
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "betterway2026"

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Giriş", layout="wide", page_icon="🏎️")

# --- KİMLİK DOĞRULAMA DURUMU ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- MODERN ARAYÜZ TASARIMI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Giriş Ekranı Arka Planı - Aydınlık ve Sade */
    .login-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #f8fafc; /* Çok hafif modern gri/mavi tonu */
        z-index: -1;
    }

    /* Giriş Formu Konteynırı - Tam Merkezleme */
    .login-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        overflow: hidden;
    }
    
    /* Beyaz Yumuşak Köşeli Kart Tasarımı */
    .login-card {
        background: #ffffff;
        padding: 50px 40px;
        border-radius: 32px; /* Yumuşak köşeler */
        box-shadow: 0 20px 40px rgba(0,0,0,0.04); /* Hafif ve profesyonel gölge */
        width: 90%;
        max-width: 440px;
        text-align: center;
        border: 1px solid #f1f5f9;
    }

    /* Login ekranındayken Streamlit öğelerini gizleme */
    body:has(.login-container) {
        overflow: hidden !important;
        background-color: #f8fafc !important;
    }
    body:has(.login-container) header {
        display: none !important;
    }
    body:has(.login-container) [data-testid="stVerticalBlock"] {
        padding: 0 !important;
        gap: 0 !important;
    }

    /* Dashboard Tasarımı (Giriş yaptıktan sonraki koyu tema) */
    .stApp {
        background: radial-gradient(circle at top right, #1d1f27, #0f1115);
    }

    [data-testid="stSidebar"] {
        background-color: #161920;
        border-right: 1px solid #2d3139;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
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
        padding: 10px 22px;
        border-radius: 12px;
        text-decoration: none;
        font-size: 14px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .kpi-title { color: #94a3b8; font-size: 13px; font-weight: 600; text-transform: uppercase; }
    .kpi-value { color: #ffffff; font-size: 34px; font-weight: 700; }

    /* Modern Giriş Butonu */
    div.stButton > button {
        background-color: #1e293b !important; /* Lacivert/Siyah tonu */
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        font-weight: 600 !important;
        height: 3.5rem !important;
        transition: 0.3s all !important;
        margin-top: 15px;
    }
    div.stButton > button:hover {
        background-color: #0075ff !important; /* Üzerine gelince canlı mavi */
        transform: translateY(-2px) !important;
    }

    /* Giriş Input Alanları */
    .stTextInput input {
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #f8fafc !important;
        padding: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ EKRANI FONKSİYONU ---
def show_login_screen():
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.4, 1])
    
    with center_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo
        st.image("https://assets.softr-files.com/applications/0d7745a6-552f-4fe6-a9dc-29570cb0f7b7/assets/a0e627e0-5a38-4798-9b07-b1beca18b0a4.png", width=240)
        
        st.markdown("<h2 style='color:#0f172a; margin-top:30px; font-weight:700; letter-spacing:-0.5px;'>Sisteme Giriş</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b; font-size:15px; margin-bottom:35px;'>BetterWay Akademi portalına hoş geldiniz</p>", unsafe_allow_html=True)
        
        # Form Alanları
        username = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adınızı girin", key="user_login", label_visibility="collapsed")
        password = st.text_input("Şifre", type="password", placeholder="Şifrenizi girin", key="pass_login", label_visibility="collapsed")
        
        if st.button("Giriş Yap", use_container_width=True):
            if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Giriş bilgileri hatalı!")
        
        st.markdown("<p style='color:#94a3b8; font-size:12px; margin-top:30px;'>© 2026 BetterWay Akademi Güvenli Erişim</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANA UYGULAMA MANTIĞI ---
if not st.session_state['logged_in']:
    show_login_screen()
else:
    # --- VERİ ÇEKME İŞLEMLERİ ---
    SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
    GENEL_GID = "0"
    SURUCU_GID = "395204791"
    HATA_OZETI_GID = "2078081831"

    @st.cache_data(ttl=5)
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
        st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=180)
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
        menu = st.radio("ANA MENÜ", options=["🏠 Genel Bakış", "🔍 Sürücü Sorgula"])
        
        if menu == "🔍 Sürücü Sorgula":
            if not df_surucu.empty:
                ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
                secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)
        
        st.markdown("---")
        if st.button("Güvenli Çıkış"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.caption("BetterWay Intelligence v8.2")

    # --- SAYFA İÇERİKLERİ ---
    if menu == "🔍 Sürücü Sorgula" and 'secilen_surucu' in locals() and secilen_surucu != "Seçiniz...":
        row = df_surucu[df_surucu['Sürücü Adı'] == secilen_surucu].iloc[0]
        st.markdown(f"""
            <div class="hero-profile">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color:#e63946; font-weight:700; font-size:12px; letter-spacing:2px;">AKADEMİ PERSONEL KARTI</span>
                        <h1 style="margin:8px 0; font-size:42px; color:white;">{row['Sürücü Adı']}</h1>
                        <p style="color:#94a3b8; font-size:18px;">📍 {row.get('EĞİTİM YERİ', '-')} | 🎓 {row.get('EĞİTİM TÜRÜ', '-')}</p>
                    </div>
                    <div class="score-ring">{row.get('SÜRÜŞ PUANI', '0')}</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top:40px;">
                    <div class="glass-card">
                        <h4 style="color:#e63946;">📊 Performans Analizi</h4>
                        <p><b>Ön Test:</b> {row.get('EĞİTİM ÖNCESİ TEST', '-')}</p>
                        <p><b>Son Test:</b> {row.get('EĞİTİM SONRASI TEST', '-')}</p>
                        <p><b>Eğitim Tarihi:</b> {row.get('EĞİTİM TARİHİ', '-')}</p>
                    </div>
                    <div class="glass-card">
                        <h4 style="color:#e63946;">⚠️ Gelişim Alanları</h4>
                        <p>{row.get('ZAYIF YÖNLER', 'Kritik bir zayıf yön tespit edilmemiştir.')}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        # Dashboard
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{int(df_genel["KATILIMCI SAYISI"].sum())}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam İşe Alım</div><div class="kpi-value">{int(pd.to_numeric(df_genel["İŞE ALIM"], errors="coerce").sum())}</div></div>', unsafe_allow_html=True)
        with k3:
            k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            st.markdown(f'<div class="glass-card"><div class="kpi-title">Kritik Yenileme</div><div class="kpi-value" style="color:#e63946;">{(k_gun < 30).sum()}</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="glass-card"><div class="kpi-title">Eğitim Sayısı</div><div class="kpi-value">{len(df_genel)}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
        l, r = st.columns([1.2, 1])
        with l:
            st.subheader("⚠️ Uygunsuzluk Özeti")
            fig = px.bar(df_hata.tail(10), x=df_hata.columns[1], y=df_hata.columns[0], orientation='h', template="plotly_dark", color_discrete_sequence=['#e63946'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with r:
            st.subheader("🗓️ Yenileme Takvimi")
            df_t = df_surucu.copy()
            df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='kg', ascending=True)
            crit = df_t[df_t['kg'] < 30]
            if not crit.empty:
                for _, row in crit.head(3).iterrows():
                    st.error(f"🚨 {row['Sürücü Adı']} - {int(row['kg'])} Gün Kaldı")
            else: st.success("✅ Tüm personel süreleri güncel.")

        st.divider()
        st.subheader("📂 Gerçekleştirilen Eğitimler Arşivi")
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        for _, row in df_genel.sort_values(by='DT', ascending=False).iterrows():
            with st.container():
                c = st.columns([1, 1.5, 2, 1, 0.8])
                c[0].write(row['EĞİTİM TARİHİ'])
                c[1].write(row['EĞİTİM YERİ'])
                c[2].write(f"**{row['EĞİTİM TÜRÜ']}**")
                c[3].write(f"{row['KATILIMCI SAYISI']} Kişi")
                l = str(row.get('RAPOR VE SERTİFİKALAR','#'))
                if l != "nan" and l != "#": c[4].markdown(f'<a href="{l}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)
                st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)
