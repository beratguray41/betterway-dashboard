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
# LOGIN CSS (LOGO ÜSTÜ BOŞ DİKDÖRTGEN YOK + EYE İKONU DIŞARIDA)
# =========================================================
def inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ✅ Background + scroll kapalı */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.10), rgba(0,0,0,0.35)), url('{LOGIN_BG_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            overflow: hidden !important;
        }}

        /* Header/footer/sidebar gizle */
        header, footer, [data-testid="stSidebar"] {{
            visibility: hidden !important;
            display: none !important;
        }}

        /* ✅ Login kartı (selector için login-box gerekli ama kendisini gizleyeceğiz) */
        [data-testid="stVerticalBlock"] > div:has(.login-box) {{
            background: rgba(255, 255, 255, 0.98);
            padding: 34px 44px !important;
            border-radius: 30px !important;
            box-shadow: 0 40px 100px rgba(0,0,0,0.30) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.55);
            max-width: 520px;
            margin: auto;
            margin-top: 10vh;
        }}

        /* ✅ Logo üstündeki "boş dikdörtgen" / placeholder görünmesin */
        .login-box {{
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* ✅ Label */
        .bw-label {{
            font-family: Inter, sans-serif;
            color: #0f172a;
            font-weight: 800;
            font-size: 13px;
            margin: 14px 0 6px 0;
            letter-spacing: .2px;
        }}

        /* ✅ Input full width */
        div[data-testid="stTextInput"] {{
            width: 100% !important;
        }}

        div[data-testid="stTextInput"] input {{
            width: 100% !important;
            border-radius: 14px !important;
            border: 1px solid #e2e8f0 !important;
            background: #f8fafc !important;
            height: 46px !important;
            color: #0f172a !important;
            padding-left: 14px !important;
            padding-right: 14px !important; /* ✅ artık göz ikonu input içinde değil */
            font-size: 14px !important;
        }}

        /* ✅ Streamlit'in şifre "göz" butonunu TAMAMEN gizle (alan daraltmasın) */
        div[data-testid="stTextInput"] button {{
            display: none !important;
        }}

        /* ✅ Şifreyi göster toggle satırı sağa yasla */
        .pw-toggle-wrap {{
            display: flex;
            justify-content: flex-end;
            margin-top: 6px;
            margin-bottom: 2px;
        }}
        .pw-toggle-wrap label {{
            font-family: Inter, sans-serif !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            color: #334155 !important;
        }}

        /* ✅ Turuncu giriş butonu */
        div.stButton > button {{
            background: #ff7b00 !important;
            color: #fff !important;
            border-radius: 14px !important;
            border: none !important;
            font-weight: 900 !important;
            height: 48px !important;
            width: 100% !important;
            margin-top: 18px !important;
            transition: 0.25s all !important;
            box-shadow: 0 6px 18px rgba(255, 123, 0, 0.25) !important;
        }}
        div.stButton > button:hover {{
            background: #e66f00 !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(255, 123, 0, 0.35) !important;
        }}

        .login-footer {{
            text-align: center;
            font-size: 10px;
            color: #94a3b8;
            margin-top: 18px;
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
    if "show_pw" not in st.session_state:
        st.session_state.show_pw = False

    _, mid, _ = st.columns([1, 1.6, 1])

    with mid:
        # selector için var ama görünmez (CSS ile gizli)
        st.markdown('<div class="login-box"></div>', unsafe_allow_html=True)

        st.image(LOGO_URL, width=220)
        st.write("")

        st.markdown('<div class="bw-label">Kullanıcı Adı</div>', unsafe_allow_html=True)
        username = st.text_input(
            "username",
            placeholder="E-posta veya kullanıcı adı",
            key="u_field",
            label_visibility="collapsed"
        )

        st.markdown('<div class="bw-label">Şifre</div>', unsafe_allow_html=True)

        # ✅ Göz ikonu input içinde değil: kendi toggle'ımız var.
        pw_type = "default" if st.session_state.show_pw else "password"
        password = st.text_input(
            "password",
            type=pw_type,
            placeholder="Şifreniz",
            key="p_field",
            label_visibility="collapsed"
        )

        # Sağda "Şifreyi göster" toggle (input'u ASLA daraltmaz)
        st.markdown('<div class="pw-toggle-wrap">', unsafe_allow_html=True)
        st.checkbox("Şifreyi göster", key="show_pw", label_visibility="visible")
        st.markdown('</div>', unsafe_allow_html=True)

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
# 2) APP LOGIC
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login_screen()
    st.stop()

# --- DASHBOARD CSS (SADECE GİRİŞTEN SONRA) ---
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
    padding: 10px 20px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 14px;
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

# --- MAIN PANEL CONTENT ---
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

