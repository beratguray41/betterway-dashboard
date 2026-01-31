import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- GELİŞMİŞ MODERN TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* KPI Kartları */
    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }

    /* Modern Sürücü Kartı Tasarımı */
    .driver-profile {
        background: linear-gradient(135deg, #1c2128 0%, #0b0e14 100%);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #e63946;
        box-shadow: 0 10px 30px rgba(230, 57, 70, 0.2);
        margin-top: 20px;
    }
    
    .score-circle {
        background: #e63946;
        color: white !important;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0 0 15px #e63946;
    }

    /* Kritik Takip Satırı */
    .critical-row {
        background: rgba(230, 57, 70, 0.1);
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #e63946;
        margin-bottom: 8px;
    }

    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
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
    st.subheader("🔍 Sürücü Sorgulama")
    if not df_surucu.empty:
        ismler = sorted(df_surucu['Sürücü Adı'].astype(str).unique().tolist())
        selected_driver = st.selectbox("İsim Seçin veya Yazın", options=["GENEL DASHBOARD"] + ismler)
    st.divider()
    st.caption("BetterWay v3.8 | 2026")

# --- ANA PANEL ---
st.title("🛡️ BetterWay Akademi Operasyon Paneli")

# 3. ÜST ÖZETLER
m1, m2, m3, m4 = st.columns(4)
with m1:
    val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
    st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:28px;">{val}</b></div>', unsafe_allow_html=True)
with m2:
    ise = df_genel['İŞE ALIM'].astype(str).str.contains("EVET|1", na=False, case=False).sum() if 'İŞE ALIM' in df_genel.columns else 0
    st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:28px;">{ise}</b></div>', unsafe_allow_html=True)
with m3:
    if 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns:
        kritik = (pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce') < 30).sum()
    else: kritik = 0
    st.markdown(f'<div class="metric-card"><span>Eğitimi Yaklaşan</span><br><b style="font-size:28px; color:#e63946;">{kritik}</b></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:28px;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SAYFA MANTIĞI ---
if selected_driver == "GENEL DASHBOARD":
    
    # 4. GRAFİK VE YAKLAŞANLAR (KRİTİK TAKİP)
    c_left, c_right = st.columns([1, 1.2])

    with c_left:
        st.subheader("⚠️ En Sık Rastlanan Olumsuzluklar (Top 10)")
        if not df_hata.empty:
            df_hata_top = df_hata.sort_values(by=df_hata.columns[1], ascending=False).head(10)
            fig = px.pie(df_hata_top, values=df_hata_top.columns[1], names=df_hata_top.columns[0], hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Reds_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.subheader("🚨 Eğitimi Yaklaşan Sürücüler (< 30 Gün)")
        if 'EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?' in df_surucu.columns:
            # 30 günden az kalanları filtrele
            df_kritik = df_surucu[pd.to_numeric(df_surucu['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?'], errors='coerce') < 30].sort_values(by='EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?')
            
            if not df_kritik.empty:
                for _, row in df_kritik.iterrows():
                    st.markdown(f"""
                        <div class="critical-row">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span><b>{row['Sürücü Adı']}</b> - {row['EĞİTİM YERİ']}</span>
                                <span style="color:#e63946; font-weight:bold;">{row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} GÜN KALDI</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Tüm eğitim süreleri güncel görünüyor.")

    # 5. GERÇEKLEŞTİRİLEN EĞİTİMLER ARŞİVİ
    st.divider()
    st.subheader("📂 Gerçekleştirilen Eğitimler Arşivi")
    h_col = st.columns([1.2, 1.5, 2, 1, 1, 1])
    titles = ["📅 TARİH", "📍 YER", "🎓 EĞİTİM TÜRÜ", "👥 SAYI", "💼 İŞE ALIM", "📄 İNDİR"]
    for i, t in enumerate(titles): h_col[i].markdown(f"**{t}**")
    st.markdown('<hr style="border:1px solid #e63946; margin-top:0;">', unsafe_allow_html=True)

    if not df_genel.empty:
        df_genel['DT'] = pd.to_datetime(df_genel['EĞİTİM TARİHİ'], dayfirst=True, errors='coerce')
        for _, row in df_genel.sort_values(by='DT', ascending=False).iterrows():
            r = st.columns([1.2, 1.5, 2, 1, 1, 1])
            r[0].write(str(row.get('EĞİTİM TARİHİ','-')))
            r[1].write(str(row.get('EĞİTİM YERİ','-')))
            r[2].write(f"**{row.get('EĞİTİM TÜRÜ','-')}**")
            r[3].write(str(row.get('KATILIMCI SAYISI','0')))
            r[4].write("EVET" if "EVET" in str(row.get('İŞE ALIM','')).upper() else "HAYIR")
            link = str(row.get('RAPOR VE SERTİFİKALAR','#'))
            if link != "nan" and link != "#": r[5].link_button("📥", link)
            else: r[5].write("-")
            st.markdown('<hr style="border:0.1px solid #30363d; margin:2px 0;">', unsafe_allow_html=True)

else:
    # --- 6. MODERN SÜRÜCÜ KARNESİ ---
    st.subheader(f"👤 Sürücü Detaylı Performans Karnesi")
    row = df_surucu[df_surucu['Sürücü Adı'] == selected_driver].iloc[0]
    
    # Karnenin Üst Kısmı (Görsel Tasarım)
    st.markdown(f"""
        <div class="driver-profile">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin:0; font-size:40px;">{row['Sürücü Adı']}</h1>
                    <p style="font-size:18px; color:#adbac7;">📍 {row['EĞİTİM YERİ']} | 🎓 {row['EĞİTİM TÜRÜ']}</p>
                </div>
                <div class="score-circle">{row['SÜRÜŞ PUANI']}</div>
            </div>
            <hr style="border: 0.1px solid #30363d; margin: 25px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h4 style="color:#e63946;">📊 Test Sonuçları</h4>
                    <p><b>Eğitim Öncesi Test:</b> {row['EĞİTİM ÖNCESİ TEST']}</p>
                    <p><b>Eğitim Sonrası Test:</b> {row['EĞİTİM SONRASI TEST']}</p>
                    <p><b>Eğitim Tarihi:</b> {row['EĞİTİM TARİHİ']}</p>
                </div>
                <div>
                    <h4 style="color:#e63946;">⚠️ Gelişim Alanları</h4>
                    <p style="background: rgba(230,57,70,0.1); padding: 15px; border-radius: 10px; border: 1px solid #e63946;">
                        {row['ZAYIF YÖNLER'] if pd.notnull(row['ZAYIF YÖNLER']) else 'Tespit edilen zayıf yön bulunmamaktadır.'}
                    </p>
                </div>
            </div>
            <div style="margin-top: 30px; padding: 15px; background: #161b22; border-radius: 10px; display: flex; justify-content: space-between;">
                <span>⏳ <b>Eğitim Yenileme Durumu:</b> {row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} Gün Kaldı</span>
                <span>📅 <b>Geçerlilik Tarihi:</b> {row['EĞİTİM GEÇERLİLİK TARİHİ']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Rapor indirme butonu
    st.markdown("<br>", unsafe_allow_html=True)
    st.button(f"📄 {selected_driver} Sertifikasını Yazdır / İndir")

st.markdown("<br><center style='color:#666;'>BetterWay Akademi Dashboard v4.0</center>", unsafe_allow_html=True)
