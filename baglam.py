import subprocess


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
        "klasor": "",
        "kabuk": "",
        "git": "",
    }


if __name__ == "__main__":
    print(baglam_topla("python olmayan_dosya.py"))