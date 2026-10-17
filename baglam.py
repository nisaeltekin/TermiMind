import os
import subprocess

import psutil
from maskeleme import maskele


def kabuk_bul():
    # Programı başlatan pencereyi bulana kadar "ebeveyn" süreçlere bak
    try:
        surec = psutil.Process(os.getpid()).parent()
        while surec is not None:
            ad = surec.name().lower()
            if ad in ("powershell.exe", "pwsh.exe"):
                return "PowerShell"
            if ad == "cmd.exe":
                return "CMD"
            surec = surec.parent()
    except psutil.Error:
        pass
    return "CMD"


def metne_cevir(veri):
    # Önce UTF-8 dene (git gibi programlar), olmazsa Windows konsol kodlaması (dir gibi komutlar)
    for kodlama in ("utf-8", "oem"):
        try:
            return veri.decode(kodlama)
        except (UnicodeDecodeError, LookupError):
            continue
    return veri.decode("utf-8", errors="replace")


def komutu_calistir(komut, kabuk):
    # Komutu kullanıcının kabuğunda çalıştır, çıktıyı ham bayt olarak al
    if kabuk == "PowerShell":
        sonuc = subprocess.run(["powershell", "-NoProfile", "-Command", komut], capture_output=True)
    else:
        sonuc = subprocess.run(komut, shell=True, capture_output=True)
    sonuc.stdout = metne_cevir(sonuc.stdout)
    sonuc.stderr = metne_cevir(sonuc.stderr)
    return sonuc


def git_durumu():
    # Git durumunu sor; klasör bir git reposu değilse boş metin döndür
    sonuc = subprocess.run("git status --short --branch", shell=True, capture_output=True, text=True, errors="replace")
    if sonuc.returncode != 0:
        return ""
    return sonuc.stdout


SON_KARAKTER = 3000


def baglam_topla(komut):
    kabuk = kabuk_bul()
    sonuc = komutu_calistir(komut, kabuk)

    # Önce maskele, SONRA kısalt
    cikti = maskele(sonuc.stdout + sonuc.stderr)
    if len(cikti) > SON_KARAKTER:
        cikti = "...(önceki kısım kısaltıldı)...\n" + cikti[-SON_KARAKTER:]

    return {
        "komut": maskele(komut),
        "cikti": cikti,
        "hata_kodu": sonuc.returncode,
        "klasor": maskele(os.getcwd()),
        "kabuk": kabuk,
        "git": maskele(git_durumu()),
    }


if __name__ == "__main__":
    print(baglam_topla("python olmayan_dosya.py"))
    print(baglam_topla("echo API_KEY=abc123xyz"))