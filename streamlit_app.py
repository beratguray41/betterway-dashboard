import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- MODERN TASARIM (CSS) ---
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
    .driver-profile {
        background: linear-gradient(135deg, #1c2128 0%, #0b0e14 100%);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #e63946;
        box-shadow: 0 10px 40px rgba(230, 57, 70, 0.3);
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .score-circle {
        background: #e63946;
        color: white !important;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(230, 57, 70, 0.5);
    }
    .critical-box {
        background: rgba(230, 57, 70, 0.1);
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #e63946;
        margin-bottom: 8px;
    }
    /* Tablo Yazı Rengi */
    .stDataFrame, .stTable { color: #ffffff !important; }
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

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Sürücü Sorgulama")
    
    if not df_surucu.empty:
        surucu_listesi = sorted(df_surucu['Sürücü Adı'].dropna().astype(str).unique().tolist())
        # Streamlit session_state kullanarak navigasyonu kontrol ediyoruz
        if 'selected_driver' not in st.session_state:
            st.session_state.selected_driver = "ANASAYFA"

        secilen_isim = st.selectbox(
            "İsim yazın veya seçin",
            options=["ANASAYFA"] + surucu_listesi,
            key="driver_selector"
        )
        st.session_state.selected_driver = secilen_isim
    else:
        st.session_state.selected_driver = "ANASAYFA"
        
    st.divider()
    st.caption("BetterWay Akademi v5.1 | 2026")

# --- ANA PANEL ---
st.title("🛡️ Akademi Operasyon Paneli")

# --- SENARYO A: SÜRÜCÜ SEÇİLDİĞİNDE ---
if st.session_state.selected_driver != "ANASAYFA":
    st.subheader(f"👤 Sürücü Karnesi")
    
    # Veriyi çek
    surucu_verisi = df_surucu[df_surucu['Sürücü Adı'] == st.session_state.selected_driver].iloc[0]
    
    # Görsel Kart
    st.markdown(f"""
        <div class="driver-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin:0; font-size:36px; color:white !important;">{surucu_verisi['Sürücü Adı']}</h1>
                    <p style="font-size:18px; color:#adbac7 !important;">📍 {surucu_verisi.get('EĞİTİM YERİ', '-')} | 🎓 {surucu_verisi.get('EĞİTİM TÜRÜ', '-')}</p>
                </div>
                <div class="score-circle">{surucu_verisi.get('SÜRÜŞ PUANI', '0')}</div>
            </div>
            <hr style="border: 0.1px solid #30363d; margin: 25px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h4 style="color:#e63946 !important;">📊 Test Skorları</h4>
                    <p><b>Ön Test:</b> {surucu_verisi.get('EĞİTİM ÖNCESİ TEST', '-')}</p>
                    <p><b>Son Test:</b> {surucu_verisi.get('EĞİTİM SONRASI TEST', '-')}</p>
                    <p><b>Eğitim Tarihi:</b> {surucu_verisi.get('EĞİTİM TARİHİ', '-')}</p>
                </div>
                <div>
                    <h4 style="color:#e63946 !important;">⚠️ Gelişim Alanları</h4>
                    <p style="background: rgba(230,57,70,0.1); padding: 15px; border-radius: 10px; border: 1px solid #e63946; color:#ffffff !important;">
                        {surucu_verisi.get('ZAYIF YÖNLER', 'Kayıt bulunamadı.')}
                    </p>
                </div>
            </div>
            <div style="margin-top: 30px; padding: 15px; background: #161b22; border-radius: 10px; display: flex; justify-content: space-between; border: 1px solid #30363d;">
                <span>⏳ <b>Eğitim Yenileme:</b> {surucu_verisi.get('EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?', '-')} Gün Kaldı</span>
                <span>📅 <b>Geçerlilik:</b> {surucu_verisi.get('EĞİTİM GEÇERLİLİK TARİHİ', '-')}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Anasayfaya Dön Butonu
    if st.button("⬅️ Anasayfaya Dön"):
        st.session_state.selected_driver = "ANASAYFA"
        st.rerun()

# --- SENARYO B: ANASAYFA ---
else:
    # 3. KPI METRİKLERİ
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:32px; color:white;">{val}</b></div>', unsafe_allow_html=True)
    with m2:
        ise_alim = pd.to_numeric(df_genel['İŞE ALIM'], errors='coerce').sum() if 'İŞE ALIM' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:32px; color:white;">{int(ise_alim)}</b></div>', unsafe_allow_html=True)
    with m3:
        k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
        k_sayi = (k_gun < 30).sum() if not df_surucu.empty else 0
        st.markdown(f'<div class="metric-card"><span>Kritik Yenileme (<30 Gün)</span><br><b style="font-size:32px; color:#e63946;">{k_sayi}</b></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:32px; color:white;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. GRAFİK VE YENİLEME TAKVİMİ
    c_l, c_r = st.columns([1, 1.2])
    with c_l:
        st.subheader("⚠️ En Sık Rastlanan 10 Uygunsuzluk")
        if not df_hata.empty:
            df_h_top = df_hata.sort_values(by=df_hata.columns[1], ascending=False).head(10)
            fig = px.pie(df_h_top, values=df_h_top.columns[1], names=df_h_top.columns[0], hole=0.5, color_discrete_sequence=px.colors.sequential.Reds_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
    with c_r:
        st.subheader("🗓️ Eğitim Yenileme Takvimi")
        if not df_surucu.empty:
            df_t = df_surucu.copy()
            df_t['k_gun_n'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='k_gun_n', ascending=True)
            
            df_crit = df_t[df_t['k_gun_n'] < 30]
            if not df_crit.empty:
                for _, row in df_crit.head(3).iterrows():
                    st.markdown(f"""<div class="critical-box">🚨 <b>{row['Sürücü Adı']}</b>: {int(row['k_gun_n'])} Gün Kaldı</div>""", unsafe_allow_html=True)
            else:
                st.info("Kritik durumda sürücü bulunmuyor.")
            
            with st.expander("🔍 Tüm Sürücülerin Yenileme Planını Gör"):
                st.dataframe(df_t[['Sürücü Adı', 'EĞİTİM YERİ', 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']].dropna(), use_container_width=True, hide_index=True)

    # 5. ARŞİV
    st.divider()
    st.subheader("📂 Gerçekleştirilen Eğitimler Arşivi")
    h_cols = st.columns([1.2, 1.5, 2, 1, 1, 1])
    h_titles = ["📅 TARİH", "📍 YER", "🎓 EĞİTİM TÜRÜ", "👥 SAYI", "💼 İŞE ALIM", "📄 İNDİR"]
    for i, t in enumerate(h_titles): h_cols[i].markdown(f"**{t}**")
    
    if not df_genel.empty:
        df_genel['DT_SORT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        for _, row in df_genel.sort_values(by='DT_SORT', ascending=False).iterrows():
            r = st.columns([1.2, 1.5, 2, 1, 1, 1])
            r[0].write(str(row.get('EĞİTİM TARİHİ','-')))
            r[1].write(str(row.get('EĞİTİM YERİ','-')))
            r[2].write(f"**{row.get('EĞİTİM TÜRÜ','-')}**")
            r[3].write(str(row.get('KATILIMCI SAYISI','0')))
            r[4].write(str(int(row.get('İŞE ALIM', 0)) if pd.notnull(row.get('İŞE ALIM')) else 0))
            l = str(row.get('RAPOR VE SERTİFİKALAR','#'))
            if l != "nan" and l != "#": r[5].link_button("📥", l)
            else: r[5].write("-")
            st.markdown('<hr style="border:0.1px solid #30363d; margin:2px 0;">', unsafe_allow_html=True)
