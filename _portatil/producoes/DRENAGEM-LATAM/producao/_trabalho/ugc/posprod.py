# -*- coding: utf-8 -*-
"""Pós-produção dos UGC Lymphoria (HeyGen) -> receita do kit.

  python posprod.py NN

Lê ugc/cfg.json[NN] = {"angulo", "roteiro", "insertos": [[palavra_ancora, clipe, dur], ...]}
1) transcreve heygen_NN.mp4 por palavra (faster-whisper small, 4 threads)
2) cola os insertos de produto (só vídeo; o áudio dela continua) começando na palavra-âncora
3) gera um alinhamento no formato ElevenLabs com o TEXTO DO ROTEIRO (Linforia -> Lymphoria) e os tempos do whisper
4) escreve a receita e roda montar_ad.py (720p, selo COD, setas no "toca")
"""
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
SAIDA_DIR = AQUI.parent.parent  # producao\
SELO = ["ENVÍO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"]


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)


def whisper(media):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = m.transcribe(media, language="es", word_timestamps=True, vad_filter=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or []) if w.word.strip()]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode().strip())


def alinhar(roteiro, pal):
    """Tempo do whisper para cada palavra do roteiro (difflib nos tokens normalizados)."""
    rw = roteiro.split()
    a = [norm(w) for w in rw]
    b = [norm(w[0]) for w in pal]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    t = [None] * len(rw)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            t[blk.a + k] = (pal[blk.b + k][1], pal[blk.b + k][2])
    # trechos substituídos (ex.: "Linforia" ouvido como "Linfória"): distribui pelo trecho do whisper
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace" and j2 > j1:
            s0, s1 = pal[j1][1], pal[j2 - 1][2]
            n = i2 - i1
            for k in range(n):
                t[i1 + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
    # buracos restantes: interpola entre vizinhos
    for i in range(len(t)):
        if t[i] is None:
            prev = next((t[j][1] for j in range(i - 1, -1, -1) if t[j]), 0.0)
            nxt = next((t[j][0] for j in range(i + 1, len(t)) if t[j]), prev + 0.3)
            t[i] = (prev, max(prev + 0.05, min(nxt, prev + 0.4)))
    casados = sum(blk.size for blk in sm.get_matching_blocks())
    return rw, t, casados / max(1, len(rw))


def main(nn):
    cfg = json.load(open(AQUI / "cfg.json", encoding="utf-8"))[nn]
    wk = AQUI / f"ugc{nn}"
    wk.mkdir(exist_ok=True)
    src = AQUI / f"heygen_{nn}.mp4"
    narr_ali = AQUI / f"narr_{nn}.alinhamento.json"
    if narr_ali.exists():   # áudio do ElevenLabs enviado ao HeyGen: tempos exatos do alinhamento
        sys.path.insert(0, str(KIT))
        import legenda as LEG
        pal = LEG.palavras_por_alinhamento(str(narr_ali), float(cfg.get("offset", 0.0)))
    else:
        pal = whisper(str(src))
    json.dump(pal, open(wk / "palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
    total = dur(src)

    # --- insertos de produto
    rw, tempos, cobertura = alinhar(cfg["roteiro"], pal)
    print(f"cobertura do alinhamento: {cobertura:.0%}")
    ins = []
    for ancora, clipe, d in cfg["insertos"]:
        an = [norm(x) for x in ancora.split()]
        idx = next(i for i in range(len(rw)) if [norm(x) for x in rw[i:i + len(an)]] == an)
        t0 = round(tempos[idx][0], 3)
        ins.append((t0, min(d, dur(AQUI / "prod" / clipe), total - 4 - t0), clipe))
    ins.sort()
    for k in range(1, len(ins)):  # sem sobreposição
        assert ins[k][0] >= ins[k - 1][0] + ins[k - 1][1] + 1.0, ins
    args, fc, ult = ["ffmpeg", "-v", "error", "-y", "-i", str(src)], [], "[0:v]"
    fc.append(f"{ult}fps=30,scale=720:1280,setsar=1[b0]")
    ult = "[b0]"
    for k, (t0, d, clipe) in enumerate(ins, 1):
        args += ["-i", str(AQUI / "prod" / clipe)]
        fc.append(f"[{k}:v]trim=0:{d:.3f},setpts=PTS-STARTPTS+{t0}/TB[c{k}]")
        fc.append(f"{ult}[c{k}]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t0 + d - 0.001:.3f})'[b{k}]")
        ult = f"[b{k}]"
    corpo = wk / "corpo.mp4"
    args += ["-filter_complex", ";".join(fc), "-map", ult, "-map", "0:a", "-c:v", "libx264", "-crf", "15",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(corpo)]
    subprocess.run(args, check=True)
    json.dump(ins, open(wk / "insertos.json", "w", encoding="utf-8"), ensure_ascii=False)

    # --- alinhamento (formato ElevenLabs) com o texto do roteiro
    chars, ini, fim = [], [], []
    for w, (a, b) in zip(rw, tempos):
        w = re.sub(r"Linforia", "Lymphoria", w)
        n = len(w)
        for k, c in enumerate(w):
            chars.append(c)
            ini.append(a + (b - a) * k / n)
            fim.append(a + (b - a) * (k + 1) / n)
        chars.append(" ")
        ini.append(b)
        fim.append(b)
    ali = wk / "alinhamento.json"
    json.dump({"characters": chars, "character_start_times_seconds": ini, "character_end_times_seconds": fim},
              open(ali, "w", encoding="utf-8"), ensure_ascii=False)

    # selo a partir da 1ª menção de "envío"/"gratis"
    i_of = next(i for i, w in enumerate(rw) if norm(w) in ("envio", "gratis", "enviamos"))
    rec = {
        "saida": str(SAIDA_DIR / f"UGC {nn} - LYMPHORIA-{cfg['angulo']}-ES-LATAM.mp4"),
        "estilo": "drop",
        "corpo": str(corpo),
        "legenda": {"fonte": f"alinhamento:{ali}",
                    "chaves": ["Lymphoria", "miel", "gratis", "recibir", "noventa", "hierbas", "oficial"]},
        "selo": {"linhas": SELO, "x": 160, "y": 1225, "desde": round(tempos[i_of][0], 2)},
        "cta": {"palavra": "toca"},
        "resolucao": "720",
        "limite_mb": 30,
    }
    json.dump(rec, open(wk / "receita.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    subprocess.run([sys.executable, str(KIT / "montar_ad.py"), str(wk / "receita.json")], check=True, env=env,
                   cwd=str(KIT.parent))
    print("OK", rec["saida"])


if __name__ == "__main__":
    main(sys.argv[1])
