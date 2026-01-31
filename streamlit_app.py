import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- MODERN CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }
    /* Arşiv Tablo Stili */
    .archive-header {
        background-color: #1c2128;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        border-bottom: 2px solid #e63946;
        margin-bottom: 10px;
    }
    .archive-row {
        background-color: #161b22;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 5px;
        border: 1px solid #30363d;
        transition: 0.3s;
    }
    .archive-row:hover { border-color: #e63946; }
    h1, h2, h3 { color: #ffffff !important; }
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
        selected_driver = st.selectbox("İsim Seçin", options=["Genel Görünüm"] + ismler)
    st.divider()
    st.caption("BetterWay Akademi v3.5")

# --- ANA PANEL ---
st.title("🛡️ BetterWay Akademi Yönetim Paneli")

# 3. ÜST ÖZET (KPI)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:28px; color:#e63946;">' + str(int(df_genel['KATILIMCI SAYISI'].sum() if 'KATILIMCI SAYISI' in df_genel.columns else 0)) + '</b></div>', unsafe_allow_html=True)
with m2:
    ise = df_genel['İŞE ALIM'].astype(str).str.contains("EVET|1", na=False, case=False).sum() if 'İŞE ALIM' in df_genel.columns else 0
    st.markdown('<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:28px;">' + str(ise) + '</b></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><span>Eğitim Sayısı</span><br><b style="font-size:28px;">' + str(len(df_genel)) + '</b></div>', unsafe_allow_html=True)
with m4:
    puan = pd.to_numeric(df_surucu['SÜRÜŞ PUANI'], errors='coerce').mean()
    st.markdown('<div class="metric-card"><span>Puan Ortalaması</span><br><b style="font-size:28px; color:#e63946;">' + f"{puan:.1f}" + '</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. GRAFİK VE YAKLAŞAN EĞİTİMLER
c_left, c_right = st.columns([1, 1.2])

with c_left:
    st.subheader("⚠️ En Sık Rastlanan İlk 10 Uygunsuzluk")
    if not df_hata.empty:
        # VERİ TEMİZLEME VE FİLTRELEME (İLK 10)
        hata_col = df_hata.columns[0]
        adet_col = df_hata.columns[1]
        df_hata_sorted = df_hata.sort_values(by=adet_col, ascending=False)
        
        top_10 = df_hata_sorted.head(10)
        
        fig = px.pie(top_10, values=adet_col, names=hata_col, hole=0.5,
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True,
                          margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.subheader("🗓️ Yaklaşan Eğitimler")
    # Temsili yaklaşan eğitimler
    upcoming = [
        {"Tarih": "05.02.2026", "Yer": "İZMİT", "Tür": "GÜVENLİ SÜRÜŞ", "Sayı": "8"},
        {"Tarih": "12.02.2026", "Yer": "GEBZE", "Tür": "DEFANSİF SÜRÜŞ", "Sayı": "5"}
    ]
    for u in upcoming:
        st.markdown(f"""
            <div style="background:#1c2128; padding:12px; border-radius:10px; margin-bottom:10px; border-left:4px solid #30363d;">
                <span style="color:#e63946; font-weight:bold;">{u['Tarih']}</span> | {u['Yer']} | <b>{u['Tür']}</b> ({u['Sayı']} Kişi)
            </div>
        """, unsafe_allow_html=True)

# 5. ARŞİV BÖLÜMÜ (REVİZE EDİLEN TABLO)
st.divider()
if selected_driver == "Genel Görünüm":
    st.subheader("📂 Gerçekleştirilen Eğitimler Arşivi")
    
    # Başlık Satırı
    h_col = st.columns([1.5, 1.5, 2, 1, 1, 1])
    headers = ["📅 TARİH", "📍 YER", "🎓 EĞİTİM TÜRÜ", "👥 SAYI", "💼 İŞE ALIM", "📄 İNDİR"]
    for i, h in enumerate(headers):
        h_col[i].markdown(f"**{h}**")
    
    st.markdown('<hr style="border:1px solid #e63946; margin-top:0;">', unsafe_allow_html=True)
    
    if not df_genel.empty:
        # Tarihe göre sırala
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        df_sorted = df_genel.sort_values(by='DT', ascending=False)
        
        for _, row in df_sorted.iterrows():
            r_col = st.columns([1.5, 1.5, 2, 1, 1, 1])
            r_col[0].write(str(row.get('EĞİTİM TARİHİ', '-')))
            r_col[1].write(str(row.get('EĞİTİM YERİ', '-')))
            r_col[2].write(f"**{row.get('EĞİTİM TÜRÜ', '-')}**")
            r_col[3].write(str(row.get('KATILIMCI SAYISI', '0')))
            
            # İşe Alım Durumu
            ise_durum = "EVET" if "EVET" in str(row.get('İŞE ALIM', '')).upper() else "HAYIR"
            r_col[4].write(ise_durum)
            
            # İndir Butonu
            link = str(row.get('RAPOR VE SERTİFİKALAR', '#'))
            if link != "nan" and link != "#":
                r_col[5].link_button("📥", link)
            else:
                r_col[5].write("-")
            st.markdown('<hr style="border:0.1px solid #30363d; margin:2px 0;">', unsafe_allow_html=True)
else:
    # Sürücü Detay Sayfası
    st.subheader(f"👤 Sürücü Karnesi: {selected_driver}")
    d_info = df_surucu[df_surucu['Sürücü Adı'] == selected_driver].iloc[0]
    st.info(f"Puan: {d_info['SÜRÜŞ PUANI']} | Yer: {d_info['EĞİTİM YERİ']} | Zayıf Yön: {d_info['ZAYIF YÖNLER']}")
