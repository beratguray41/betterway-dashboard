import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Sürücü Takip Sistemi", layout="wide", page_icon="🏎️")

# BetterWay Kurumsal Stil (CSS)
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    div[data-testid="stMetricValue"] { color: #e63946 !important; font-size: 30px !important; }
    .driver-card { 
        background-color: white; padding: 20px; border-radius: 12px; 
        border-top: 5px solid #e63946; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .warning-text { color: #e63946; font-weight: bold; }
    .success-text { color: #2a9d8f; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME FONKSİYONU
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
SURUCU_GID = "395204791" # Tüm Sürücüler Sayfası GID

@st.cache_data(ttl=10)
def load_surucu_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SURUCU_GID}"
    try:
        data = pd.read_csv(url)
        # Sütun isimlerindeki gizli boşlukları temizleyelim
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
        return pd.DataFrame()

df = load_surucu_data()

# 3. ANA BAŞLIK
st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=160)
st.title("🛡️ Sürücü Performans ve Eğitim Takip Paneli")

if not df.empty:
    # --- ÜST METRİKLER ---
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Toplam Sürücü", len(df))
    with m2:
        avg_puan = pd.to_numeric(df['SÜRÜŞ PUANI'], errors='coerce').mean()
        st.metric("Ortalama Sürüş Puanı", f"{avg_puan:.1f}")
    with m3:
        # Yenilemeye 30 günden az kalanlar
        days_col = 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'
        if days_col in df.columns:
            kalan_gun = pd.to_numeric(df[days_col], errors='coerce')
            kritik_sayisi = (kalan_gun < 30).sum()
            st.metric("Yenilemesi Yaklaşan", f"{kritik_sayisi} Kişi")
    with m4:
        st.metric("Eğitim Yerleri", df['EĞİTİM YERİ'].nunique())

    st.divider()

    # --- FİLTRELEME VE ARAMA ---
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🔍 Arama & Filtre")
        search = st.text_input("Sürücü Adı ile Ara", placeholder="Örn: Ahmet Yılmaz")
        yer_filtre = st.multiselect("Eğitim Yerine Göre Filtrele", options=df['EĞİTİM YERİ'].unique())
    
    with c2:
        st.subheader("📈 Puan Dağılım Grafiği")
        fig = px.bar(df, x='Sürücü Adı', y='SÜRÜŞ PUANI', color='SÜRÜŞ PUANI', 
                     color_continuous_scale='Reds', template="plotly_white")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Filtreleri Uygula
    dff = df.copy()
    if search:
        dff = dff[dff['Sürücü Adı'].str.contains(search, case=False, na=False)]
    if yer_filtre:
        dff = dff[dff['EĞİTİM YERİ'].isin(yer_filtre)]

    # --- SÜRÜCÜ KARTLARI ---
    st.divider()
    st.subheader("📋 Detaylı Sürücü Karneleri")

    if dff.empty:
        st.info("Kriterlere uygun sürücü bulunamadı.")
    else:
        for _, row in dff.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="driver-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin:0;">👤 {row.get('Sürücü Adı', 'N/A')}</h3>
                            <p style="color:#666; margin-bottom:10px;">📍 {row.get('EĞİTİM YERİ', '-')} | 🎓 {row.get('EĞİTİM TÜRÜ', '-')}</p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 24px; font-weight: bold; color: #e63946;">{row.get('SÜRÜŞ PUANI', '0')} Puan</div>
                            <small style="color:#888;">Tarih: {row.get('EĞİTİM TARİHİ', '-')}</small>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
                        <div>
                            <b>📝 Test Sonuçları:</b><br>
                            Ön Test: {row.get('EĞİTİM ÖNCESİ TEST', '-')} | Son Test: {row.get('EĞİTİM SONRASI TEST', '-')}
                        </div>
                        <div>
                            <b>⚠️ Zayıf Yönler:</b><br>
                            <span style="color:#e63946;">{row.get('ZAYIF YÖNLER', 'Belirtilmemiş')}</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center;">
                        <span>⏳ <b>Eğitim Yenileme:</b> {row.get('EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?', '-')} Gün Kaldı</span>
                        <span style="font-size: 0.8rem; color:#888;">Geçerlilik: {row.get('EĞİTİM GEÇERLİLİK TARİHİ', '-')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.warning("E-tablodaki veriler okunamadı. Lütfen 'Tüm Sürücüler' sayfasındaki sütun başlıklarını ve GID numarasını kontrol edin.")
