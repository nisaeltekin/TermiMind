import time

import ollama

from baglam import baglam_topla
from gemma import MODEL, soru_hazirla, talimat_hazirla

b = baglam_topla("python demo-sirket/app.py")
b["mod"] = "hata"


def sn(r, alan):
    return round((getattr(r, alan, 0) or 0) / 1e9, 2)


for i in range(3):
    t = time.time()
    r = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": talimat_hazirla(b)},
            {"role": "user", "content": soru_hazirla(b)},
        ],
        think=False,
        format="json",
        options={"temperature": 0.2},
    )
    print(
        f"{i + 1}. deneme: toplam {time.time() - t:.1f} sn | "
        f"yükleme {sn(r, 'load_duration')} sn | "
        f"talimat {getattr(r, 'prompt_eval_count', 0)} token / {sn(r, 'prompt_eval_duration')} sn | "
        f"cevap {getattr(r, 'eval_count', 0)} token / {sn(r, 'eval_duration')} sn"
    )
