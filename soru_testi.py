import time

from gemma import gemma_sor
from guvenlik import tehlike_kontrol
from main import komut_sor_baglami

SORULAR = [
    # Bu gece sorun çıkaranlar
    "son 3 push'u göster",
    "node_modules klasörünü değiştir",
    "son commitlerimi nasıl silerim",
    # Net istekler (bozulmamalı)
    "son 3 commit'i göster",
    "node_modules klasörünü sil",
    "yüklü python paketlerini listele",
    "requirements.txt dosyasındaki paketleri kur",
    "yeni bir dal oluştur ve ona geç",
    # Farklı türde sorular
    "bu klasördeki en büyük 5 dosyayı göster",
    "8000 portunu hangi program kullanıyor",
]

for soru in SORULAR:
    t = time.time()
    cevap = gemma_sor(komut_sor_baglami(soru))
    sure = time.time() - t
    komut = cevap["komut"]
    tehlike = tehlike_kontrol(komut) if komut else {"tehlikeli": False}
    print(f"SORU    : {soru}")
    print(f"KOMUT   : {komut or '(boş, soru sordu)'}")
    print(f"RİSK    : {cevap['risk']}  |  guvenlik.py: {'TEHLİKELİ' if tehlike['tehlikeli'] else 'güvenli'}  |  {sure:.1f} sn")
    print(f"AÇIKLAMA: {cevap['aciklama']}")
    print("-" * 70)