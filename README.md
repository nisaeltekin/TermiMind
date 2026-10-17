# 🧠 TermiMind

**Gemma 4 ile çalışan, yerel ve gizlilik odaklı terminal asistanı.** Hataları sade bir Türkçeyle açıklar, güvenli düzeltmeler önerir ve gizli bilgilerini hiçbir yere göndermez.

**Hacktoberfest Elazığ 2026**'da tek gecede geliştirildi.

## Neden TermiMind?

Terminalde bir hata alınca çoğumuz hata mesajını bir sohbet botuna yapıştırırız.
Ama terminal çıktısında API anahtarları, şifreler, IP adresleri ve kullanıcı adları
olabilir. TermiMind bu verilerin bilgisayarından çıkmasına gerek bırakmaz:

- Gemma 4 modeli tamamen yerelde (Ollama ile) çalışır, internet gerekmez.
- Gizli bilgiler modele gitmeden önce `***` ile maskelenir.
- Maliyet sıfırdır, kimsenin fiyatına bağımlı kalmazsın.
- Komut asla otomatik çalışmaz, her zaman senden onay ister.

Öğrenciler için bir faydası daha var: TermiMind sadece *ne* yazılacağını değil, hatanın *neden* olduğunu da Türkçe anlatır.

Orta segment bir öğrenci laptopunda (MSI, NVIDIA ekran kartı) `gemma4:e4b` **tamamen GPU'da** çalışıyor ve yaklaşık **7-10 saniyede** cevap veriyor.

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

Komut başarılı olursa Gemma'ya hiç sorulmaz. Komut, TermiMind'ın algıladığı kabukta (CMD veya PowerShell) çalıştırılır; Gemma da önerisini bu kabuğa göre yapar.

## Güvenlik katmanları

1. `maskeleme.py`: gizli bilgiler modele gitmeden önce maskelenir.
2. `gemma.py`: model komutun riskini tahmin eder.
3. `guvenlik.py`: kural tabanlı ikinci katman. Modele güvenlik kararını bırakmayız,
   tehlikeli komutlar model ne derse desin yakalanır.
4. `arayuz.py`: maskelenmiş değer (`***`) içeren komutlar **hiç çalıştırılamaz**, sadece kopyalanabilir. Model gerçek değeri hiç görmediği için komut eksiktir; kullanıcı `***` yerine gerçek değeri kendisi yazar.

### Neler maskeleniyor?

- `.env` tarzı gizli bilgiler: adında `KEY`, `SECRET`, `TOKEN`, `PASSWORD`, `PWD` ve Türkçe `SIFRE` / `PAROLA` geçenler
- Bilinen anahtar biçimleri (`ghp_…`, `github_pat_…`, `sk-…`)
- IP adresleri (`127.0.0.1` ve `0.0.0.0` hariç; bunlar gizli değil ve hata ayıklarken işe yarıyor)
- E-posta adresleri
- Dosya yollarındaki Windows kullanıcı adı

Hata ayıklama için önemli olan bilgiler (hata türü, port, satır numarası, dosya adı) **korunur**, böylece model yine de yardımcı olabilir.

### Gece yakaladığımız iki detay

- **Önce maskele, sonra kısalt.** Uzun çıktılar son 3000 karaktere kısaltılıyor, ama ancak maskelemeden *sonra*. Aksi halde kesim noktası `API_KEY=abc123` satırının ortasına denk gelip `Y=abc123` kısmını açıkta bırakabilirdi.
- **Görünmez karakterler maskelemeyi atlatamaz.** Test ederken kendi git e-posta adresimizde `@` işaretinden hemen önce görünmez bir kontrol karakteri (`\x91`) olduğunu fark ettik. Ekranda normal görünüyordu ama e-posta filtresinden kaçıyordu. Artık maskelemeden önce görünmez ve sıfır genişlikli karakterler temizleniyor; bunu bir test de güvence altına alıyor.

## Şirket demosu

