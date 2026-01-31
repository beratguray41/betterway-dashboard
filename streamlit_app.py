import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- ULTRA MODERN DARK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Sidebar Menü Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Sidebar'daki Radyo Butonları (Menü gibi göstermek için) */
    .stRadio > div {
        background-color: transparent;
        border-radius: 10px;
    }
    
    /* Kart Yapıları */
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
    }
    .score-circle {
        background: #e63946;
        color: white !important;
        width: 85px; height: 85px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 26px; font-weight: bold;
    }
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

# --- SOL BAR (SIDEBAR) GÖRSEL DÜZENLEME ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🏠 ANA MENÜ SEÇİMİ
    menu = st.radio(
        "📍 MENÜ",
        options=["🏠 ANASAYFA PANELİ", "🔍 SÜRÜCÜ SORGULAMA"],
        index=0
    )
    
    st.markdown("---")
    
    # Sadece Sürücü Sorgulama seçiliyse arama kutusunu göster
    if menu == "🔍 SÜRÜCÜ SORGULAMA":
        if not df_surucu.empty:
            ismler = sorted(df_surucu['Sürücü Adı'].dropna().unique().tolist())
            secilen_surucu = st.selectbox("👤 Sürücü Seçin", options=["Seçiniz..."] + ismler)
        else:
            secilen_surucu = "Seçiniz..."
    else:
        secilen_surucu = "Seçiniz..."

    st.divider()
    st.caption("BetterWay Akademi v5.5")

# --- ANA PANEL İÇERİĞİ ---
st.title("🛡️ BetterWay Operasyon Paneli")

# --- DURUM 1: SÜRÜCÜ SORGULAMA EKRANI ---
if menu == "🔍 SÜRÜCÜ SORGULAMA" and secilen_surucu != "Seçiniz...":
    st.subheader(f"📊 Kişisel Performans Karnesi")
    
    # Veriyi bul
    row = df_surucu[df_surucu['Sürücü Adı'] == secilen_surucu].iloc[0]
    
    st.markdown(f"""
        <div class="driver-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin:0; color:white !important;">{row['Sürücü Adı']}</h1>
                    <p>📍 {row.get('EĞİTİM YERİ', '-')} | 🎓 {row.get('EĞİTİM TÜRÜ', '-')}</p>
                </div>
                <div class="score-circle">{row.get('SÜRÜŞ PUANI', '0')}</div>
            </div>
            <hr style="border: 0.1px solid #30363d; margin: 20px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="color:#e63946;">📝 Test Bilgileri</h4>
                    <p>Ön Test: {row.get('EĞİTİM ÖNCESİ TEST', '-')}<br>Son Test: {row.get('EĞİTİM SONRASI TEST', '-')}</p>
                </div>
                <div>
                    <h4 style="color:#e63946;">⚠️ Zayıf Yönler</h4>
                    <p>{row.get('ZAYIF YÖNLER', 'Kayıt bulunamadı.')}</p>
                </div>
            </div>
            <div style="margin-top:20px; padding:10px; background:#161b22; border-radius:10px;">
                ⏳ <b>Yenileme:</b> {row.get('EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?', '-')} Gün Kaldı ({row.get('EĞİTİM GEÇERLİLİK TARİHİ', '-')})
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- DURUM 2: ANASAYFA DASHBOARD ---
else:
    # Üst KPI Kutuları
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:30px;">{val}</b></div>', unsafe_allow_html=True)
    with c2:
        ise = pd.to_numeric(df_genel['İŞE ALIM'], errors='coerce').sum() if 'İŞE ALIM' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:30px;">{int(ise)}</b></div>', unsafe_allow_html=True)
    with c3:
        k_gun = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
        k_sayi = (k_gun < 30).sum() if not df_surucu.empty else 0
        st.markdown(f'<div class="metric-card"><span>Kritik Yenileme</span><br><b style="font-size:30px; color:#e63946;">{k_sayi}</b></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:30px;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Grafik ve Takvim
    l, r = st.columns([1, 1.2])
    with l:
        st.subheader("⚠️ Uygunsuzluk Özeti")
        if not df_hata.empty:
            fig = px.pie(df_hata.head(10), values=df_hata.columns[1], names=df_hata.columns[0], hole=0.5, color_discrete_sequence=px.colors.sequential.Reds_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
    
    with r:
        st.subheader("🗓️ Yenileme Planı")
        if not df_surucu.empty:
            df_t = df_surucu.copy()
            df_t['kg'] = pd.to_numeric(df_t['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_t = df_t.sort_values(by='kg', ascending=True)
            with st.expander("🔻 TÜM SÜRÜCÜ LİSTESİ (Sıralı)"):
                st.dataframe(df_t[['Sürücü Adı', 'EĞİTİM YERİ', 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']].dropna(), use_container_width=True, hide_index=True)

    # Arşiv
    st.divider()
    st.subheader("📂 Eğitim Arşivi")
    df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
    for _, row in df_genel.sort_values(by='DT', ascending=False).iterrows():
        cols = st.columns([1.5, 1.5, 2, 1, 1, 1])
        cols[0].write(str(row.get('EĞİTİM TARİHİ','-')))
        cols[1].write(str(row.get('EĞİTİM YERİ','-')))
        cols[2].write(f"**{row.get('EĞİTİM TÜRÜ','-')}**")
        cols[3].write(str(row.get('KATILIMCI SAYISI','0')))
        cols[4].write(str(int(row.get('İŞE ALIM', 0)) if pd.notnull(row.get('İŞE ALIM')) else 0))
        link = str(row.get('RAPOR VE SERTİFİKALAR','#'))
        if link != "nan" and link != "#": cols[5].link_button("📥", link)
        else: cols[5].write("-")
        st.markdown('<hr style="border:0.1px solid #30363d; margin:2px 0;">', unsafe_allow_html=True)
