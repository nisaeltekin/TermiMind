"""main.py - TermiMind komut satiri girisi. Tum parcalari birbirine baglar."""

import os
import subprocess
from typing import List

import psutil
import typer
from rich.console import Console

from arayuz import goster_ve_onayla
from baglam import baglam_topla
from gemma import gemma_sor
from maskeleme import maskele

app = typer.Typer(add_completion=False)
console = Console()


def kabuk_tespit():
    try:
        ust = psutil.Process().parent()
        for _ in range(6):
            if ust is None:
                break
            ad = ust.name().lower()
            if "pwsh" in ad or "powershell" in ad:
                return "PowerShell"
            if ad.startswith("cmd"):
                return "CMD"
            ust = ust.parent()
    except Exception:
        pass
    return "CMD"


def git_durumu():
    try:
        sonuc = subprocess.run(
            "git status -sb",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if sonuc.returncode == 0:
            return maskele(sonuc.stdout)
    except Exception:
        pass
    return ""


def komut_sor_baglami(istek):
    return {
        "mod": "komut_sor",
        "komut": maskele(istek),
        "cikti": "",
        "hata_kodu": 0,
        "klasor": maskele(os.getcwd()),
        "kabuk": kabuk_tespit(),
        "git": git_durumu(),
    }


@app.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
def ana(
    komut: List[str] = typer.Argument(
        ..., help="Hata modu: calistirilacak komut. --sor ile: ne yapmak istedigin."
    ),
    sor: bool = typer.Option(
        False, "--sor", "-s", help="Unuttugun komutu sor (komutu calistirmaz)."
    ),
):
    if sor:
        baglam = komut_sor_baglami(" ".join(komut))
    else:
        console.print("[dim]Komut çalıştırılıyor...[/dim]")
        baglam = baglam_topla(subprocess.list2cmdline(komut))
        baglam["mod"] = "hata"
        if baglam["cikti"]:
            console.print(baglam["cikti"], markup=False, highlight=False)
        if baglam["hata_kodu"] == 0:
            console.print("[green]Komut başarıyla çalıştı, Gemma'ya gerek yok.[/green]")
            raise typer.Exit(0)

    with console.status("Gemma düşünüyor..."):
        cevap = gemma_sor(baglam)
    goster_ve_onayla(cevap)


if __name__ == "__main__":
    app()