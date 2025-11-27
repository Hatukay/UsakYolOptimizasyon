"""
Karınca Kolonisi Optimizasyonu (ACO) Algoritması
Traveling Salesman Problem (TSP) için optimize edilmiş implementasyon.
"""

import numpy as np
import random
from typing import List, Tuple


class KarincaKolonisiAlgoritmasi:
    """
    Karınca Kolonisi Algoritması sınıfı.
    TSP problemi için en kısa rotayı bulur.
    """
    
    def __init__(
        self, 
        mesafe_matrisi: np.ndarray,
        karinca_sayisi: int = 10,
        alpha: float = 1.0,  # Feromon önemi
        beta: float = 2.0,   # Mesafe önemi
        buharlasma_orani: float = 0.5,
        iterasyon_sayisi: int = 100,
        baslangic_feromon: float = 1.0
    ):
        """
        Args:
            mesafe_matrisi: n x n mesafe matrisi
            karinca_sayisi: Her iterasyondaki karınca sayısı
            alpha: Feromon önemi parametresi (ne kadar yüksek o kadar feromon önemli)
            beta: Mesafe önemi parametresi (ne kadar yüksek o kadar mesafe önemli)
            buharlasma_orani: Feromon buharlaşma oranı (0-1 arası)
            iterasyon_sayisi: Algoritmanın çalışacağı iterasyon sayısı
            baslangic_feromon: Başlangıç feromon değeri
        """
        self.mesafe_matrisi = mesafe_matrisi
        self.n = len(mesafe_matrisi)
        self.karinca_sayisi = karinca_sayisi
        self.alpha = alpha
        self.beta = beta
        self.buharlasma_orani = buharlasma_orani
        self.iterasyon_sayisi = iterasyon_sayisi
        self.baslangic_feromon = baslangic_feromon
        
        # Feromon matrisi (başlangıçta tüm değerler eşit)
        self.feromon_matrisi = np.ones((self.n, self.n)) * baslangic_feromon
        
        # En iyi çözüm
        self.en_iyi_rota = None
        self.en_iyi_mesafe = float('inf')
        
        # İterasyon geçmişi (grafik için)
        self.iterasyon_gecmisi = []
    
    def rota_mesafesi_hesapla(self, rota: List[int]) -> float:
        """
        Verilen rotanın toplam mesafesini hesaplar.
        
        Args:
            rota: Ziyaret edilecek noktaların sırası (örn: [0, 3, 1, 2, 0])
        
        Returns:
            float: Toplam mesafe (km)
        """
        toplam_mesafe = 0
        for i in range(len(rota) - 1):
            toplam_mesafe += self.mesafe_matrisi[rota[i]][rota[i + 1]]
        return toplam_mesafe
    
    def olasilik_hesapla(self, mevcut_nokta: int, ziyaret_edilmis: set) -> np.ndarray:
        """
        Bir karıncanın bir sonraki noktayı seçme olasılıklarını hesaplar.
        
        Args:
            mevcut_nokta: Karıncanın bulunduğu nokta
            ziyaret_edilmis: Zaten ziyaret edilmiş noktalar kümesi
        
        Returns:
            np.ndarray: Her nokta için seçilme olasılığı
        """
        olasiliklar = np.zeros(self.n)
        
        for i in range(self.n):
            if i == mevcut_nokta or i in ziyaret_edilmis:
                olasiliklar[i] = 0  # Aynı nokta veya ziyaret edilmiş noktalar
            else:
                # Feromon ve mesafe kombinasyonu
                mesafe = self.mesafe_matrisi[mevcut_nokta][i]
                if mesafe == 0:
                    olasiliklar[i] = 0
                else:
                    feromon = self.feromon_matrisi[mevcut_nokta][i] ** self.alpha
                    cekicilik = (1.0 / mesafe) ** self.beta  # Mesafe ne kadar kısa o kadar çekici
                    olasiliklar[i] = feromon * cekicilik
        
        # Normalizasyon
        toplam = np.sum(olasiliklar)
        if toplam > 0:
            olasiliklar = olasiliklar / toplam
        
        return olasiliklar
    
    def karinca_rota_olustur(self) -> Tuple[List[int], float]:
        """
        Bir karıncanın rastgele bir rota oluşturmasını simüle eder.
        
        Returns:
            tuple: (rota, mesafe) - rota başlangıç noktasıyla biter
        """
        baslangic = 0  # Her zaman merkez (0. indeks) başlangıç
        rota = [baslangic]
        ziyaret_edilmis = {baslangic}
        
        # Tüm noktaları ziyaret et
        while len(ziyaret_edilmis) < self.n:
            mevcut_nokta = rota[-1]
            olasiliklar = self.olasilik_hesapla(mevcut_nokta, ziyaret_edilmis)
            
            # Olasılıklara göre sonraki noktayı seç
            sonraki_nokta = np.random.choice(self.n, p=olasiliklar)
            rota.append(sonraki_nokta)
            ziyaret_edilmis.add(sonraki_nokta)
        
        # Merkeze dön
        rota.append(baslangic)
        mesafe = self.rota_mesafesi_hesapla(rota)
        
        return rota, mesafe
    
    def feromon_guncelle(self, rota: List[int], mesafe: float):
        """
        Bir rotadan sonra feromon matrisini günceller.
        Daha kısa rotalar daha fazla feromon bırakır.
        
        Args:
            rota: Ziyaret edilen noktaların sırası
            mesafe: Rotanın toplam mesafesi
        """
        feromon_miktari = 1.0 / mesafe  # Mesafe ne kadar kısa, feromon o kadar fazla
        
        for i in range(len(rota) - 1):
            self.feromon_matrisi[rota[i]][rota[i + 1]] += feromon_miktari
    
    def feromon_buharlasma(self):
        """
        Feromon matrisinde buharlaşma işlemini gerçekleştirir.
        """
        self.feromon_matrisi *= (1.0 - self.buharlasma_orani)
    
    def calistir(self) -> Tuple[List[int], float, List[float]]:
        """
        ACO algoritmasını çalıştırır.
        
        Returns:
            tuple: (en_iyi_rota, en_iyi_mesafe, iterasyon_gecmisi)
        """
        print(f"Karınca Kolonisi Algoritması başlatılıyor...")
        print(f"   Karınca sayısı: {self.karinca_sayisi}")
        print(f"   Iterasyon sayısı: {self.iterasyon_sayisi}")
        
        for iterasyon in range(self.iterasyon_sayisi):
            # Her iterasyonda tüm karıncalar rota oluşturur
            karinca_rotalari = []
            karinca_mesafeleri = []
            
            for _ in range(self.karinca_sayisi):
                rota, mesafe = self.karinca_rota_olustur()
                karinca_rotalari.append(rota)
                karinca_mesafeleri.append(mesafe)
            
            # En iyi rotayı güncelle
            en_iyi_idx = np.argmin(karinca_mesafeleri)
            if karinca_mesafeleri[en_iyi_idx] < self.en_iyi_mesafe:
                self.en_iyi_rota = karinca_rotalari[en_iyi_idx].copy()
                self.en_iyi_mesafe = karinca_mesafeleri[en_iyi_idx]
            
            # Feromon buharlaşması
            self.feromon_buharlasma()
            
            # En iyi karıncanın rotası üzerine feromon ekle
            self.feromon_guncelle(self.en_iyi_rota, self.en_iyi_mesafe)
            
            # İterasyon geçmişine kaydet
            self.iterasyon_gecmisi.append(self.en_iyi_mesafe)
            
            if (iterasyon + 1) % 10 == 0:
                print(f"   Iterasyon {iterasyon + 1}/{self.iterasyon_sayisi}: En iyi mesafe = {self.en_iyi_mesafe:.2f} km")
        
        print(f"Algoritma tamamlandı! En iyi mesafe: {self.en_iyi_mesafe:.2f} km")
        
        return self.en_iyi_rota, self.en_iyi_mesafe, self.iterasyon_gecmisi

