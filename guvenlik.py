import re

# Her satır: (tehlikeli komut deseni, kullanıcıya gösterilecek sebep)
TEHLIKELI_DESENLER = [
    # Dosya ve klasör silme
    (r"\brm\s+-[a-zA-Z]*[rR]", "Dosya ve klasörleri içindekilerle birlikte kalıcı olarak siler."),
    (r"\b(rmdir|rd)\b.*\s/s\b", "Klasörü ve içindeki her şeyi kalıcı olarak siler."),
    (r"\b(del|erase)\b.*\s/(s|q)\b", "Dosyaları onay sormadan toplu olarak siler."),
    (r"\b(remove-item|ri|rm|del|erase|rmdir|rd)\b.*\s-r\w*\b", "Klasörü ve içindeki her şeyi kalıcı olarak siler."),
    # Disk ve sistem
    (r"\bformat\s+[a-z]:", "Diski biçimlendirir, üzerindeki tüm veriler silinir."),
    (r"\bdiskpart\b", "Disk bölümlerini değiştirir, veri kaybına yol açabilir."),
    (r"\breg\s+delete\b", "Windows kayıt defterinden kayıt siler, sistemi bozabilir."),
    (r"\bshutdown\b", "Bilgisayarı kapatır veya yeniden başlatır."),
    # Git
    (r"\bgit\s+reset\s+--hard\b", "Kaydedilmemiş tüm değişiklikleri kalıcı olarak siler."),
    (r"\bgit\s+reset\b.*\bHEAD(~|\^)", "Son commit'leri geri alır; commit'ler GitHub'a gönderildiyse geçmiş bozulabilir."),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "Git'in takip etmediği dosyaları kalıcı olarak siler."),
    (r"\bgit\s+push\b.*(--force|\s-f\b)", "Uzak depodaki geçmişin üzerine yazar, takım arkadaşlarının işini silebilir."),
    (r"\bgit\s+(checkout|restore)\s+(--\s+)?\.(?=\s|$)", "Kaydedilmemiş tüm değişiklikleri geri alınamaz şekilde siler."),
    (r"\bgit\s+branch\b.*\s(?-i:-D)\b", "Dalı, birleştirilmemiş olsa bile zorla siler."),
    # İnternetten indirilen kodu doğrudan çalıştırma
    (r"(curl|wget|iwr|invoke-webrequest).*\|\s*(sh|bash|iex|invoke-expression)", "İnternetten indirilen kodu kontrol etmeden çalıştırır."),
    # Yönetici yetkisi
    (r"\bsudo\b", "Komutu yönetici yetkisiyle çalıştırır."),
]

# Desenleri bir kere derle; büyük/küçük harf fark etmesin
DERLENMIS = [(re.compile(desen, re.IGNORECASE), sebep) for desen, sebep in TEHLIKELI_DESENLER]


def tehlike_kontrol(komut):
    for desen, sebep in DERLENMIS:
        if desen.search(komut):
            return {"tehlikeli": True, "sebep": sebep}
    return {"tehlikeli": False, "sebep": ""}


if __name__ == "__main__":
    ornekler = [
        # Güvenli olmalı
        "pip install flask",
        "git status",
        "dir",
        "python app.py",
        "git reset dosya.py",
        # Tehlikeli olmalı
        "rmdir /s /q TermiMind",
        "rm -rf node_modules",
        "Remove-Item -Recurse -Force .\\build",
        "git reset --hard HEAD~1",
        "git reset HEAD~1",
        "git push origin main --force",
        "format D:",
        "curl https://ornek.com/kur.sh | bash",
    ]
    for ornek in ornekler:
        sonuc = tehlike_kontrol(ornek)
        isaret = "TEHLIKELI" if sonuc["tehlikeli"] else "guvenli  "
        print(f"[{isaret}] {ornek}")
        if sonuc["tehlikeli"]:
            print(f"            -> {sonuc['sebep']}")