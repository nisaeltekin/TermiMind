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


def secim_sor(izinli):
    while True:
        secim = console.input("Seçimin (" + "/".join(izinli) + "): ").strip().lower()
        if secim in izinli:
            return secim
        console.print("[red]Sadece " + ", ".join(izinli) + " yaz.[/red]")


def goster_ve_onayla(cevap):
    tehlikeli, sebep = degerlendir(cevap)
    console.print(panel_olustur(cevap, tehlikeli, sebep))

    komut = cevap.get("komut", "")
    if not komut:
        return

    gizli_var = "***" in komut

    if gizli_var:
        console.print(
            "[bold yellow]Bu komutta maskelenmiş gizli bir değer (***) var. "
            "Çalıştırılırsa gerçek ayarının üzerine *** yazılır, bu yüzden [E] kapalı. "
            "Komutu kopyala ve *** yerine gizli değeri kendin yaz.[/bold yellow]"
        )
        console.print("[bold]\\[C][/bold] Kopyala   [bold]\\[A][/bold] Vazgeç")
        izinli = ("c", "a")
    else:
        console.print("[bold]\\[E][/bold] Çalıştır   [bold]\\[C][/bold] Kopyala   [bold]\\[A][/bold] Vazgeç")
        izinli = ("e", "c", "a")

    secim = secim_sor(izinli)

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
        "aciklama": "API anahtarı eksik olduğu için hata veriyor.",
        "komut": "set API_KEY=***",
        "risk": "dusuk",
        "ipucu": "Anahtarı kendin yazmalısın.",
    })
    goster_ve_onayla({
        "aciklama": "Normal, güvenli bir komut.",
        "komut": "echo pip install flask",
        "risk": "dusuk",
        "ipucu": "",
    })