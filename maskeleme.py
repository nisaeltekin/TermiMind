import re
import unicodedata

# Terminal renk kodları (örn. \x1b[31m). Anahtar isminin arasına girip maskelemeyi bozmasınlar diye silinir.
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def gorunmezleri_temizle(metin):
    # Önce renk kodlarını sil, sonra tüm görünmez kontrol (Cc) ve biçim (Cf) karakterlerini at.
    # Satır sonu ve tab korunur. (\x91, \u200b, \u202e, \u2061 gibi karakterler bu kapsamda.)
    metin = ANSI.sub("", metin)
    return "".join(k for k in metin if k in "\n\r\t" or unicodedata.category(k) not in ("Cc", "Cf"))


# Her satır: (aranacak desen, yerine konacak metin)
DESENLER = [
    # 1. .env satırları: API_KEY=..., API_KEY="...", "api_key": "...", DB_SIFRE=...
    #    Adı Error/Exception/Warning ile biten hata isimleri hariç (örn. InvalidTokenError)
    (re.compile(r"(?i)\b(\w*(?:KEY|SECRET|TOKEN|PASSWORD|PASSWD|PWD|SIFRE|ŞIFRE|ŞİFRE|PAROLA|KULLANICI|USERNAME)\w*)(?<!ERROR)(?<!EXCEPTION)(?<!WARNING)([\"']?)(\s*[=:]\s*)(?:\"[^\"\n]*\"|'[^'\n]*'|[^\s\"']+)"), r"\1\2\3***"),
    # 2. Bearer token ve JWT
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*"), "Bearer ***"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"), "***"),
    # 3. Bilinen servis anahtarları (GitHub, OpenAI, GitLab, Slack, npm, AWS)
    (re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}"), "***"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "***"),
    (re.compile(r"\b(?:glpat-|xox[abprs]-|npm_)[A-Za-z0-9_-]{10,}"), "***"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "***"),
    # 4. IP adresleri (yerel 127.0.0.1 ve 0.0.0.0 hariç, bunlar gizli değil)
    (re.compile(r"\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b"), "***.***.***.***"),
    # 5. E-posta adresleri
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "***@***"),
    # 6. Windows kullanıcı adı (tek veya çift ters bölüyle yazılmış yollar)
    (re.compile(r"(?i)(C:[\\/]+Users[\\/]+)[^\\/'\"\n]+"), r"\1***"),
]


def maskele(metin):
    metin = gorunmezleri_temizle(metin)
    for desen, yerine in DESENLER:
        metin = desen.sub(yerine, metin)
    return metin


if __name__ == "__main__":
    ornekler = [
        "API_KEY=abc123xyz",
        'API_KEY="tirnakli-gizli-deger"',
        '{"api_key": "json-gizli-deger"}',
        "DB_PASSWORD: super-gizli-sifre",
        "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.abc123def",
        "Sunucuya baglanilamadi: 192.168.1.10",
        "Hata raporu: sumeyra@ornek.com",
        r"can't open file 'C:\Users\Huzur Bilgisayar\Desktop\TermiMind\app.py'",
    ]
    for ornek in ornekler:
        print(ornek)
        print("  ->", maskele(ornek))