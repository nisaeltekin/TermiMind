"""arayuz.py - Gemma'nin cevabini rich ile gosterir, kullaniciya sorar."""

import subprocess

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from guvenlik import tehlike_kontrol

console = Console()

RISK_RENK = {"dusuk": "green", "orta": "yellow", "yuksek": "red"}
RISK_ETIKET = {"dusuk": "DÜŞÜK", "orta": "ORTA", "yuksek": "YÜKSEK"}


def degerlendir(cevap):
    """Gemma'nin riski ve guvenlik.py'nin sonucundan birlesik karar verir."""
    komut = cevap.get("komut", "")
    sebep = ""
    tehlikeli = cevap.get("risk", "yuksek") == "yuksek"
    if komut:
        kontrol = tehlike_kontrol(komut)
        if kontrol.get("tehlikeli"):
            tehlikeli = True
            sebep = kontrol.get("sebep", "")
    return tehlikeli, sebep


def panel_olustur(cevap, tehlikeli, sebep):
    risk = "yuksek" if tehlikeli else cevap.get("risk", "yuksek")
    renk = RISK_RENK.get(risk, "red")

    parcalar = [Text(cevap.get("aciklama", ""))]

    komut = cevap.get("komut", "")
    if komut:
        parcalar.append(Text(""))
        parcalar.append(Text("Önerilen komut:", style="bold"))
        parcalar.append(Text("  " + komut, style="bold cyan"))

    if sebep:
        parcalar.append(Text(""))
        parcalar.append(Text("UYARI: " + sebep, style="bold red"))

    ipucu = cevap.get("ipucu", "")
    if ipucu:
        parcalar.append(Text(""))
        parcalar.append(Text("İpucu: " + ipucu, style="italic"))

    baslik = "TermiMind  |  Risk: " + RISK_ETIKET.get(risk, "YÜKSEK")
    return Panel(Group(*parcalar), title=baslik, border_style=renk, padding=(1, 2))


def kopyala(metin):
    try:
        subprocess.run("clip", input=metin.encode("utf-16"), check=True)
        console.print("[green]Komut panoya kopyalandı.[/green]")
    except Exception:
        console.print("[red]Kopyalanamadı. Komutu elle seçip kopyala.[/red]")


def calistir(komut):
    console.print("[dim]Çalıştırılıyor...[/dim]")
    sonuc = subprocess.run(komut, shell=True)
    console.print("[dim]Bitti. Çıkış kodu: " + str(sonuc.returncode) + "[/dim]")


def secim_sor():
    while True:
        secim = console.input("Seçimin (e/c/a): ").strip().lower()
        if secim in ("e", "c", "a"):
            return secim
        console.print("[red]Sadece e, c veya a yaz.[/red]")


def goster_ve_onayla(cevap):
    tehlikeli, sebep = degerlendir(cevap)
    console.print(panel_olustur(cevap, tehlikeli, sebep))

    komut = cevap.get("komut", "")
    if not komut:
        return

    console.print("[bold]\\[E][/bold] Çalıştır   [bold]\\[C][/bold] Kopyala   [bold]\\[A][/bold] Vazgeç")
    secim = secim_sor()

    if secim == "c":
        kopyala(komut)
    elif secim == "e":
        if tehlikeli:
            console.print("[bold red]Bu komut tehlikeli olabilir.[/bold red]")
            emin = console.input("Yine de çalıştırılsın mı? (evet yaz): ").strip().lower()
            if emin != "evet":
                console.print("[yellow]Vazgeçildi.[/yellow]")
                return
        calistir(komut)
    else:
        console.print("[yellow]Vazgeçildi.[/yellow]")


if __name__ == "__main__":
    goster_ve_onayla({
        "aciklama": "Python, 'flask' modülünü bulamadı çünkü kurulu değil.",
        "komut": "echo pip install flask",
        "risk": "dusuk",
        "ipucu": "Modül hatalarında genelde pip install ile kurulum gerekir.",
    })
    goster_ve_onayla({
        "aciklama": "Gemma bunu düşük riskli saydı ama guvenlik.py yakalamalı.",
        "komut": "rmdir /s /q yok_boyle_klasor",
        "risk": "dusuk",
        "ipucu": "Silmeden önce klasörün içeriğine bak.",
    })
    goster_ve_onayla({
        "aciklama": "Gemma'ya ulaşılamadı. Ollama açık mı kontrol et.",
        "komut": "",
        "risk": "yuksek",
        "ipucu": "",
    })