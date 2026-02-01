import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1) SAYFA AYARLARI (EN BAŞTA OLMALI)
# =========================================================
st.set_page_config(page_title="BetterWay Akademi | Pro Dashboard", layout="wide", page_icon="🏎️")

# =========================================================
# 2) AUTH & LOGIN ALTYAPISI
# =========================================================
VALID_USERS = {
    "admin": {"password": "betterway2026", "firm": "BetterWay Akademi"},
 
}

LOGIN_BG_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769852261/c66a13ab-7751-4ebd-9ad5-6a2f907cb0da_1_bc0j6g.jpg"
LOGO_URL = "https://res.cloudinary.com/dkdgj03sl/image/upload/v1769924744/betterway_logo_arkaplan_xffybj.png"

# --- LOGIN CSS ---
def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {{
            background: linear-gradient(rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.8)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
        }}
        
        header, footer, [data-testid="stSidebar"] {{ display: none !important; }}

        /* Login Kartı */
        [data-testid="stVerticalBlock"] > div:has(.login-container) {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 35px 30px !important;
            border-radius: 20px !important;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.4);
            max-width: 440px;
            margin: auto;
            margin-top: 10vh;
            gap: 0.5rem !important;
        }}
        
        div[data-testid="stElementContainer"]:has(.login-container) {{ display: none !important; }}
        
        /* Logo */
        .logo-container {{ display: flex; justify-content: center; margin-bottom: 25px; }}
        .logo-container img {{ width: 200px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }}

        /* Inputlar */
        .custom-label {{ font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 5px; display: block; }}
        div[data-testid="stTextInput"] input {{
            background-color: #f8fafc !important; border: 1px solid #cbd5e1 !important;
            color: #1e293b !important; border-radius: 10px !important; padding: 0 14px !important;
            font-size: 14px !important; height: 48px !important; transition: all 0.2s ease;
        }}
        div[data-testid="stTextInput"] input:focus {{
            background-color: #ffffff !important; border: 1px solid #ff7b00 !important;
            box-shadow: 0 0 0 3px rgba(255, 123, 0, 0.15) !important;
        }}
        div[data-testid="stTextInput"] button {{ display: none !important; }}

        /* Buton */
        div.stButton > button {{
            background: linear-gradient(135deg, #ff7b00 0%, #ff5500 100%) !important;
            color: white !important; border: none !important; border-radius: 10px !important;
            padding: 12px !important; font-size: 15px !important; font-weight: 700 !important;
            width: 100% !important; margin-top: 25px !important;
            box-shadow: 0 8px 20px rgba(255, 123, 0, 0.25) !important; height: 50px !important;
        }}
        div.stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 12px 25px rgba(255, 123, 0, 0.35) !important; }}

        .footer-text {{ text-align: center; margin-top: 25px; font-size: 10px; color: #94a3b8; font-weight: 500; }}
        </style>
        """, unsafe_allow_html=True
    )

def login_screen():
    inject_login_css()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="login-container"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}"></div>', unsafe_allow_html=True)

        st.markdown('<span class="custom-label">Kullanıcı Adı</span>', unsafe_allow_html=True)
        username = st.text_input("username", placeholder="E-posta veya kullanıcı adı", label_visibility="collapsed")
        
        st.write("") 

        st.markdown('<span class="custom-label">Şifre</span>', unsafe_allow_html=True)
        # Type='password' kaldırıldı -> Şifre görünür
        password = st.text_input("password", placeholder="Şifreniz", label_visibility="collapsed")

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

# --- AUTH KONTROL ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# =========================================================
# 3) DASHBOARD (GİRİŞ YAPILDIKTAN SONRA ÇALIŞIR)
# =========================================================

# --- PREMIUM MODERN CSS (SaaS Style) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f1115;
    }
    
    /* Login background'u eziyoruz */
    .stApp {
        background: radial-gradient(circle at top right, #1d1f27, #0f1115) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #161920;
        border-right: 1px solid #2d3139;
        display: flex !important; /* Login'de gizlemiştik, geri açıyoruz */
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

# 2. VERİ ÇEKME
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
    st.image("https://res.cloudinary.com/dkdgj03sl/image/upload/v1769850715/Black_and_Red_Car_Animated_Logo-8_ebzsvo.png", width=180)
    
    # Aktif Firma Bilgisi
    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:20px; border:1px solid rgba(255,255,255,0.1);">
            <div style="color:#94a3b8; font-size:10px; font-weight:700;">AKTİF HESAP</div>
            <div style="color:white; font-weight:600; font-size:13px;">{st.session_state.get('firm', 'Firma')}</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "NAVİGASYON",
        options=["🏠 Genel Bakış", "🔍 Sürücü Sorgula"],
        index=0
    )
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    if menu == "🔍 Sürücü Sorgula":
        if not df_surucu.empty:
            ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
            secilen_surucu = st.selectbox("Personel Ara", options=["Seçiniz..."] + ismler)
        else: secilen_surucu = "Seçiniz..."
    else: secilen_surucu = "Seçiniz..."

    # Çıkış Yap Butonu
    if st.button("Güvenli Çıkış", key="logout_btn"):
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

# --- DURUM 2: ANASAYFA ---
else:
    # 3. KPI DASHBOARD
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        v = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="glass-card"><div class="kpi-title">Toplam Katılımcı</div><div class="kpi-value">{v}</div><div class="kpi-trend" style="color:#22c55e;">▲ Aktif Eğitim</div></div>', unsafe_allow_html=True)
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

    # 4. ANALİZ ALANI (MODERN GRAFİK VE TAKVİM)
    col_l, col_r = st.columns([1.2, 1])
    
    with col_l:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>⚠️ En Sık Rastlanan Uygunsuzluklar</h3>", unsafe_allow_html=True)
        if not df_hata.empty:
            # Pasta grafiği yerine modern Yatay Bar Grafik (Bar Chart)
            df_h_plot = df_hata.sort_values(by=df_hata.columns[1], ascending=True).tail(8)
            
            fig = px.bar(
                df_h_plot, 
                x=df_hata.columns[1], 
                y=df_hata.columns[0],
                orientation='h',
                template="plotly_dark",
                color_discrete_sequence=['#e63946']
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=0, b=0, l=0, r=0),
                xaxis=dict(showgrid=False, title="Vaka Sayısı"),
                yaxis=dict(title=None),
                height=350,
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_r:
        st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>🗓️ Yenileme Takvimi</h3>", unsafe_allow_html=True)
        if not df_surucu.empty:
            df_t = df_surucu.copy()
            df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='kg', ascending=True)
            
            crit_df = df_t[df_t['kg'] < 30]
            if not crit_df.empty:
                for _, row in crit_df.head(4).iterrows():
                    st.markdown(f"""<div class="status-alert">🚨 {row['Sürücü Adı']} - <span style="float:right;">{int(row['kg'])} Gün</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-success">✅ Tüm personel süreleri güncel.</div>', unsafe_allow_html=True)
            
            with st.expander("🔻 TAM LİSTEYİ GÖRÜNTÜLE"):
                st.dataframe(
                    df_t[['Sürücü Adı', 'EĞİTİM YERİ', 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']].dropna(), 
                    use_container_width=True, hide_index=True
                )

    # 5. EĞİTİM ARŞİVİ (CLEAN TABLE)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; margin-bottom:25px;'>📂 Gerçekleştirilen Eğitimler Arşivi</h3>", unsafe_allow_html=True)
    
    # Header
    h_cols = st.columns([1, 1, 2, 1, 1, 0.8])
    labels = ["TARİH", "LOKASYON", "EĞİTİM TÜRÜ", "KATILIMCI", "İŞE ALIM", "DOKÜMAN"]
    for i, l in enumerate(labels): h_cols[i].markdown(f"<small style='color:#64748b; font-weight:700;'>{l}</small>", unsafe_allow_html=True)
    
    if not df_genel.empty:
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        for _, row in df_genel.sort_values(by='DT', ascending=False).iterrows():
            with st.container():
                r = st.columns([1, 1, 2, 1, 1, 0.8])
                r[0].write(f"<span style='font-size:13px;'>{row.get('EĞİTİM TARİHİ','-')}</span>", unsafe_allow_html=True)
                r[1].write(f"<span style='font-size:13px;'>{row.get('EĞİTİM YERİ','-')}</span>", unsafe_allow_html=True)
                r[2].write(f"<b style='font-size:14px; color:#e2e8f0;'>{row.get('EĞİTİM TÜRÜ','-')}</b>", unsafe_allow_html=True)
                r[3].write(f"<span style='font-size:13px;'>{row.get('KATILIMCI SAYISI','0')} Kişi</span>", unsafe_allow_html=True)
                r[4].write(f"<span style='font-size:13px;'>{int(row.get('İŞE ALIM', 0)) if pd.notnull(row.get('İŞE ALIM')) else 0} Aday</span>", unsafe_allow_html=True)
                
                link = str(row.get('RAPOR VE SERTİFİKALAR','#'))
                if link != "nan" and link != "#": 
                    r[5].markdown(f'<a href="{link}" target="_blank" class="download-btn">İndir 📥</a>', unsafe_allow_html=True)
                else: 
                    r[5].write("")
                st.markdown("<div style='border-bottom: 1px solid #1e222d; margin: 8px 0;'></div>", unsafe_allow_html=True)

st.markdown("<br><br><center style='color:#475569; font-size:12px;'>BetterWay Akademi Management Dashboard © 2026</center><br>", unsafe_allow_html=True)
 
