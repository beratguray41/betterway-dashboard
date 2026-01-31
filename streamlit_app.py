import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- ULTRA MODERN CSS ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Kart Yapıları */
    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .driver-card {
        background: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #e63946;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Yazı Renkleri */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    p, b, span { color: #adbac7 !important; }
    .score-text { color: #e63946 !important; font-size: 28px; font-weight: bold; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Butonlar */
    .stButton>button {
        width: 100%;
        background-color: #e63946;
        color: white !important;
        border-radius: 8px;
        border: none;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
GENEL_GID = "0"
SURUCU_GID = "395204791"

@st.cache_data(ttl=5)
def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)

# --- SIDEBAR (SÜRÜCÜ ARA) ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Sürücü Sorgulama")
    search_query = st.text_input("Sürücü Adı Yazın", placeholder="Sürücü ara...")
    st.divider()
    st.caption("BetterWay Dashboard v2.0 - 2026")

# --- ANA PANEL ---
st.title("🏎️ BetterWay Akademi Yönetim Paneli")

# 1. ÜST METRİKLER (Şık Kutular)
m1, m2, m3, m4 = st.columns(4)
with m1:
    val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
    st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:30px; color:white;">{val}</b></div>', unsafe_allow_html=True)
with m2:
    ise = len(df_genel[df_genel['İŞE ALIM'].str.contains("EVET", na=False, case=False)])
    st.markdown(f'<div class="metric-card"><span>İşe Alım</span><br><b style="font-size:30px; color:white;">{ise}</b></div>', unsafe_allow_html=True)
with m3:
    puan = pd.to_numeric(df_surucu['SÜRÜŞ PUANI'], errors='coerce').mean()
    st.markdown(f'<div class="metric-card"><span>Puan Ortalaması</span><br><b style="font-size:30px; color:#e63946;">{puan:.1f}</b></div>', unsafe_allow_html=True)
with m4:
    aktif = len(df_genel)
    st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:30px; color:white;">{aktif}</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. GRAFİKLER
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 En Sık Rastlanan Olumsuzluklar")
    if 'ZAYIF YÖNLER' in df_surucu.columns:
        zayif_data = df_surucu['ZAYIF YÖNLER'].replace(['nan', 'None', ''], pd.NA).dropna().value_counts().reset_index()
        zayif_data.columns = ['Hata', 'Adet']
        fig = px.pie(zayif_data, values='Adet', names='Hata', hole=0.5, 
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📈 Aylık Katılımcı Sayıları")
    if 'EĞİTİM TARİHİ' in df_genel.columns:
        df_genel['Tarih_DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        aylik = df_genel.groupby(df_genel['Tarih_DT'].dt.strftime('%m-%Y'))['KATILIMCI SAYISI'].sum().reset_index()
        fig2 = px.bar(aylik, x='Tarih_DT', y='KATILIMCI SAYISI', color_discrete_sequence=['#e63946'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

# 3. ALT BÖLÜM: SORGULAMA VEYA LİSTELEME
st.divider()

if search_query:
    st.subheader(f"👤 '{search_query}' Sonuçları")
    res = df_surucu[df_surucu['Sürücü Adı'].str.contains(search_query, case=False, na=False)]
    
    if not res.empty:
        for _, row in res.iterrows():
            st.markdown(f"""
            <div class="driver-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 22px; font-weight: bold; color: white !important;">{row['Sürücü Adı']}</span>
                    <span class="score-text">{row['SÜRÜŞ PUANI']} Puan</span>
                </div>
                <hr style="border: 0.1px solid #30363d;">
                <p><b>📍 Eğitim Yeri:</b> {row['EĞİTİM YERİ']} | <b>🎓 Tür:</b> {row['EĞİTİM TÜRÜ']}</p>
                <p><b>📝 Testler:</b> Ön Test: {row['EĞİTİM ÖNCESİ TEST']} | Son Test: {row['EĞİTİM SONRASI TEST']}</p>
                <p><b>⚠️ Zayıf Yönler:</b> <span style="color:#e63946 !important;">{row['ZAYIF YÖNLER'] if pd.notnull(row['ZAYIF YÖNLER']) else 'Yok'}</span></p>
                <p><b>⏳ Yenilemeye Kalan:</b> {row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} Gün</p>
            </div>
            """, unsafe_allow_html=True)
            # Belge Butonu (Genel Tablodan Eşleştirme)
            st.button(f"📄 {row['Sürücü Adı']} Sertifikasını İndir")
    else:
        st.error("Sürücü bulunamadı.")
else:
    st.subheader("📄 Genel Eğitim Tablosu ve Raporlar")
    for _, row in df_genel.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.markdown(f"**{row['EĞİTİM TÜRÜ']}**<br><small>{row['EĞİTİM YERİ']}</small>", unsafe_allow_html=True)
            with c2:
                st.write(f"📅 {row['EĞİTİM TARİHİ']}")
            with c3:
                l = row['RAPOR VE SERTİFİKALAR'] if pd.notnull(row['RAPOR VE SERTİFİKALAR']) else "#"
                st.link_button("📥 Rapor", l)
            st.markdown('<hr style="border: 0.1px solid #30363d;">', unsafe_allow_html=True)
