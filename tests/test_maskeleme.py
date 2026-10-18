from maskeleme import maskele


def test_env_anahtari_gizlenir():
    assert maskele("API_KEY=abc123xyz") == "API_KEY=***"


def test_github_tokeni_gizlenir():
    token = "ghp_" + "A" * 30
    assert token not in maskele(f"anahtarim {token}")


def test_ip_adresi_gizlenir():
    assert "192.168.1.10" not in maskele("Sunucuya baglanilamadi: 192.168.1.10")


def test_eposta_gizlenir():
    assert "sumeyra@ornek.com" not in maskele("Hata raporu: sumeyra@ornek.com")


def test_kullanici_adi_gizlenir():
    assert maskele(r"C:\Users\Huzur Bilgisayar\Desktop") == r"C:\Users\***\Desktop"


def test_normal_hata_mesaji_bozulmaz():
    metin = "ModuleNotFoundError: No module named 'flask'"
    assert maskele(metin) == metin


def test_turkce_sifre_gizlenir():
    assert maskele("DB_SIFRE=gizli123") == "DB_SIFRE=***"


def test_hata_ismi_bozulmaz():
    assert "Signature" in maskele("jwt.exceptions.InvalidTokenError: Signature has expired")


def test_yerel_ip_gizlenmez():
    assert "127.0.0.1" in maskele("Connection refused: 127.0.0.1:5432")


def test_gorunmez_karakter_maskelemeyi_atlatamaz():
    sonuc = maskele("250541012\x91@firat.edu.tr")
    assert "firat.edu.tr" not in sonuc


def test_tirnakli_degerler_gizlenir():
    assert "gercek" not in maskele('API_KEY="gercek-gizli-deger"')
    assert "gercek" not in maskele('{"api_key": "gercek-gizli-deger"}')
    assert "gizli" not in maskele("DB_PASSWORD='cok gizli sifre'")


def test_unicode_ve_renk_kodlari_maskelemeyi_atlatamaz():
    assert "gercek" not in maskele("API_\u2061KEY=gercek-gizli-deger")
    assert "gercek" not in maskele("API\u202e_KEY=gercek-gizli-deger")
    assert "gercek" not in maskele("API_\x1b[31mKEY=gercek-gizli-deger")


def test_bearer_ve_jwt_gizlenir():
    sonuc = maskele("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.abc123def")
    assert "eyJ" not in sonuc


def test_servis_tokenlari_gizlenir():
    for token in ("glpat-" + "A" * 20, "xoxb-" + "1" * 20, "npm_" + "B" * 30, "AKIA" + "C" * 16):
        assert token not in maskele("anahtar " + token)



def test_veritabani_kullanici_adi_gizlenir():
    assert "lojistik_app" not in maskele("Veritabanina baglanilamadi (kullanici=lojistik_app).")