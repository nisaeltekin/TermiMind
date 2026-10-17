import re

# Görünmez kontrol karakterleri (\x91 gibi) ve sıfır genişlikli boşluklar.
# Maskelemeyi atlatmasınlar diye en başta temizleniyor. Satır sonu, tab ve renk kodu (ESC) korunuyor.
GORUNMEZ = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1a\x1c-\x1f\x7f-\x9f\u200b-\u200f\u2060\ufeff]")

# Her satır: (aranacak desen, yerine konacak metin)
DESENLER = [
    # 1. .env satırları: API_KEY=..., DB_PASSWORD: ..., DB_SIFRE=...
    #    Adı Error/Exception/Warning ile biten hata isimleri hariç (örn. InvalidTokenError)
    (re.compile(r"(?i)\b(\w*(?:KEY|SECRET|TOKEN|PASSWORD|PASSWD|PWD|SIFRE|ŞIFRE|ŞİFRE|PAROLA|KULLANICI|USERNAME)\w*)(?<!ERROR)(?<!EXCEPTION)(?<!WARNING)\s*([=:])\s*[^\s\"']+"), r"\1\2***"),
    # 2. Bilinen servis anahtarları
    (re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}"), "***"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "***"),
    # 3. IP adresleri (yerel 127.0.0.1 ve 0.0.0.0 hariç, bunlar gizli değil)
    (re.compile(r"\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b"), "***.***.***.***"),
    # 4. E-posta adresleri
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "***@***"),
    # 5. Windows kullanıcı adı (tek veya çift ters bölüyle yazılmış yollar)
    (re.compile(r"(?i)(C:[\\/]+Users[\\/]+)[^\\/'\"\n]+"), r"\1***"),
]


def maskele(metin):
    metin = GORUNMEZ.sub("", metin)
    for desen, yerine in DESENLER:
        metin = desen.sub(yerine, metin)
    return metin


if __name__ == "__main__":
    ornekler = [
        "API_KEY=abc123xyz",
        "DB_PASSWORD: super-gizli-sifre",
        "token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
        "Sunucuya baglanilamadi: 192.168.1.10",
        "Hata raporu: sumeyra@ornek.com",
        r"can't open file 'C:\Users\Huzur Bilgisayar\Desktop\TermiMind\app.py'",
    ]
    for ornek in ornekler:
        print(ornek)
        print("  ->", maskele(ornek))