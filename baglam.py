import os
import subprocess


def git_durumu():
    # Git durumunu sor; klasör bir git reposu değilse boş metin döndür
    sonuc = subprocess.run("git status --short --branch", shell=True, capture_output=True, text=True)
    if sonuc.returncode != 0:
        return ""
    return sonuc.stdout


def baglam_topla(komut):
    # 1. Komutu çalıştır
    sonuc = subprocess.run(komut, shell=True, capture_output=True, text=True)

    # 2. Normal çıktı ile hata çıktısını birleştir
    cikti = sonuc.stdout + sonuc.stderr

    # 3. Sözleşmedeki isimlerle sözlüğü döndür
    return {
        "komut": komut,
        "cikti": cikti,
        "hata_kodu": sonuc.returncode,
        "klasor": os.getcwd(),
        "kabuk": "",
        "git": git_durumu(),
    }


if __name__ == "__main__":
    print(baglam_topla("python olmayan_dosya.py"))