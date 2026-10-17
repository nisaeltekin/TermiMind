from pathlib import Path


def ayarlari_oku():
    ayarlar = {}
    dosya = Path(__file__).parent / "sirket.env"
    for satir in dosya.read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if satir and not satir.startswith("#") and "=" in satir:
            anahtar, deger = satir.split("=", 1)
            ayarlar[anahtar] = deger
    return ayarlar


ayarlar = ayarlari_oku()
print("Siparis servisi baslatiliyor...")
print(f"Ayarlar yuklendi: DB_SIFRE={ayarlar['DB_SIFRE']} API_KEY={ayarlar['API_KEY']}")
raise ConnectionError(
    f"Veritabanina baglanilamadi: {ayarlar['DB_HOST']}:5432 "
    f"(kullanici={ayarlar['DB_KULLANICI']}). Destek: {ayarlar['DESTEK_EPOSTA']}"
)