[`demo-sirket/`](demo-sirket/) klasörü, hata mesajında ayarlarını sızdıran kurgusal bir lojistik şirketinin uygulamasını simüle ediyor (tüm bilgiler sahte).

```
python demo-sirket/app.py                  # önce: 5 gizli bilgi açıkta
python main.py python demo-sirket/app.py   # sonra: hepsi maskeli, hata yine açıklanıyor
```

Bizim denememizde Gemma `ping ***.***.***.*** -n 1` önerdi. Gerçek IP'yi göremediği için TermiMind **[E]** seçeneğini kapattı ve kullanıcıdan komutu kopyalayıp gerçek değeri kendisinin yazmasını istedi.

## Testler ve otomasyon

- Maskeleme ve tehlike tespiti için **30 pytest testi**. Gereksiz alarm vermediğimizden emin olmak için tehlikeliye benzeyen ama güvenli komutlar da test ediliyor (`rm dosya.txt`, `git push origin main`, `git branch -d`).
- **GitHub Actions**, her push ve pull request'te testleri otomatik çalıştırıyor.

```
python -m pytest -v
```

## Bilinen sınırlar

- Uzun süren veya kullanıcıdan girdi bekleyen komutlar (`npm run dev`, `input()` bekleyen betikler) takılı kalır, çünkü çıktı yakalanıyor.
- Sadece CMD ve PowerShell algılanıyor; Git Bash henüz desteklenmiyor.
- Tehlike kontrolü bir yasak listesi; her şeyi yakalayamaz. Asıl güvenlik önlemi, her komutun kullanıcı onayı gerektirmesi.
- Model sadece maskelenmiş veriyi gördüğü için bazen tam olarak doğru komutu öneremiyor (örneğin hiç görmediği bir IP'ye `ping` atamıyor). Bu ödünleşimi bilinçli olarak kabul ediyoruz.

## Proje yapısı ve modül sözleşmesi

```
main.py      → komut satırı girişi (typer)
baglam.py    → komutu çalıştırır; çıktı, hata kodu, klasör, kabuk ve git durumunu toplar
maskeleme.py → gizli bilgileri gizler
gemma.py     → Ollama üzerinden Gemma 4'e sorar, cevabı JSON olarak alır
guvenlik.py  → tehlikeli komutları Türkçe açıklamayla işaretler
arayuz.py    → rich arayüzü: panel, risk rengi, [E]/[C]/[A], çift onay
```

Projenin iki yarısı paralel olarak geliştirildi. Parçaların birbirine uyması için önce aşağıdaki sözleşme üzerinde anlaştık; ilk uçtan uca deneme hiçbir değişiklik gerektirmeden çalıştı.

**`baglam_topla(komut)`** şunu döndürür:
- `komut`: çalıştırılan komut
- `cikti`: komutun çıktısı veya hata mesajı
- `hata_kodu`: 0 ise başarılı, başka sayıysa hata
- `klasor`: komutun çalıştığı klasör
- `kabuk`: `"CMD"` veya `"PowerShell"`
- `git`: git durumu, git yoksa boş

Tüm metin alanları maskelenmiş gelir.

**`gemma_sor(baglam)`** şunu döndürür:
- `aciklama`: hatanın Türkçe açıklaması
- `komut`: önerilen düzeltme komutu (uygun komut yoksa boş)
- `risk`: `"dusuk"`, `"orta"` veya `"yuksek"`
- `ipucu`: bir dahakine dikkat edilecek şey

**`tehlike_kontrol(komut)`** şunu döndürür:
- `tehlikeli`: `True` veya `False`
- `sebep`: neden tehlikeli olduğunun Türkçe açıklaması (güvenliyse boş)

## Ekip

- [@nisaeltekin](https://github.com/nisaeltekin): Gemma entegrasyonu, prompt tasarımı, terminal arayüzü, komut satırı girişi
- [@Sumeyraadiyaman](https://github.com/Sumeyraadiyaman): bağlam toplama, maskeleme, güvenlik kontrolü, testler, otomasyon, şirket demosu

## Lisans

MIT