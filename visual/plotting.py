"""
Görselleştirme Modülü
Streamlit haritası ve matplotlib grafikleri için fonksiyonlar içerir.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import List, Tuple


def haritada_rotayi_ciz(
    koordinatlar: List[Tuple[float, float]],
    rota: List[int],
    mahalle_isimleri: List[str],
    mesafe: float
):
    """
    Streamlit haritası üzerinde rotayı çizer.
    
    Args:
        koordinatlar: (lat, lng) tuple'larından oluşan liste
        rota: Ziyaret edilecek noktaların sırası
        mahalle_isimleri: Mahalle isimleri listesi
        mesafe: Toplam mesafe (km)
    """
    # Rota için koordinatları hazırla
    rota_koordinatlari = []
    rota_etiketleri = []
    
    for nokta_idx in rota:
        if nokta_idx < len(koordinatlar):
            lat, lng = koordinatlar[nokta_idx]
            rota_koordinatlari.append([lat, lng])
            rota_etiketleri.append(mahalle_isimleri[nokta_idx])
    
    # DataFrame oluştur
    df = pd.DataFrame(rota_koordinatlari, columns=['lat', 'lon'])
    df['mahalle'] = rota_etiketleri
    
    # Streamlit haritası
    st.subheader("Optimize Edilmiş Rota Haritası")
    st.caption(f"Toplam Mesafe: {mesafe:.2f} km")
    
    # Haritayı göster (rota çizgisiyle)
    st.map(
        df,
        zoom=12,
        use_container_width=True
    )
    
    # Rota detaylarını göster
    with st.expander("Rota Detayları"):
        rota_string = " → ".join(rota_etiketleri)
        st.write(f"**Rota:** {rota_string}")
        
        # Rota tablosu
        rota_data = {
            'Sıra': range(1, len(rota_etiketleri)),
            'Mahalle': rota_etiketleri[:-1],  # Son eleman başlangıçla aynı
            'Enlem': [koordinatlar[i][0] for i in rota[:-1]],
            'Boylam': [koordinatlar[i][1] for i in rota[:-1]]
        }
        rota_df = pd.DataFrame(rota_data)
        st.dataframe(rota_df, use_container_width=True, hide_index=True)


def iterasyon_grafigi_ciz(iterasyon_gecmisi: List[float]):
    """
    İterasyonlara göre maliyet (mesafe) düşüşünü gösteren çizgi grafiği çizer.
    
    Args:
        iterasyon_gecmisi: Her iterasyondaki en iyi mesafe listesi
    """
    if not iterasyon_gecmisi:
        st.warning("Grafik için veri bulunamadı.")
        return
    
    # Plotly ile interaktif grafik
    st.subheader("Algoritma Performans Grafiği")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(iterasyon_gecmisi) + 1)),
        y=iterasyon_gecmisi,
        mode='lines+markers',
        name='En İyi Mesafe',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=5)
    ))
    
    fig.update_layout(
        title='İterasyonlara Göre En İyi Mesafe Değişimi',
        xaxis_title='İterasyon',
        yaxis_title='Mesafe (km)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Özet istatistikler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Başlangıç Mesafesi",
            f"{iterasyon_gecmisi[0]:.2f} km"
        )
    
    with col2:
        st.metric(
            "En İyi Mesafe",
            f"{iterasyon_gecmisi[-1]:.2f} km"
        )
    
    with col3:
        iyilestirme = ((iterasyon_gecmisi[0] - iterasyon_gecmisi[-1]) / iterasyon_gecmisi[0]) * 100
        st.metric(
            "İyileştirme",
            f"%{iyilestirme:.1f}"
        )


def matplotlib_iterasyon_grafigi(iterasyon_gecmisi: List[float]) -> plt.Figure:
    """
    Matplotlib ile iterasyon grafiği oluşturur (alternatif).
    
    Args:
        iterasyon_gecmisi: Her iterasyondaki en iyi mesafe listesi
    
    Returns:
        plt.Figure: Matplotlib figür nesnesi
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(
        range(1, len(iterasyon_gecmisi) + 1),
        iterasyon_gecmisi,
        marker='o',
        markersize=3,
        linewidth=2,
        color='#1f77b4'
    )
    
    ax.set_xlabel('İterasyon', fontsize=12)
    ax.set_ylabel('Mesafe (km)', fontsize=12)
    ax.set_title('İterasyonlara Göre En İyi Mesafe Değişimi', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

