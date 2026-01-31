import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi Dashboard", layout="wide", page_icon="🏎️")

# BetterWay Cool Stil
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .report-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #e63946; margin-bottom: 20px; }
    .stat-box { background: #1d3557; color: white; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
GENEL_GID = "0"
SURUCU_GID = "395204791"

@st.cache_data(ttl=10)
def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=180)
    st.header("🔍 Sürücü Sorgulama")
    search_query = st.text_input("Sürücü Adı Yazın...", placeholder="Örn: Ahmet Yılmaz")
    
    st.markdown("---")
    st.info("Bulunan sürücünün belgesi aşağıda detaylarda listelenecektir.")

# --- ANA SAYFA ÜST KISIM (METRİKLER) ---
st.title("🛡️ BetterWay Akademi Yönetim Paneli")

# Aylık/Yıllık Özet Veriler
c1, c2, c3, c4 = st.columns(4)
with c1:
    total_k = df_genel['KATILIMCI SAYISI'].sum() if 'KATILIMCI SAYISI' in df_genel.columns else 0
    st.metric("Toplam Katılımcı", f"{total_k} Kişi")
with c2:
    ise_alim = (df_genel['İŞE ALIM'] == "EVET").sum() if 'İŞE ALIM' in df_genel.columns else 0
    st.metric("Toplam İşe Alım", f"{ise_alim} Kişi")
with c3:
    avg_p = pd.to_numeric(df_surucu['SÜRÜŞ PUANI'], errors='coerce').mean()
    st.metric("Genel Puan Ort.", f"{avg_p:.1f}")
with c4:
    st.metric("Aktif Eğitimler", len(df_genel))

st.divider()

# --- ORTA KISIM: GRAFİKLER ---
col_graph1, col_graph2 = st.columns([1, 1])

with col_graph1:
    st.subheader("⚠️ En Çok Tekrar Eden Olumsuzluklar")
    if 'ZAYIF YÖNLER' in df_surucu.columns:
        # nan olmayanları filtrele ve pasta grafiği yap
        zayif_yonler = df_surucu['ZAYIF YÖNLER'].dropna().value_counts().reset_index()
        zayif_yonler.columns = ['Hata Tipi', 'Sayı']
        fig = px.pie(zayif_yonler, values='Sayı', names='Hata Tipi', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig, use_container_width=True)

with col_graph2:
    st.subheader("📅 Aylık Katılımcı Dağılımı")
    # Tarih bazlı grafik (Eğitim Tarihi sütunu üzerinden)
    if 'EĞİTİM TARİHİ' in df_genel.columns:
        df_genel['Tarih'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], errors='coerce')
        monthly = df_genel.groupby(df_genel['Tarih'].dt.strftime('%B'))['KATILIMCI SAYISI'].sum().reset_index()
        fig2 = px.bar(monthly, x='Tarih', y='KATILIMCI SAYISI', color_discrete_sequence=['#1d3557'])
        st.plotly_chart(fig2, use_container_width=True)

# --- ALT KISIM: ARAMA SONUCU VEYA GENEL TABLO ---
st.divider()

if search_query:
    st.subheader(f"🔍 '{search_query}' İçin Arama Sonuçları")
    # Sürücü sayfasından ara
    results = df_surucu[df_surucu['Sürücü Adı'].str.contains(search_query, case=False, na=False)]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="report-card">
                <h3>👤 {row['Sürücü Adı']}</h3>
                <b>Puan: {row['SÜRÜŞ PUANI']}</b> | <b>Ön Test:</b> {row['EĞİTİM ÖNCESİ TEST']} | <b>Son Test:</b> {row['EĞİTİM SONRASI TEST']}<br>
                <b>Zayıf Yönler:</b> <span style="color:red">{row['ZAYIF YÖNLER'] if pd.notnull(row['ZAYIF YÖNLER']) else 'Tespit Edilmedi'}</span><br>
                <b>Yenilemeye Kalan:</b> {row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} Gün
            </div>
            """, unsafe_allow_html=True)
            # Belge/Rapor Linki
            if 'RAPOR VE SERTİFİKALAR' in df_genel.columns:
                # Genel tablodan ilgili sürücünün belgesini bulmaya çalış
                st.link_button("Sertifika / Belgeyi İndir", "https://betterway.com.tr") # Buraya link sütunu gelecek
    else:
        st.error("Sürücü bulunamadı.")

else:
    st.subheader("📄 Genel Eğitim Tablosu ve Sertifikalar")
    # Genel tabloyu listele
    for _, row in df_genel.iterrows():
        c_a, c_b, c_c = st.columns([3, 2, 1])
        with c_a:
            st.write(f"**{row['EĞİTİM TÜRÜ']}** - {row['EĞİTİM YERİ']}")
        with c_b:
            st.write(f"📅 {row['EĞİTİM TARİHİ']}")
        with c_c:
            link = row['RAPOR VE SERTİFİKALAR'] if pd.notnull(row['RAPOR VE SERTİFİKALAR']) else "#"
            st.link_button("📥 İndir", link)
        st.markdown("---")
