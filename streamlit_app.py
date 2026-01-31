import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. SAYFA AYARLARI VE COOL TEMA
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# Custom CSS: BetterWay Kırmızısı ve Modern Fontlar
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { color: #e63946; font-size: 32px; font-weight: bold; }
    .stButton>button { background-color: #e63946; color: white; border-radius: 8px; border: none; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1, h2, h3 { color: #1d3557; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .report-card { 
        background-color: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #e63946; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ BAĞLANTISI
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=300)
def load_data():
    data = conn.read(spreadsheet=SHEET_URL)
    return data.dropna(how='all')

try:
    df = load_data()

    # --- SIDEBAR: LOGO VE FİLTRELER ---
    with st.sidebar:
        st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200) # Logo linkini güncelleyebilirsiniz
        st.markdown("---")
        st.subheader("🎯 Filtreleme Paneli")
        
        # Dinamik Filtreler (E-tablo sütun isimlerine göre ayarlanmalı)
        all_firms = ["Tüm Firmalar"] + list(df.iloc[:, 0].unique()) # 1. Sütun Firma varsayıldı
        selected_firm = st.selectbox("Firma Seçin", all_firms)
        
        st.info("Bu dashboard BetterWay Akademi için özel olarak tasarlanmıştır.")

    # Veri Filtreleme İşlemi
    if selected_firm != "Tüm Firmalar":
        df_final = df[df.iloc[:, 0] == selected_firm]
    else:
        df_final = df

    # --- ANA PANEL BAŞLANGIÇ ---
    st.title("🛡️ BetterWay Akademi Sürüş Analiz Sistemi")
    st.markdown(f"**Görüntülenen:** {selected_firm} | **Tarih:** {pd.Timestamp.now().strftime('%d/%m/%Y')}")

    # 3. KPI METRİKLERİ (Özet Bilgiler)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Toplam Katılımcı", len(df_final))
    with m2:
        # 2. Sütunun puan olduğunu varsayıyoruz, değilse indeksi değiştirin
        avg_score = pd.to_numeric(df_final.iloc[:, 1], errors='coerce').mean()
        st.metric("Ortalama Puan", f"{avg_score:.1f}/100")
    with m3:
        st.metric("Aktif Eğitimler", "14")
    with m4:
        st.metric("Başarı Oranı", "%88")

    st.markdown("---")

    # 4. GRAFİKLER (Cool Görünüm)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📈 Puan Dağılımı")
        fig = px.histogram(df_final, x=df_final.columns[1], nbins=10, 
                           color_discrete_sequence=['#e63946'], 
                           template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🏢 Firma Bazlı Katılım")
        fig2 = px.pie(df, names=df.columns[0], hole=0.4, 
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig2, use_container_width=True)

    # 5. SÜRÜCÜ LİSTESİ VE RAPORLAR
    st.markdown("---")
    st.subheader("📋 Katılımcı Detaylı Rapor Listesi")

    # Arama Kutusu
    search = st.text_input("", placeholder="Sürücü ismi veya detay ara...")
    
    # Veriyi filtrele ve göster
    if search:
        df_display = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_display = df_final

    # Modern Kart Yapısı
    for index, row in df_display.iterrows():
        st.markdown(f"""
            <div class="report-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #1d3557;">👤 {row.iloc[0]}</span><br>
                        <span style="color: #666;">Firma: {row.iloc[0]} | Tarih: {pd.Timestamp.now().strftime('%d/%m/%Y')}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.5rem; color: #e63946; font-weight: bold;">{row.iloc[1]} Puan</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Rapor Butonu (E-tabloda link varsa oraya gider)
        report_url = "https://betterway.com.tr" # Burayı row['Rapor Sütunu'] ile değiştirebiliriz
        st.link_button(f"📄 {row.iloc[0]} - Detaylı Raporu İndir", report_url)

except Exception as e:
    st.error(f"Veri bağlantısı sırasında bir hata oluştu: {e}")
    st.info("Lütfen Google Sheets belgenizin 'Bağlantıya sahip herkes görüntüleyebilir' olarak ayarlandığından emin olun.")

# FOOTER
st.markdown("---")
st.markdown("<center style='color: #999;'>BetterWay Akademi Dashboard © 2026 | Güvenli Sürüş, Güvenli Gelecek</center>", unsafe_allow_html=True)
