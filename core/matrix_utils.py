"""
Mesafe Matrisi Hesaplama Modülü
Google Maps API kullanarak gerçek mesafeleri çeker.
API key yoksa veya hata olursa Mock Mode (Öklid mesafesi) kullanır.
"""

import os
import math
import numpy as np
from typing import List, Tuple, Optional
import googlemaps


def okleid_mesafesi_hesapla(nokta1: Tuple[float, float], nokta2: Tuple[float, float]) -> float:
    """
    İki nokta arasındaki Öklid mesafesini hesaplar (km cinsinden).
    
    Args:
        nokta1: (lat, lng) formatında ilk nokta
        nokta2: (lat, lng) formatında ikinci nokta
    
    Returns:
        float: İki nokta arası mesafe (km)
    """
    lat1, lng1 = nokta1
    lat2, lng2 = nokta2
    
    # Dünya yarıçapı (km)
    R = 6371.0
    
    # Dereceyi radyana çevir
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    
    # Haversine formülü
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    mesafe = R * c
    return mesafe


def google_maps_mesafe_matrisi_olustur(
    koordinatlar: List[Tuple[float, float]], 
    api_key: Optional[str] = None
) -> Optional[np.ndarray]:
    """
    Google Maps API kullanarak mesafe matrisi oluşturur.
    
    Args:
        koordinatlar: (lat, lng) tuple'larından oluşan liste
        api_key: Google Maps API anahtarı (None ise Mock Mode)
    
    Returns:
        np.ndarray: n x n mesafe matrisi (km), başarısız olursa None
    """
    if api_key is None:
        return None
    
    try:
        # Google Maps istemcisi oluştur
        gmaps = googlemaps.Client(key=api_key)
        
        n = len(koordinatlar)
        mesafe_matrisi = np.zeros((n, n))
        
        # Her nokta çifti için mesafe hesapla
        for i in range(n):
            for j in range(n):
                if i == j:
                    mesafe_matrisi[i][j] = 0
                else:
                    try:
                        # Directions API ile mesafe al
                        origin = f"{koordinatlar[i][0]},{koordinatlar[i][1]}"
                        destination = f"{koordinatlar[j][0]},{koordinatlar[j][1]}"
                        
                        result = gmaps.distance_matrix(
                            origins=[origin],
                            destinations=[destination],
                            mode="driving",
                            units="metric"
                        )
                        
                        # Mesafe bilgisini al (km)
                        if result['rows'][0]['elements'][0]['status'] == 'OK':
                            mesafe_metre = result['rows'][0]['elements'][0]['distance']['value']
                            mesafe_km = mesafe_metre / 1000.0
                            mesafe_matrisi[i][j] = mesafe_km
                        else:
                            # API hatası durumunda Öklid kullan
                            mesafe_matrisi[i][j] = okleid_mesafesi_hesapla(
                                koordinatlar[i], koordinatlar[j]
                            )
                    except Exception as e:
                        # Hata durumunda Öklid kullan
                        print(f"API hatası ({i}, {j}): {e}")
                        mesafe_matrisi[i][j] = okleid_mesafesi_hesapla(
                            koordinatlar[i], koordinatlar[j]
                        )
        
        return mesafe_matrisi
    
    except Exception as e:
        print(f"Google Maps API hatası: {e}")
        return None


def mesafe_matrisi_olustur(
    koordinatlar: List[Tuple[float, float]], 
    api_key: Optional[str] = None
) -> Tuple[np.ndarray, bool]:
    """
    Ana mesafe matrisi oluşturma fonksiyonu.
    Önce Google Maps API dener, başarısız olursa Mock Mode kullanır.
    
    Args:
        koordinatlar: (lat, lng) tuple'larından oluşan liste
        api_key: Google Maps API anahtarı (None ise Mock Mode)
    
    Returns:
        tuple: (mesafe_matrisi, gercek_mesafe_kullanildi) - gercek_mesafe_kullanildi True ise API başarılı
    """
    # Önce Google Maps API'yi dene
    if api_key:
        mesafe_matrisi = google_maps_mesafe_matrisi_olustur(koordinatlar, api_key)
        if mesafe_matrisi is not None:
            return mesafe_matrisi, True
    
    # API yoksa veya başarısız olduysa Mock Mode (Öklid mesafesi)
    print("Google Maps API kullanılamıyor. Mock Mode (Öklid mesafesi) aktif.")
    n = len(koordinatlar)
    mesafe_matrisi = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j:
                mesafe_matrisi[i][j] = 0
            else:
                mesafe_matrisi[i][j] = okleid_mesafesi_hesapla(koordinatlar[i], koordinatlar[j])
    
    return mesafe_matrisi, False

