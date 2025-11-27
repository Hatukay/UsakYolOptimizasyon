# Usak Elektrik Ariza Rota Optimizasyonu (ACO Projesi)

**Ogrenci Adi Soyadi:** Hatukay Duran Alabay
**Ogrenci No:** 2112721062
**Senaryo:** 2 (Usak Ili - Elektrik Ariza Mudahale Rotasi)

---

## Proje Aciklamasi

Bu proje, Karinca Kolonisi Algoritmasi (Ant Colony Optimization - ACO) kullanilarak, Usak ilindeki 15 farkli mahallede meydana gelen arizalara tek bir teknik ekibin en kisa surede mudahale etmesini saglayan rotayi belirlemek amaciyla gelistirilmistir.

Uygulama, Gezgin Satici Problemi (Traveling Salesman Problem - TSP) tabanlidir ve gercek dunya mesafelerini kullanmak icin Google Maps API entegrasyonuna sahiptir.

### Senaryo Detaylari
- **Konum:** Usak Merkez ve cevre mahalleleri.
- **Hedef:** 15 farkli lokasyon (Mahalleler).
- **Amac:** Merkezden baslayip tum ariza noktalarini gezdikten sonra tekrar merkeze donen en dusuk maliyetli (mesafe) rotayi bulmak.

## Dosya Yapisi

Proje, asagidaki klasor yapisina uygun olarak moduler bir sekilde gelistirilmistir:

aco_yol_optimizasyonu/
├── main.py                 # Streamlit ana arayuzu ve uygulama giris noktasi
├── requirements.txt        # Gerekli Python kutuphaneleri
├── .gitignore              # Hassas dosyalari (secrets.toml) gizlemek icin
├── README.md               # Proje dokumantasyonu
├── .streamlit/
│   └── secrets.toml        # Google Maps API Anahtari (Git'e yuklenmez)
├── data/
│   └── coordinates.py      # Usak ili mahalle koordinat verileri
├── core/
│   ├── matrix_utils.py     # Mesafe matrisi hesaplama (API ve Mock Mode destegi)
│   └── ant_algorithm.py    # ACO algoritmasinin Python sinifi
└── visual/
    └── plotting.py         # PyDeck harita cizimi ve Plotly grafikleri

## Kurulum ve Calistirma

Projenin bilgisayarinizda calismasi icin asagidaki adimlari izleyin:

### 1. Kutuphaneleri Yukleyin
Terminali proje klasorunde acin ve gereksinimleri yukleyin:

pip install -r requirements.txt

### 2. API Anahtari (Guvenlik Adimi)
Google Maps API anahtarinizi kodun icine yazmak yerine guvenli bir sekilde .streamlit/secrets.toml dosyasina eklemelisiniz.

1. Proje ana dizininde .streamlit adinda bir klasor olusturun.
2. Icine secrets.toml adinda bir dosya olusturun.
3. Icerigi su sekilde duzenleyin:

GOOGLE_API_KEY = "BURAYA_KENDI_API_ANAHTARINIZI_YAZIN"

Not: API anahtari girilmezse veya kota asilirsa sistem otomatik olarak 'Mock Mode'a gecer ve kus ucusu mesafe (Haversine formulu) ile calismaya devam eder.

### 3. Uygulamayi Baslatin
Terminalde su komutu calistirin:

streamlit run main.py

## Parametreler ve Kullanim

Uygulama arayuzunde (Sidebar) asagidaki ACO parametreleri degistirilebilir:

* **Karinca Sayisi:** Her iterasyonda yola cikan ajan sayisi. (Onerilen: 20-50)
* **Iterasyon Sayisi:** Algoritmanin kac tur calisacagi. (Onerilen: 50-100)
* **Alpha:** Feromon izinin (tecrubenin) rota secimindeki etkisi.
* **Beta:** Mesafenin (yol kisaliginin) rota secimindeki etkisi.
* **Buharlasma Orani:** Feromonlarin zamanla silinme hizi. Yanlis rotalarin unutulmasi icin kullanilir.

## Ozellikler

* **Google Maps Entegrasyonu:** Gercek surus mesafeleri (Driving Mode) kullanilir.
* **Guvenlik:** API anahtarlari gizli dosya yapisi ile korunur, repoya yuklenmez.
* **Interaktif Harita:** PyDeck kutuphanesi ile rota harita uzerinde gorsellestirilir.
* **Yakinsama Grafigi:** Algoritmanin her adimda rotayi nasil iyilestirdigi grafiklenir.
* **Moduler Kod:** Okunabilir, Turkce yorum satirlari iceren temiz kod yapisi.

## Kullanilan Teknolojiler

* Python 3.x
* Streamlit (Web Arayuzu)
* Google Maps Services (Mesafe Matrisi)
* NumPy & Pandas (Veri Isleme)
* PyDeck & Plotly (Gorsellestirme)