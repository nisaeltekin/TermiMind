"""main.py - TermiMind komut satiri girisi. Tum parcalari birbirine baglar."""

import os
import subprocess
from typing import List

import typer
from rich.console import Console

from arayuz import goster_ve_onayla
from baglam import baglam_topla, git_durumu, kabuk_bul
from gemma import gemma_sor
from guvenlik import istek_tehlikeyi_gerektiriyor_mu, tehlike_kontrol
from maskeleme import maskele

app = typer.Typer(add_completion=False)
console = Console()


def komut_sor_baglami(istek):
    return {
        "mod": "komut_sor",
        "komut": maskele(istek),
        "cikti": "",
        "hata_kodu": 0,
        "klasor": maskele(os.getcwd()),
        "kabuk": kabuk_bul(),
        "git": maskele(git_durumu()),
    }


def belirsiz_istek_cevabi():
    return {
        "aciklama": (
            "İsteğin silme gibi geri alınamaz bir işlem içermiyor gibi görünüyor, "
            "ama model böyle bir komut önerdi. Tam olarak ne yapmak istiyorsun? "
            "Örneğin: yeniden adlandırmak, taşımak ya da silip yeniden kurmak."
        ),
        "komut": "",
        "risk": "dusuk",
        "ipucu": "İsteğini daha açık yazarsan doğru komutu önerebilirim.",
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
        komut_metni = komut[0] if len(komut) == 1 else subprocess.list2cmdline(komut)
        baglam = baglam_topla(komut_metni)
        baglam["mod"] = "hata"
        if baglam["cikti"]:
            console.print(baglam["cikti"], markup=False, highlight=False)
        if baglam["hata_kodu"] == 0:
            console.print("[green]Komut başarıyla çalıştı, Gemma'ya gerek yok.[/green]")
            raise typer.Exit(0)

    with console.status("Gemma düşünüyor..."):
        cevap = gemma_sor(baglam)
    if baglam["mod"] == "hata" and cevap["komut"].strip() == baglam["komut"].strip():
        cevap["komut"] = ""
    if (
        baglam["mod"] == "komut_sor"
        and cevap["komut"]
        and tehlike_kontrol(cevap["komut"])["tehlikeli"]
        and not istek_tehlikeyi_gerektiriyor_mu(" ".join(komut))
    ):
        cevap = belirsiz_istek_cevabi()
    goster_ve_onayla(cevap, baglam["kabuk"])


if __name__ == "__main__":
    app()