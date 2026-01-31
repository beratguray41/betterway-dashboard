import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Yönetim Paneli", layout="wide", page_icon="🏎️")

# --- ULTRA MODERN CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Modern Kart Yapısı */
    .metric-card {
        background: linear-gradient(145deg, #161b22, #1c2128);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Yaklaşan ve Gerçekleşen Eğitim Tablo Tasarımı */
    .training-row {
        background: #161b22;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #e63946;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .status-badge {
        background: #2d333b;
        color: #e63946;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #e63946;
    }

    h1, h2, h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
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
    except:
        return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Sürücü Arama")
    
    if not df_surucu.empty:
        ismler = sorted(df_surucu['Sürücü Adı'].astype(str).unique().tolist())
        selected_driver = st.selectbox("Sürücü Seçin/Yazın", options=["Seçiniz"] + ismler)
    
    st.divider()
    st.caption("BetterWay Akademi v3.0")

# --- ANA PANEL ---
st.title("🛡️ Akademi Operasyon Dashboard")

# 3. ÜST ÖZET METRİKLER
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><span>Son Eğitim Tarihi</span><br><b style="font-size:24px;">27.01.2026</b></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><span>Son Eğitim Yeri</span><br><b style="font-size:24px;">DERİNCE</b></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><span>Katılımcı (Son)</span><br><b style="font-size:24px; color:#e63946;">4</b></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><span>Eğitim Türü</span><br><b style="font-size:24px;">DEFANSİF</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. GRAFİK VE YAKLAŞAN EĞİTİMLER
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("⚠️ En Sık Rastlanan Uygunsuzluklar")
    if not df_hata.empty:
        fig = px.pie(df_hata, values=df_hata.columns[1], names=df_hata.columns[0], hole=0.6,
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🗓️ Yaklaşan Eğitim Programı")
    # Örnek Yaklaşan Eğitim Verisi (E-tablondan da çekilebilir, şimdilik manuel ekledim)
    upcoming_data = [
        {"Tarih": "05.02.2026", "Yer": "İZMİT", "Tür": "GÜVENLİ SÜRÜŞ", "Durum": "PLANLANDI"},
        {"Tarih": "12.02.2026", "Yer": "GEBZE", "Tür": "DEFANSİF SÜRÜŞ", "Durum": "ONAY BEKLİYOR"},
        {"Tarih": "18.02.2026", "Yer": "DERİNCE", "Tür": "PSİKOTEKNİK", "Durum": "PLANLANDI"}
    ]
    for train in upcoming_data:
        st.markdown(f"""
            <div class="training-row">
                <div>
                    <b>{train['Tarih']}</b> - {train['Yer']}<br>
                    <small style="color:#adbac7;">{train['Tür']}</small>
                </div>
                <div class="status-badge">{train['Durum']}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# 5. GERÇEKLEŞTİRİLEN EĞİTİMLER VE SERTİFİKALAR
if (not df_surucu.empty) and (selected_driver != "Seçiniz"):
    # Sürücü Detay Kartı
    st.subheader(f"👤 Sürücü Karnesi: {selected_driver}")
    driver_info = df_surucu[df_surucu['Sürücü Adı'] == selected_driver].iloc[0]
    st.markdown(f"""
        <div style="background:#1c2128; padding:20px; border-radius:15px; border:1px solid #e63946;">
            <h3>Puan: {driver_info['SÜRÜŞ PUANI']}</h3>
            <p><b>Eğitim:</b> {driver_info['EĞİTİM TÜRÜ']} | <b>Yer:</b> {driver_info['EĞİTİM YERİ']}</p>
            <p><b>Zayıf Yönler:</b> {driver_info['ZAYIF YÖNLER']}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.subheader("📄 Gerçekleştirilen Eğitimler Arşivi")
    # Tarihe göre sıralama (Yeniden Eskiye)
    if not df_genel.empty:
        df_genel['Tarih_DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        df_sorted = df_genel.sort_values(by='Tarih_DT', ascending=False)
        
        for _, row in df_sorted.iterrows():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"<b>{row['EĞİTİM YERİ']}</b> - {row['EĞİTİM TÜRÜ']}", unsafe_allow_html=True)
            with c2:
                st.write(f"📅 {row['EĞİTİM TARİHİ']}")
            with c3:
                l = str(row['RAPOR VE SERTİFİKALAR'])
                if l != "nan": st.link_button("Sertifika", l)
            st.markdown('<hr style="border:0.1px solid #30363d; margin:5px 0;">', unsafe_allow_html=True)

st.markdown("<br><center style='color:#666;'>BetterWay Akademi © 2026</center>", unsafe_allow_html=True)
