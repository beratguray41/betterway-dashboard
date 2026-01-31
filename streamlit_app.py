import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI VE TEMA
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- ULTRA MODERN DARK MODE TASARIM (CSS) ---
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
    .driver-card {
        background: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #e63946;
        margin-bottom: 25px;
    }
    .score-badge { 
        background-color: #e63946; color: white !important; 
        padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 20px;
    }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME FONKSİYONU
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
    except Exception as e:
        return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)
df_hata = load_data(HATA_OZETI_GID)

# --- SOL PANEL (SÜRÜCÜ ARAMA REVİZE) ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Sürücü Sorgulama")
    
    # Dinamik Arama Kutusu (Yazmaya başladığında aşağı doğru liste akar)
    if not df_surucu.empty:
        ismler = sorted(df_surucu['Sürücü Adı'].astype(str).unique().tolist())
        selected_driver = st.selectbox(
            "Sürücü İsmi Yazın veya Seçin",
            options=["Arama Yapılmadı"] + ismler,
            index=0,
            help="Yazmaya başladığınızda eşleşen isimler listelenir."
        )
    else:
        selected_driver = "Arama Yapılmadı"
    
    st.divider()
    st.caption("BetterWay Dashboard v2.5")

# --- ANA PANEL ---
st.title("🛡️ BetterWay Akademi Yönetim Paneli")

if not df_genel.empty:
    
    # 3. ÜST METRİKLER
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:32px; color:white;">{val}</b></div>', unsafe_allow_html=True)
    with m2:
        ise_count = df_genel['İŞE ALIM'].astype(str).str.contains("EVET", na=False, case=False).sum() if 'İŞE ALIM' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:32px; color:white;">{ise_count}</b></div>', unsafe_allow_html=True)
    with m3:
        puan_avg = pd.to_numeric(df_surucu['SÜRÜŞ PUANI'], errors='coerce').mean() if not df_surucu.empty else 0
        st.markdown(f'<div class="metric-card"><span>Genel Puan Ort.</span><br><b style="font-size:32px; color:#e63946;">{puan_avg:.1f}</b></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:32px; color:white;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. GRAFİKLER (Hata Özeti)
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.subheader("⚠️ En Sık Rastlanan Olumsuzluklar")
        if not df_hata.empty:
            fig_pie = px.pie(df_hata, values=df_hata.columns[1], names=df_hata.columns[0], hole=0.5, 
                             color_discrete_sequence=px.colors.sequential.Reds_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
    with col_r:
        st.subheader("📊 Aylık Katılımcı Analizi")
        if 'EĞİTİM TARİHİ' in df_genel.columns:
            df_genel['Tarih_DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
            aylik = df_genel.groupby(df_genel['Tarih_DT'].dt.strftime('%m-%Y'))['KATILIMCI SAYISI'].sum().reset_index()
            fig_bar = px.bar(aylik, x='Tarih_DT', y='KATILIMCI SAYISI', color_discrete_sequence=['#e63946'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # 5. ARAMA SONUCU VEYA GENEL LİSTE
    if selected_driver != "Arama Yapılmadı":
        st.subheader(f"👤 Detaylı Sürücü Karnesi: {selected_driver}")
        res = df_surucu[df_surucu['Sürücü Adı'] == selected_driver]
        
        if not res.empty:
            for _, row in res.iterrows():
                st.markdown(f"""
                <div class="driver-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 26px; font-weight: bold; color: white !important;">{row['Sürücü Adı']}</span>
                        <span class="score-badge">{row['SÜRÜŞ PUANI']} PUAN</span>
                    </div>
                    <hr style="border: 0.1px solid #30363d; margin: 15px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <p>📍 <b>Eğitim Yeri:</b> {row['EĞİTİM YERİ']}</p>
                        <p>🎓 <b>Eğitim Türü:</b> {row['EĞİTİM TÜRÜ']}</p>
                        <p>📝 <b>Ön Test:</b> {row['EĞİTİM ÖNCESİ TEST']}</p>
                        <p>📝 <b>Son Test:</b> {row['EĞİTİM SONRASI TEST']}</p>
                    </div>
                    <p style="background: #2d1316; padding: 10px; border-radius: 8px; border: 1px solid #e63946;">
                        ⚠️ <b>Zayıf Yönler:</b> <span style="color:#ff4d4d !important;">{row['ZAYIF YÖNLER'] if pd.notnull(row['ZAYIF YÖNLER']) else 'Tespit Edilmedi'}</span>
                    </p>
                    <p>⏳ <b>Eğitim Yenileme:</b> {row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} Gün Kaldı</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Arama sonuçları açıkken genel tabloyu gizle ya da altına ekle. Biz gizliyoruz.
        if st.button("Aramayı Temizle"):
             st.rerun()
    
    else:
        st.subheader("📄 Genel Eğitim Tablosu ve Sertifikalar")
        if 'EĞİTİM TARİHİ' in df_genel.columns:
            df_genel['Sort_Date'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
            df_display = df_genel.sort_values(by='Sort_Date', ascending=False)
        else:
            df_display = df_genel

        for _, row in df_display.iterrows():
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.markdown(f"**{row['EĞİTİM TÜRÜ']}**<br><small>{row['EĞİTİM YERİ']}</small>", unsafe_allow_html=True)
            with c2:
                st.write(f"📅 {row['EĞİTİM TARİHİ']}")
            with c3:
                link = row['RAPOR VE SERTİFİKALAR'] if pd.notnull(row['RAPOR VE SERTİFİKALAR']) else "#"
                if link != "#":
                    st.link_button("📥 İndir", str(link))
            st.markdown('<hr style="border: 0.1px solid #30363d; margin: 5px 0;">', unsafe_allow_html=True)

else:
    st.warning("Veriler yüklenemedi. GID ve paylaşım ayarlarını kontrol edin.")
