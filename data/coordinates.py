"""
Uşak İli Mahalle Koordinatları
15 mahallenin enlem ve boylam bilgilerini içerir.
"""


def usak_mahalleleri_getir():
    """
    Uşak ilindeki 15 mahallenin koordinatlarını döndürür.
    
    Returns:
        list: Her elemanı {'isim': str, 'lat': float, 'lng': float} formatında olan liste
    """
    mahalleler = [
        {'isim': 'Merkez', 'lat': 38.6735, 'lng': 29.4058},  # Merkez (başlangıç noktası)
        {'isim': 'Altıntaş', 'lat': 38.6833, 'lng': 29.4200},
        {'isim': 'Kurtuluş', 'lat': 38.6700, 'lng': 29.3900},
        {'isim': 'Yeşilova', 'lat': 38.6900, 'lng': 29.4100},
        {'isim': 'Atatürk', 'lat': 38.6800, 'lng': 29.4000},
        {'isim': 'Yeni Mahalle', 'lat': 38.6750, 'lng': 29.4150},
        {'isim': 'Cumhuriyet', 'lat': 38.6650, 'lng': 29.3950},
        {'isim': 'İstiklal', 'lat': 38.6850, 'lng': 29.3850},
        {'isim': 'Fatih', 'lat': 38.6600, 'lng': 29.4050},
        {'isim': 'Barbaros', 'lat': 38.6950, 'lng': 29.3950},
        {'isim': 'Çamlıbel', 'lat': 38.6550, 'lng': 29.4150},
        {'isim': 'Şehitler', 'lat': 38.6880, 'lng': 29.4000},
        {'isim': 'Göksu', 'lat': 38.6700, 'lng': 29.4250},
        {'isim': 'Huzur', 'lat': 38.6620, 'lng': 29.3880},
        {'isim': 'Zafer', 'lat': 38.6780, 'lng': 29.3920},
    ]
    return mahalleler


def koordinat_listesi_getir():
    """
    Sadece koordinat listesini döndürür (lat, lng tuple'ları).
    
    Returns:
        list: (lat, lng) tuple'larından oluşan liste
    """
    mahalleler = usak_mahalleleri_getir()
    return [(mahalle['lat'], mahalle['lng']) for mahalle in mahalleler]


def mahalle_isimleri_getir():
    """
    Mahalle isimlerini döndürür.
    
    Returns:
        list: Mahalle isimlerinden oluşan liste
    """
    mahalleler = usak_mahalleleri_getir()
    return [mahalle['isim'] for mahalle in mahalleler]

