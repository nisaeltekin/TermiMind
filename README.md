# TermiMind

**Yerel, gizlilik öncelikli terminal asistanı — Gemma 4 ile çalışır.**
Hataları sade Türkçe açıklar, güvenli düzeltmeler önerir ve sırlarını hiçbir yere göndermez.

---

## Neden TermiMind?

Terminalde bir hata alınca çoğumuz hata mesajını bir sohbet botuna yapıştırırız.
Ama terminal çıktısında API anahtarları, şifreler, IP adresleri ve kullanıcı adları
olabilir. TermiMind bu verilerin bilgisayarından çıkmasına gerek bırakmaz:

- **Gemma 4** modeli tamamen yerelde (Ollama ile) çalışır, internet gerekmez.
- Gizli bilgiler modele gitmeden önce `***` ile maskelenir.
- **Maliyet sıfırdır**, kimsenin fiyatına bağımlı kalmazsın.
- Komut asla otomatik çalışmaz, her zaman senden onay ister.

---

## Kim ödeme yapar?

| Araç | Aylık maliyet |
|------|--------------|
| ChatGPT API | $20+ |
| GitHub Copilot | $10 |
| **TermiMind** | **$0** |

Model yerel çalıştığı için token ücreti yok, abonelik yok, veri sızıntısı yok.

---

## Kurulum

### 1. Ollama'yı kur, modeli indir

```bash
# https://ollama.com adresinden Ollama'yı kur, sonra:
ollama pull gemma4:e4b
```

### 2. Repoyu klonla ve bağımlılıkları kur

```bash
git clone https://github.com/nisaeltekin/TermiMind.git
cd TermiMind
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Kullanım

### Hata modu — komutu çalıştır, hata çıkarsa Gemma Türkçe açıklasın

```bash
python main.py python app.py
```

### Unutulan komut modu — ne yapmak istediğini yaz, komutu öğren

```bash
python main.py --sor "son 5 commit'i göster"
python main.py --sor "node_modules klasörünü sil"
```

Önerilen komut için üç seçenek sunulur:

- **[E]** Çalıştır
- **[C]** Kopyala
- **[A]** Vazgeç

Tehlikeli komutlar (`rm -rf`, `git reset --hard`, `***` içerenler vb.) **kırmızı uyarıyla** işaretlenir ve çalıştırmadan önce ikinci onay istenir.

---

## Güvenlik katmanları

```
Kullanıcı komutu
      │
      ▼
1. maskeleme.py   → API anahtarı, şifre, IP → *** ile değiştirilir
      │
      ▼
2. gemma.py       → Model risk tahmini: "dusuk" / "orta" / "yuksek"
      │
      ▼
3. guvenlik.py    → Kural tabanlı ikinci katman
                    (modele güvenlik kararını bırakmayız,
                     tehlikeli komutlar model ne derse desin yakalanır)
      │
      ▼
4. arayuz.py      → Onay kutusu: [E] / [C] / [A]
                    *** içeriyorsa [E] kapalı → sadece Kopyala / Vazgeç
```

---

## Demo senaryosu

```bash
# 1. Klasik hata yakalama
python main.py python yok_dosya.py

# 2. Tehlikeli komut — kırmızı kutu
python main.py --sor "yok_klasor klasörünü ve içindekileri sil"

# 3. Git yardımı
python main.py --sor "son commitimi geri al"

# 4. Şirket ortamı simülasyonu (demo-sirket/)
cd demo-sirket
python app.py
```

---

## Ortak Sözleşme (API)

### `baglam_topla(komut)` şunu döndürür:

| Alan | Tür | Açıklama |
|------|-----|----------|
| `komut` | metin | çalıştırılan komut |
| `cikti` | metin | komutun çıktısı veya hata mesajı |
| `hata_kodu` | sayı | 0 = başarılı, diğer = hata |
| `klasor` | metin | komutun çalıştığı klasör |
| `kabuk` | metin | `"CMD"` veya `"PowerShell"` |
| `git` | metin | git durumu (git yoksa boş) |

### `gemma_sor(baglam)` şunu döndürür:

| Alan | Tür | Açıklama |
|------|-----|----------|
| `aciklama` | metin | hatanın Türkçe açıklaması |
| `komut` | metin | önerilen düzeltme komutu |
| `risk` | metin | `"dusuk"` / `"orta"` / `"yuksek"` |
| `ipucu` | metin | bir dahakine dikkat edilecek şey |

### `tehlike_kontrol(komut)` şunu döndürür:

| Alan | Tür | Açıklama |
|------|-----|----------|
| `tehlikeli` | bool | `True` veya `False` |
| `sebep` | metin | neden tehlikeli (güvenliyse boş) |

### `goster_ve_onayla(cevap, kabuk)`

Onay arayüzünü gösterir. `cevap` = `gemma_sor` çıktısı, `kabuk` = `"CMD"` / `"PowerShell"`.

---

## Testler

```bash
pytest
```

---

## Lisans

MIT
