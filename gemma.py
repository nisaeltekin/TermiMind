"""gemma.py - Gemma'ya soru sorar, cevabi sozluge cevirir."""

import json

import ollama

MODEL = "gemma4:e4b"
GECERLI_RISKLER = ("dusuk", "orta", "yuksek")
MAX_CIKTI_UZUNLUGU = 2000

RISK_DUZELTME = {
    "low": "dusuk",
    "medium": "orta",
    "high": "yuksek",
    "dusuk": "dusuk",
    "düşük": "dusuk",
    "dusunuk": "dusuk",
    "düşünük": "dusuk",
    "orta": "orta",
    "yuksek": "yuksek",
    "yüksek": "yuksek",
}


def cikti_kisalt(cikti):
    if len(cikti) > MAX_CIKTI_UZUNLUGU:
        return cikti[-MAX_CIKTI_UZUNLUGU:]
    return cikti


def talimat_hazirla(baglam):
    kabuk = baglam.get("kabuk", "CMD")
    mod = baglam.get("mod", "hata")

    ortak = (
        "Sen bir Windows terminal asistanısın. "
        "Kullanıcının kabuğu: " + kabuk + ". "
        "Önerdiğin komut bu kabukta çalışmalı (CMD ve PowerShell komutları farklıdır). "
        "Sadece JSON döndür, başka hiçbir şey yazma. "
        "JSON tam olarak şu 4 anahtarı içermeli: "
        "aciklama (Türkçe, kısa ve sade), "
        "komut (önerilen tek bir komut), "
        "risk (sadece şu 3 İngilizce değerden biri: low, medium, high), "
        "ipucu (bir dahaki sefere dikkat edilecek şey, Türkçe, tek cümle). "
        "Risk kuralı: sadece bilgi gösteren veya paket kuran komutlar low. "
        "Dosya değiştiren komutlar medium. "
        "Dosya silen, disk formatlayan, sistem ayarı değiştiren komutlar high."
    )

    if mod == "komut_sor":
        return ortak + (
            " Kullanıcı bir komutu unuttu ve ne yapmak istediğini anlattı. "
            "Ona uygun komutu öner. aciklama alanında komutun ne yaptığını anlat."
        )
    return ortak + (
        " Kullanıcının komutu hata verdi. "
        "aciklama alanında hatanın sebebini anlat, komut alanında düzeltmeyi öner."
    )


def soru_hazirla(baglam):
    mod = baglam.get("mod", "hata")
    if mod == "komut_sor":
        return (
            "Kullanıcının isteği: " + baglam.get("komut", "") + "\n"
            "Klasör: " + baglam.get("klasor", "") + "\n"
            "Git durumu: " + (baglam.get("git") or "git yok")
        )
    return (
        "Komut: " + baglam.get("komut", "") + "\n"
        "Hata kodu: " + str(baglam.get("hata_kodu", "")) + "\n"
        "Klasör: " + baglam.get("klasor", "") + "\n"
        "Git durumu: " + (baglam.get("git") or "git yok") + "\n"
        "Çıktı:\n" + cikti_kisalt(baglam.get("cikti", ""))
    )


def cevap_isle(ham):
    veri = json.loads(ham)
    sonuc = {
        "aciklama": str(veri.get("aciklama", "")).strip(),
        "komut": str(veri.get("komut", "")).strip(),
        "risk": RISK_DUZELTME.get(str(veri.get("risk", "")).strip().lower(), "yuksek"),
        "ipucu": str(veri.get("ipucu", "")).strip(),
    }
    if not sonuc["komut"]:
        raise ValueError("Model komut önermedi")
    return sonuc


def hata_cevabi(mesaj):
    return {"aciklama": mesaj, "komut": "", "risk": "yuksek", "ipucu": ""}


def gemma_sor(baglam):
    try:
        cevap = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": talimat_hazirla(baglam)},
                {"role": "user", "content": soru_hazirla(baglam)},
            ],
            think=False,
            format="json",
            options={"temperature": 0.2},
        )
        return cevap_isle(cevap["message"]["content"])
    except json.JSONDecodeError:
        return hata_cevabi("Model geçerli bir cevap üretemedi. Tekrar dene.")
    except ValueError:
        return hata_cevabi("Model bir komut öneremedi. İsteğini farklı yazmayı dene.")
    except Exception:
        return hata_cevabi(
            "Gemma'ya ulaşılamadı. Ollama açık mı ve gemma4:e4b indirilmiş mi kontrol et."
        )


if __name__ == "__main__":
    test = {
        "mod": "hata",
        "komut": "python app.py",
        "cikti": "ModuleNotFoundError: No module named 'flask'",
        "hata_kodu": 1,
        "klasor": "C:\\proje",
        "kabuk": "CMD",
        "git": "",
    }
    print(gemma_sor(test))
    test2 = {
        "mod": "komut_sor",
        "komut": "son 5 commit'i göster",
        "cikti": "",
        "hata_kodu": 0,
        "klasor": "C:\\proje",
        "kabuk": "CMD",
        "git": "On branch main",
    }
    print(gemma_sor(test2))
    test3 = {
        "mod": "komut_sor",
        "komut": "proje klasöründeki tüm .tmp dosyalarını sil",
        "cikti": "",
        "hata_kodu": 0,
        "klasor": "C:\\proje",
        "kabuk": "CMD",
        "git": "",
    }
    print(gemma_sor(test3))