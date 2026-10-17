import re

# Her satır: (aranacak desen, yerine konacak metin)
DESENLER = [
    # 1. .env satırları: API_KEY=..., DB_PASSWORD: ..., SECRET_TOKEN=...
    (re.compile(r"(?i)\b([A-Z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD|PASSWD|PWD)[A-Z0-9_]*)\s*([=:])\s*[^\s\"']+"), r"\1\2***"),
    # 2. Bilinen servis anahtarları
    (re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}"), "***"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "***"),
    # 3. IP adresleri
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "***.***.***.***"),
    # 4. E-posta adresleri
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "***@***"),
    # 5. Windows kullanıcı adı (tek veya çift ters bölüyle yazılmış yollar)
    (re.compile(r"(?i)(C:[\\/]+Users[\\/]+)[^\\/'\"\n]+"), r"\1***"),
]


def maskele(metin):
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