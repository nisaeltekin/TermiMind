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


def komutu_calistir(komut, kabuk):
    # Komutu kullanıcının kabuğunda çalıştır
    ayarlar = {"capture_output": True, "text": True, "errors": "replace"}
    if kabuk == "PowerShell":
        return subprocess.run(["powershell", "-NoProfile", "-Command", komut], **ayarlar)
    return subprocess.run(komut, shell=True, **ayarlar)


def git_durumu():
    # Git durumunu sor; klasör bir git reposu değilse boş metin döndür
    sonuc = subprocess.run("git status --short --branch", shell=True, capture_output=True, text=True, errors="replace")
    if sonuc.returncode != 0:
        return ""
    return sonuc.stdout


def baglam_topla(komut):
    kabuk = kabuk_bul()
    sonuc = komutu_calistir(komut, kabuk)
    cikti = sonuc.stdout + sonuc.stderr

    return {
        "komut": maskele(komut),
        "cikti": maskele(cikti),
        "hata_kodu": sonuc.returncode,
        "klasor": maskele(os.getcwd()),
        "kabuk": kabuk,
        "git": maskele(git_durumu()),
    }


if __name__ == "__main__":
    print(baglam_topla("python olmayan_dosya.py"))
    print(baglam_topla("echo API_KEY=abc123xyz"))