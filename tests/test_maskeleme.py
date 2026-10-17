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