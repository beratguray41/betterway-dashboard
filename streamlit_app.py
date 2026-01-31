import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi Dashboard", layout="wide", page_icon="🏎️")

# Custom CSS: BetterWay Tasarımı
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    div[data-testid="stMetricValue"] { color: #e63946 !important; font-size: 38px !important; }
    .report-card { 
        background-color: white; padding: 15px; border-radius: 12px; 
        border-left: 6px solid #e63946; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }
    .status-badge {
        background-color: #e63946; color: white; padding: 2px 8px; 
        border-radius: 4px; font-size: 12px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME (Doğrudan CSV Üzerinden - Kütüphane Gerektirmez)
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(URL)
        data.columns = data.columns.str.strip() # Sütun isimlerindeki boşlukları temizle
        return data.dropna(subset=['Sürücü Adı']) # Sürücü adı boş olanları at
    except Exception as e:
        st.error(f"Veri çekilemedi: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=180)
        st.markdown("### 🏢 Yönetim Paneli")
        
        firm_list = ["Tüm Firmalar"] + sorted(df['Firma Adı'].unique().tolist())
        selected_firm = st.selectbox("Firma Filtresi", firm_list)
        
        st.markdown("---")
        st.caption("BetterWay Akademi v1.0")

    # Filtreleme
    df_filtered = df if selected_firm == "Tüm Firmalar" else df[df['Firma Adı'] == selected_firm]

    # --- ANA EKRAN ---
    st.title("🏎️ BetterWay Sürüş Performans Analizi")
    
    # 3. KPI METRİKLERİ
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Toplam Katılımcı", len(df_filtered))
    with m2:
        avg_score = pd.to_numeric(df_filtered['Puan'], errors='coerce').mean()
        st.metric("Ortalama Puan", f"{avg_score:.1f}")
    with m3:
        top_driver = df_filtered.sort_values(by='Puan', ascending=False).iloc[0]['Sürücü Adı'] if not df_filtered.empty else "-"
        st.metric("En İyi Sürücü", top_driver)
    with m4:
        st.metric("Firma Sayısı", df_filtered['Firma Adı'].nunique())

    st.markdown("---")

    # 4. GRAFİKLER
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📊 Sürücü Puan Dağılımı")
        fig = px.bar(df_filtered, x='Sürücü Adı', y='Puan', 
                     color='Puan', color_continuous_scale='Reds', template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("🎯 Firma Katılım Oranı")
        fig2 = px.pie(df, names='Firma Adı', hole=0.5, color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig2, use_container_width=True)

    # 5. SÜRÜCÜ LİSTESİ VE RAPORLAR
    st.divider()
    st.subheader("📄 Eğitim Raporları ve Detaylar")
    
    search = st.text_input("🔍 Sürücü İsmi Ara...", placeholder="İsim yazmaya başlayın...")
    df_display = df_filtered[df_filtered['Sürücü Adı'].str.contains(search, case=False)] if search else df_filtered

    if df_display.empty:
        st.info("Kayıt bulunamadı.")
    else:
        for index, row in df_display.iterrows():
            st.markdown(f"""
                <div class="report-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.1rem; font-weight: bold; color: #1d3557;">{row['Sürücü Adı']}</span>
                            <span class="status-badge" style="margin-left:10px;">{row['Firma Adı']}</span><br>
                            <small style="color: #666;">Eğitim Tarihi: {row['Tarih']}</small>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 1.4rem; color: #e63946; font-weight: bold;">{row['Puan']} Puan</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            link = row['Rapor Linki'] if pd.notnull(row['Rapor Linki']) else "#"
            st.link_button(f"📄 {row['Sürücü Adı']} - Raporu Görüntüle", link)
else:
    st.warning("Veri yüklenemedi. Lütfen Google Sheets linkini ve sütun başlıklarını kontrol edin.")

st.markdown("---")
st.markdown("<center style='color: #999;'>BetterWay Akademi Dashboard © 2026</center>", unsafe_allow_html=True)
