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

