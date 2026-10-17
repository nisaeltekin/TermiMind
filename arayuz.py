"""arayuz.py - Gemma'nin cevabini rich ile gosterir, kullaniciya sorar."""

import subprocess

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from baglam import kabuk_bul, komutu_calistir
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


def calistir(komut, kabuk):
    console.print("[dim]Çalıştırılıyor (" + kabuk + ")...[/dim]")
    try:
        sonuc = komutu_calistir(komut, kabuk)
    except Exception as hata:
        console.print("[red]Komut çalıştırılamadı: " + str(hata) + "[/red]", markup=True)
        return
    cikti = (sonuc.stdout or "") + (sonuc.stderr or "")
    if cikti.strip():
        console.print(cikti, markup=False, highlight=False)
    console.print("[dim]Bitti. Çıkış kodu: " + str(sonuc.returncode) + "[/dim]")


def secim_sor(izinli):
    while True:
        secim = console.input("Seçimin (" + "/".join(izinli) + "): ").strip().lower()
        if secim in izinli:
            return secim
        console.print("[red]Sadece " + ", ".join(izinli) + " yaz.[/red]")


def goster_ve_onayla(cevap, kabuk="CMD"):
    tehlikeli, sebep = degerlendir(cevap)
    console.print(panel_olustur(cevap, tehlikeli, sebep))

    komut = cevap.get("komut", "")
    if not komut:
        return

    if "***" in komut:
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
        calistir(komut, kabuk)
    else:
        console.print("[yellow]Vazgeçildi.[/yellow]")


if __name__ == "__main__":
    kabuk = kabuk_bul()
    console.print("Tespit edilen kabuk: " + kabuk)
    goster_ve_onayla({
        "aciklama": "API anahtarı eksik olduğu için hata veriyor.",
        "komut": "set API_KEY=***",
        "risk": "dusuk",
        "ipucu": "Anahtarı kendin yazmalısın.",
    }, kabuk)
    goster_ve_onayla({
        "aciklama": "Her iki kabukta da çalışan güvenli bir komut.",
        "komut": "echo merhaba",
        "risk": "dusuk",
        "ipucu": "",
    }, kabuk)
    goster_ve_onayla({
        "aciklama": "Bu komut sadece PowerShell'de çalışır.",
        "komut": "Write-Output powershell-calisti",
        "risk": "dusuk",
        "ipucu": "CMD'de hata vermesi normal.",
    }, kabuk)