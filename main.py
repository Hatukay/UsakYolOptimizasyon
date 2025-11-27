"""
UsakYolOptimizasyon - Ana Streamlit Uygulaması
Karınca Kolonisi Algoritması ile Yol Optimizasyonu
"""

import streamlit as st
import sys
import os
import numpy as np
import pandas as pd

# Klasör yollarını ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.coordinates import usak_mahalleleri_getir, koordinat_listesi_getir, mahalle_isimleri_getir
from core.matrix_utils import mesafe_matrisi_olustur
from core.ant_algorithm import KarincaKolonisiAlgoritmasi
from visual.plotting import haritada_rotayi_ciz, iterasyon_grafigi_ciz


def api_key_al():
    """
    API key'i .streamlit/secrets.toml dosyasından alır.
    
    Returns:
        str: API key veya None
    """
    try:
        if 'google_maps_api_key' in st.secrets:
            return st.secrets['google_maps_api_key']
    except:
        pass
    
    return None


# Sayfa yapılandırması
st.set_page_config(
    page_title="UsakYolOptimizasyon - Uşak İli Arıza Giderme Rotası",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Modern CSS tema
st.markdown("""
<style>
    /* Ana renkler */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Uşak görseli için kart */
    .usak-hero {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Görsel stil */
    img {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Genel sayfa stilleri */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metrik kartları */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    /* Sidebar stil */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Buton stilleri */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Başlık stilleri */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 600;
    }
    
    /* Başarı mesajları */
    .stSuccess {
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    
    /* Bilgi mesajları */
    .stInfo {
        background-color: #d1ecf1;
        border-color: #bee5eb;
    }
    
    /* Streamlit header, menü ve footer'ı tamamen gizle */
    header {visibility: hidden !important; height: 0 !important;}
    footer {visibility: hidden !important; height: 0 !important;}
    #MainMenu {visibility: hidden !important; height: 0 !important;}
    
    /* Deploy butonu ve toolbar */
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stDeployButton {display: none !important;}
    
    /* Hamburger menü ve ayarlar butonu */
    button[title="Settings"],
    button[title="View app source"],
    button[kind="header"] {display: none !important;}
    
    /* Yüzen emoji animasyonu - Streamlit'in başlangıç dekorasyonu */
    [data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    iframe[title="stDecoration"] {display: none !important;}
    
    /* Tüm header elementlerini gizle */
    .stApp > header {display: none !important;}
    header[data-testid="stHeader"] {display: none !important;}
    
    /* Sidebar üzerindeki menü butonu */
    [data-testid="stSidebar"] [data-testid="stHeader"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Hero bölümü - Uşak görseli
col_hero1, col_hero2 = st.columns([1, 1])

with col_hero1:
    st.markdown("""
    <div class="main-header">
        <h1>Karınca Kolonisi Algoritması</h1>
        <p>Yol Optimizasyonu ile Arıza Giderme Rotası</p>
    </div>
    """, unsafe_allow_html=True)

with col_hero2:
    try:
        resim_yolu = os.path.join(os.path.dirname(__file__), "img", "usak-gezilecek-yerler-800x400.jpg")
        if os.path.exists(resim_yolu):
            st.image(resim_yolu, use_container_width=True, caption="Uşak İli")
    except Exception as e:
        pass

st.markdown("### Uşak İli - Elektrik Firması Arıza Giderme Rotası Optimizasyonu")

st.markdown("---")

# Sidebar - Parametreler
st.sidebar.header("Algoritma Parametreleri")

# Karınca sayısı
karinca_sayisi = st.sidebar.slider(
    "Karınca Sayısı",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="Her iterasyonda oluşturulacak karınca sayısı"
)

# Alpha (Feromon önemi)
alpha = st.sidebar.slider(
    "Alpha (Feromon Önemi)",
    min_value=0.1,
    max_value=3.0,
    value=1.0,
    step=0.1,
    help="Feromon önemini kontrol eder. Yüksek değer = feromon daha önemli"
)

# Beta (Mesafe önemi)
beta = st.sidebar.slider(
    "Beta (Mesafe Önemi)",
    min_value=0.1,
    max_value=5.0,
    value=2.0,
    step=0.1,
    help="Mesafe önemini kontrol eder. Yüksek değer = mesafe daha önemli"
)

# Buharlaşma oranı
buharlasma_orani = st.sidebar.slider(
    "Buharlaşma Oranı",
    min_value=0.1,
    max_value=0.9,
    value=0.5,
    step=0.05,
    help="Her iterasyonda feromonun ne kadarının buharlaşacağı"
)

# İterasyon sayısı
iterasyon_sayisi = st.sidebar.slider(
    "İterasyon Sayısı",
    min_value=10,
    max_value=500,
    value=100,
    step=10,
    help="Algoritmanın çalışacağı iterasyon sayısı"
)

st.sidebar.markdown("---")

# API Key'i dosyadan al
api_key = api_key_al()

# API Key durumunu sidebar'da göster
if api_key:
    st.sidebar.success("Google Maps API Key bulundu")
else:
    st.sidebar.info("API Key bulunamadı - Mock Mode aktif (Öklid mesafesi)")

st.sidebar.markdown("---")

# Çalıştır butonu
calistir = st.sidebar.button("Algoritmayı Çalıştır", type="primary", use_container_width=True)

# Ana içerik
st.markdown("""
### Uşak İli Mahalleleri
Aşağıdaki 15 mahallede arıza giderme rotası oluşturulacaktır.
""")

# Mahalle bilgilerini göster
mahalleler = usak_mahalleleri_getir()
mahalle_df = pd.DataFrame(mahalleler)

# İki sütunlu layout
col1, col2 = st.columns([2, 1])

with col1:
    st.dataframe(mahalle_df, use_container_width=True, hide_index=True)

with col2:
    st.info(f"**Toplam Nokta Sayısı:** {len(mahalleler)}\n\n**Başlangıç Noktası:** Merkez")

st.markdown("---")

# Algoritmayı çalıştır
if calistir:
    with st.spinner("Optimizasyon yapılıyor... Lütfen bekleyin."):
        # Koordinatları al
        koordinatlar = koordinat_listesi_getir()
        mahalle_isimleri = mahalle_isimleri_getir()
        
        # Mesafe matrisini oluştur
        st.info("Mesafe matrisi hesaplanıyor...")
        mesafe_matrisi, gercek_mesafe_kullanildi = mesafe_matrisi_olustur(koordinatlar, api_key)
        
        if gercek_mesafe_kullanildi:
            st.success("Google Maps API ile gerçek mesafeler kullanıldı")
        else:
            st.warning("Mock Mode: Öklid mesafesi kullanılıyor")
        
        # ACO algoritmasını oluştur ve çalıştır
        st.info("Karınca Kolonisi Algoritması çalıştırılıyor...")
        
        aco = KarincaKolonisiAlgoritmasi(
            mesafe_matrisi=mesafe_matrisi,
            karinca_sayisi=karinca_sayisi,
            alpha=alpha,
            beta=beta,
            buharlasma_orani=buharlasma_orani,
            iterasyon_sayisi=iterasyon_sayisi
        )
        
        en_iyi_rota, en_iyi_mesafe, iterasyon_gecmisi = aco.calistir()
        
        # Sonuçları göster
        st.success("Optimizasyon tamamlandı!")
        
        st.markdown("---")
        
        # Haritada rotayı çiz
        haritada_rotayi_ciz(koordinatlar, en_iyi_rota, mahalle_isimleri, en_iyi_mesafe)
        
        st.markdown("---")
        
        # İterasyon grafiğini çiz
        iterasyon_grafigi_ciz(iterasyon_gecmisi)
        
        # Sonuç özeti
        st.markdown("### Sonuç Özeti")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("En İyi Mesafe", f"{en_iyi_mesafe:.2f} km")
        
        with col2:
            st.metric("Kullanılan Karınca Sayısı", karinca_sayisi)
        
        with col3:
            st.metric("İterasyon Sayısı", iterasyon_sayisi)
        
        with col4:
            st.metric("Ziyaret Edilen Nokta", len(mahalleler))

elif not calistir:
    # Başlangıç mesajı
    st.info("Sol taraftaki parametreleri ayarlayıp 'Algoritmayı Çalıştır' butonuna tıklayın.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Karınca Kolonisi Algoritması ile Yol Optimizasyonu | Uşak İli Arıza Giderme Rotası</small>
</div>
""", unsafe_allow_html=True)

