# TermiMind

Local, privacy-first terminal assistant powered by Gemma 4. Explains errors in plain Turkish, suggests safe fixes, and never sends your secrets anywhere.



&#x20;## Ortak Sözleşme



&#x20;### baglam\_topla(komut) şunu döndürür:

\- komut: çalıştırılan komut (metin)

\- cikti: komutun çıktısı veya hata mesajı (metin)

\- hata\_kodu: 0 ise başarılı, başka sayıysa hata (sayı)

\- klasor: komutun çalıştığı klasör (metin)

\- kabuk: "CMD" veya "PowerShell" (metin)

\- git: git durumu, git yoksa boş (metin)



&#x20;### gemma\_sor(baglam) şunu döndürür:

\- aciklama: hatanın Türkçe açıklaması

\- komut: önerilen düzeltme komutu

\- risk: "dusuk", "orta" veya "yuksek"

\- ipucu: bir dahakine dikkat edilecek şey



\### tehlike\_kontrol(komut) şunu döndürür:

\- tehlikeli: True veya False

\- sebep: neden tehlikeli olduğunun Türkçe açıklaması (güvenliyse boş)

## Neden TermiMind?

Terminalde bir hata alınca çoğumuz hata mesajını bir sohbet botuna yapıştırırız.
Ama terminal çıktısında API anahtarları, şifreler, IP adresleri ve kullanıcı adları
olabilir. TermiMind bu verilerin bilgisayarından çıkmasına gerek bırakmaz:

- Gemma 4 modeli tamamen yerelde (Ollama ile) çalışır, internet gerekmez.
- Gizli bilgiler modele gitmeden önce `***` ile maskelenir.
- Maliyet sıfırdır, kimsenin fiyatına bağımlı kalmazsın.
- Komut asla otomatik çalışmaz, her zaman senden onay ister.

## Kurulum

1. [Ollama](https://ollama.com)'yı kur, sonra modeli indir:

```
ollama pull gemma4:e4b
```

2. Repoyu klonla ve bağımlılıkları kur:

```
git clone https://github.com/nisaeltekin/TermiMind.git
cd TermiMind
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım

**Hata modu:** komutu TermiMind ile çalıştır, hata çıkarsa Gemma Türkçe açıklasın.

```
python main.py python app.py
```

**Unutulan komut modu:** ne yapmak istediğini yaz, komutu öğren (komut çalıştırılmaz).

```
python main.py --sor "son 5 commit'i göster"
```

Önerilen komut için üç seçenek sunulur: **[E]** Çalıştır, **[C]** Kopyala,
**[A]** Vazgeç. Tehlikeli komutlar (dosya silme, `git reset --hard` vb.) kırmızı
uyarıyla işaretlenir ve çalıştırmadan önce ikinci onay istenir.

## Güvenlik katmanları

1. `maskeleme.py`: gizli bilgiler modele gitmeden önce maskelenir.
2. `gemma.py`: model komutun riskini tahmin eder.
3. `guvenlik.py`: kural tabanlı ikinci katman. Modele güvenlik kararını bırakmayız,
   tehlikeli komutlar model ne derse desin yakalanır.

## Lisans

MIT

