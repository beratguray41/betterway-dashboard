import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI VE TEMA
st.set_page_config(page_title="BetterWay Akademi | Dashboard", layout="wide", page_icon="🏎️")

# --- ULTRA MODERN DARK MODE TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Üst Metrik Kartları */
    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
        transition: 0.3s;
    }
    .metric-card:hover { border-color: #e63946; transform: translateY(-5px); }
    
    /* Sürücü Detay Kartı */
    .driver-card {
        background: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #e63946;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    
    /* Başlıklar ve Yazılar */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; letter-spacing: -1px; }
    p, b, span, label { color: #adbac7 !important; }
    .score-badge { 
        background-color: #e63946; color: white !important; 
        padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 20px;
    }
    
    /* Sidebar Ayarları */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Scrollbar Tasarımı */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ ÇEKME FONKSİYONU
SHEET_ID = "1Q-VMr9_wz7Op-tutiYePUhZi3OKmyITMKJmtqQuN1YU"
GENEL_GID = "0"
SURUCU_GID = "395204791"

@st.cache_data(ttl=5)
def load_data(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Veri yüklenemedi (GID: {gid}): {e}")
        return pd.DataFrame()

df_genel = load_data(GENEL_GID)
df_surucu = load_data(SURUCU_GID)

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.betterway.com.tr/wp-content/uploads/2021/05/logo.png", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Sürücü Sorgulama")
    search_query = st.text_input("Sürücü Adı Yazın", placeholder="İsim soyisim...")
    st.divider()
    st.markdown("💡 **İpucu:** Sürücü araması yaparak kişisel belge ve sertifikalara ulaşabilirsiniz.")

# --- ANA PANEL ---
st.title("🛡️ BetterWay Akademi Yönetim Paneli")

if not df_genel.empty and not df_surucu.empty:
    
    # 3. ÜST METRİKLER
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        val = int(df_genel['KATILIMCI SAYISI'].sum()) if 'KATILIMCI SAYISI' in df_genel.columns else 0
        st.markdown(f'<div class="metric-card"><span>Toplam Katılımcı</span><br><b style="font-size:32px; color:white;">{val}</b></div>', unsafe_allow_html=True)
    with m2:
        # Hata korumalı metin arama
        ise_count = 0
        if 'İŞE ALIM' in df_genel.columns:
            ise_count = df_genel['İŞE ALIM'].astype(str).str.contains("EVET", na=False, case=False).sum()
        st.markdown(f'<div class="metric-card"><span>Toplam İşe Alım</span><br><b style="font-size:32px; color:white;">{ise_count}</b></div>', unsafe_allow_html=True)
    with m3:
        puan_avg = pd.to_numeric(df_surucu['SÜRÜŞ PUANI'], errors='coerce').mean()
        st.markdown(f'<div class="metric-card"><span>Genel Puan Ort.</span><br><b style="font-size:32px; color:#e63946;">{puan_avg:.1f}</b></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><span>Toplam Eğitim</span><br><b style="font-size:32px; color:white;">{len(df_genel)}</b></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. GRAFİKLER
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.subheader("⚠️ En Sık Rastlanan Olumsuzluklar")
        if 'ZAYIF YÖNLER' in df_surucu.columns:
            # Temizlik ve Sayma
            z_data = df_surucu['ZAYIF YÖNLER'].astype(str).replace(['nan', 'None', ''], pd.NA).dropna().value_counts().reset_index()
            z_data.columns = ['Olumsuzluk', 'Adet']
            fig_pie = px.pie(z_data, values='Adet', names='Olumsuzluk', hole=0.5, 
                             color_discrete_sequence=px.colors.sequential.Reds_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_r:
        st.subheader("📅 Eğitim Türü Dağılımı")
        if 'EĞİTİM TÜRÜ' in df_genel.columns:
            tur_data = df_genel['EĞİTİM TÜRÜ'].value_counts().reset_index()
            fig_bar = px.bar(tur_data, x='EĞİTİM TÜRÜ', y='count', color_discrete_sequence=['#e63946'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # 5. ARAMA SONUCU VEYA GENEL LİSTE
    if search_query:
        st.subheader(f"👤 '{search_query}' Detaylı Sürücü Karnesi")
        res = df_surucu[df_surucu['Sürücü Adı'].str.contains(search_query, case=False, na=False)]
        
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
                        ⚠️ <b>Zayıf Yönler:</b> <span style="color:#ff4d4d !important;">{row['ZAYIF YÖNLER'] if pd.notnull(row['ZAYIF YÖNLER']) and str(row['ZAYIF YÖNLER']) != 'nan' else 'Tespit Edilmedi'}</span>
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                        <span>⏳ <b>Yenilemeye Kalan:</b> {row['EĞİTİM YENİLEMEYE KAÇ GÜN KALDI?']} Gün</span>
                        <span style="font-size: 0.85rem;">Geçerlilik: {row['EĞİTİM GEÇERLİLİK TARİHİ']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Sürücüye özel sertifika/rapor butonu (E-tabloda RAPOR sütunu varsa eşleşir)
                st.button(f"📄 {row['Sürücü Adı']} - Sertifikayı Görüntüle")
        else:
            st.error("Sürücü sistemde bulunamadı. Lütfen ismi kontrol edin.")
    
    else:
        st.subheader("📄 Genel Eğitim Tablosu ve Sertifikalar")
        # Header
        h1, h2, h3 = st.columns([3, 2, 1])
        h1.write("**EĞİTİM BİLGİSİ**")
        h2.write("**TARİH**")
        h3.write("**İŞLEM**")
        st.divider()

        for _, row in df_genel.iterrows():
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.markdown(f"**{row['EĞİTİM TÜRÜ']}**<br><small>{row['EĞİTİM YERİ']}</small>", unsafe_allow_html=True)
            with c2:
                st.write(f"📅 {row['EĞİTİM TARİHİ']}")
            with c3:
                link = row['RAPOR VE SERTİFİKALAR'] if pd.notnull(row['RAPOR VE SERTİFİKALAR']) else "#"
                if link != "#":
                    st.link_button("📥 İndir", link)
                else:
                    st.caption("Belge Yok")
            st.markdown('<hr style="border: 0.1px solid #30363d; margin: 5px 0;">', unsafe_allow_html=True)

else:
    st.warning("E-tablo verileri yükleniyor veya ulaşılamıyor. Lütfen paylaşım ayarlarını kontrol edin.")

st.markdown("<br><br><center style='color: #666;'>BetterWay Akademi Dashboard © 2026</center>", unsafe_allow_html=True)
