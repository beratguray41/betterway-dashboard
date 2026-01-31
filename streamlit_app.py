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
        border: 1px solid #e63946;
        margin-top: 20px;
    }
    .score-circle {
        background: #e63946;
        color: white !important;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
    }
    .critical-box {
        background: rgba(230, 57, 70, 0.1);
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #e63946;
        margin-bottom: 8px;
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
    except:
        return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    if not df_surucu.empty:
        ismler = sorted(df_surucu['Sürücü Adı'].astype(str).unique().tolist())
        selected_driver = st.selectbox("🔍 Sürücü Sorgula", options=["GENEL DASHBOARD"] + ismler)
    st.divider()
    st.caption("BetterWay v4.7 | 2026")

# --- ANA PANEL ---
st.title("🛡️ Akademi Operasyon Paneli")

if selected_driver == "GENEL DASHBOARD":
    
    # 3. ÜST ÖZETLER (KPI)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:32px; color:white;">{val}</b></div>', unsafe_allow_html=True)
    
    with m2:
        if 'İŞE ALIM' in df_genel.columns:
            ise_alim_toplam = pd.to_numeric(df_genel['İŞE ALIM'], errors='coerce').sum()
        else:
            ise_alim_toplam = 0
        st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:32px; color:white;">{int(ise_alim_toplam)}</b></div>', unsafe_allow_html=True)
    
    with m3:
        if 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns:
            # Sayısal formata çevir
            kalan_gunler = pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            k_sayi = (kalan_gunler < 30).sum()
        else: k_sayi = 0
        st.markdown(f'<div class="metric-card"><span>Kritik Yenileme (<30 Gün)</span><br><b style="font-size:32px; color:#e63946;">{k_sayi}</b></div>', unsafe_allow_html=True)
    
    with m4:
        st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:32px; color:white;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. GRAFİK VE YENİLEME TAKVİMİ
    c_left, c_right = st.columns([1, 1.2])

    with c_left:
        st.subheader("⚠️ En Sık Rastlanan 10 Uygunsuzluk")
        if not df_hata.empty:
            df_hata_top = df_hata.sort_values(by=df_hata.columns[1], ascending=False).head(10)
            fig = px.pie(df_hata_top, values=df_hata_top.columns[1], names=df_hata_top.columns[0], hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Reds_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.subheader("🗓️ Eğitim Yenileme Takvimi")
        if 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns:
            # Veriyi temizle ve sırala
            df_takvim = df_surucu.copy()
            df_takvim['kalan_gun_num'] = pd.to_numeric(df_takvim['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce')
            df_takvim = df_takvim.sort_values(by='kalan_gun_num', ascending=True)

            # Sadece 30 günün altındakileri kritik kutu olarak göster
            df_kritik = df_takvim[df_takvim['kalan_gun_num'] < 30]
            
            if not df_kritik.empty:
                for _, row in df_kritik.head(3).iterrows():
                    st.markdown(f"""<div class="critical-box">🚨 <b>{row['Sürücü Adı']}</b>: {int(row['kalan_gun_num'])} Gün Kaldı</div>""", unsafe_allow_html=True)
            else:
                st.info("Şu an kritik durumda (30 günden az) sürücü bulunmuyor.")

            # TÜM LİSTEYİ GÖSTER BUTONU (Planlama için tüm sürücüler)
            with st.expander("🔍 Tüm Sürücülerin Yenileme Takvimini Gör (Sıralı)"):
                # Tabloyu daha okunaklı formatla
                display_df = df_takvim[['Sürücü Adı', 'EĞİTİM YERİ', 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']].copy()
                display_df.columns = ['Sürücü Adı', 'Eğitim Yeri', 'Kalan Gün']
                st.dataframe(display_df, use_container_width=True, hide_index=True)

    # 5. ARŞİV
    st.divider()
    st.subheader("📂 Gerçekleştirilen Eğitimler Arşivi")
    h = st.columns([1.2, 1.5, 2, 1, 1, 1])
    titles = ["📅 TARİH", "📍 YER", "🎓 EĞİTİM TÜRÜ", "👥 SAYI", "💼 İŞE ALIM", "📄 İNDİR"]
    for i, t in enumerate(titles): h[i].markdown(f"**{t}**")
    
    if not df_genel.empty:
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        for _, row in df_genel.sort_values(by='DT', ascending=False).iterrows():
            r = st.columns([1.2, 1.5, 2, 1, 1, 1])
            r[0].write(str(row.get('EĞİTİM TARİHİ','-')))
            r[1].write(str(row.get('EĞİTİM YERİ','-')))
            r[2].write(f"**{row.get('EĞİTİM TÜRÜ','-')}**")
            r[3].write(str(row.get('KATILIMCI SAYISI','0')))
            r[4].write(str(int(row.get('İŞE ALIM', 0)) if pd.notnull(row.get('İŞE ALIM')) else 0))
            link = str(row.get('RAPOR VE SERTİFİKALAR','#'))
            if link != "nan" and link != "#": r[5].link_button("📥", link)
            else: r[5].write("-")
            st.markdown('<hr style="border:0.1px solid #30363d; margin:2px 0;">', unsafe_allow_html=True)
