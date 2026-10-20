# -*- coding: utf-8 -*-
"""Revisão automática de um AD final antes de entregar. No vídeo inteiro:
- decodificação completa, resolução (9:16 720x1280/1080x1920, 4:5 720x900/1080x1350, 1:1 720x720/1080x1080;
  --formato 4:5 aceita só as do formato), áudio, duração e tamanho;
- whisper no idioma alvo (--idioma es), com tempo por segmento, + busca de termos proibidos (--proibidos);
- opcional: whisper num 2º idioma (--idioma-residual en) para achar fala residual do original (trechos que só
  fazem sentido nesse idioma) + detecção automática de idioma;
- folha de contato (1 quadro a cada --passo s) em <nome>_revisao.jpg;
- cortes de cena (scdet) a menos de 0,3 s um do outro = quadro solto;
- silêncio no fim e silêncios longos no meio (silencedetect);
- salto de pts no áudio (ffprobe packet=pts_time; o silencedetect NÃO pega) e áudio mais curto que o vídeo;
- setas de CTA: estão no último quadro? ficam em cima da faixa escura do rodapé (aviso/legenda)?
Saída: <nome>_revisao.txt + <nome>_revisao.jpg (ao lado do vídeo ou em --saida). Código de saída 1 se achou problema.

  python revisar_ad.py "AD 25 - X.mp4" --idioma es --idioma-residual en --proibidos "maya verra,60 días,tiktok"
  python revisar_ad.py "AD 06 - X.mp4" --proibidos proibidos.txt --passo 2 --saida _revisao
--proibidos: lista separada por vírgula ou arquivo .txt (um termo por linha). Acentos e maiúsculas são ignorados;
  termo com |, [, \\ ou ( é tratado como regex. Linhas com # no .txt são comentários.
--faixa y0,y1: posição da faixa do rodapé (px da saída) se a detecção automática não servir.
--lipsync "saida1.mp4:es1.mp3:pt1.mp4,saida2.mp4::pt2.mp4:320;280;400;440": roda o checar_lipsync.py em cada trecho
  com lipsync (saída do HeyGen etc. : áudio novo : trecho original [: rosto x;y;w;h de quem fala]). Áudio vazio = o da
  própria saída; sem original = sem o teste "a boca mudou". Critério principal = índice de pausa (boca fecha nas
  pausas da voz nova). Trecho REPROVADO vira PROBLEMA, AVISO vira aviso; com 2+ trechos também sai o índice do
  conjunto (todos os quadros juntos), que reprova o AD se passar de 0,75.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from comum import FORMATOS, checar_decodificacao, checar_resolucao, dur, formato_de, info, mb, run, tmpdir  # noqa: E402


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def ler_proibidos(arg: str | None) -> list[str]:
    if not arg:
        return []
    p = Path(arg)
    if p.suffix.lower() == ".txt" and p.exists():
        return [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    return [t.strip() for t in arg.split(",") if t.strip()]


def acha_termo(termo: str, linha_norm: str) -> bool:
    t = norm(termo)
    if any(c in t for c in "|[\\("):
        return re.search(t, linha_norm) is not None
    if not re.search(r"\w", t):            # "$" e afins: busca literal
        return t in linha_norm
    return re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", linha_norm) is not None


def ffmpeg_stderr(args: list[str]) -> str:
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--idioma", default="es")
    ap.add_argument("--idioma-residual", default=None, help="2º idioma p/ achar fala residual (ex.: en)")
    ap.add_argument("--proibidos", default=None, help='"a,b,c" ou arquivo .txt')
    ap.add_argument("--passo", type=float, default=1.0, help="s entre quadros da folha de contato")
    ap.add_argument("--saida", default=None, help="pasta dos relatórios (padrão: ao lado do vídeo)")
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--sem-whisper", action="store_true")
    ap.add_argument("--ate", type=float, default=None, help="transcreve só até este segundo")
    ap.add_argument("--faixa", default=None, help="y0,y1 da faixa do rodapé (px da saída)")
    ap.add_argument("--formato", default=None, choices=list(FORMATOS),
                    help="9:16 | 4:5 | 1:1: exige a resolução desse formato (padrão: aceita qualquer um dos 3)")
    ap.add_argument("--silencio-fim", type=float, default=1.0, help="s de silêncio no fim que viram problema")
    ap.add_argument("--lipsync", default=None,
                    help='"saida.mp4:audio_novo:original.mp4[:x;y;w;h],..." (checar_lipsync.py; rosto opcional)')
    a = ap.parse_args()

    v = Path(a.video).resolve()
    out_dir = Path(a.saida).resolve() if a.saida else v.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    txt_out = out_dir / f"{v.stem}_revisao.txt"
    jpg_out = out_dir / f"{v.stem}_revisao.jpg"
    L: list[str] = []
    probs: list[str] = []
    avisos: list[str] = []

    def log(s=""):
        print(s, flush=True)
        L.append(s)

    log(f"REVISÃO: {v.name}")

    # 1) formato e decodificação
    i = info(v)
    vs = next(s for s in i["streams"] if s["codec_type"] == "video")
    tem_a = any(s["codec_type"] == "audio" for s in i["streams"])
    d = float(i["format"]["duration"])
    res = f"{vs['width']}x{vs['height']}"
    fmt = formato_de(vs["width"], vs["height"])
    log(f"duração {d:.2f}s | {res} ({fmt or 'formato desconhecido'}) | {vs.get('r_frame_rate')} fps | "
        f"áudio: {'sim' if tem_a else 'NÃO'} | {mb(v):.1f} MB")
    res_ok, res_msg = checar_resolucao(vs["width"], vs["height"], a.formato)
    if not res_ok:
        probs.append(res_msg)
    if not tem_a:
        probs.append("sem faixa de áudio")
    err = checar_decodificacao(v)
    log("decodificação: " + ("OK" if not err else "ERRO " + err[:300]))
    if err:
        probs.append("erro de decodificação")

    # 2) áudio: salto de pts e duração
    if tem_a:
        pts = [float(x.strip(",")) for x in run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                                                 "packet=pts_time", "-of", "csv=p=0", v]).split() if x.strip(", ")]
        if len(pts) > 10:
            dl = np.diff(pts)
            med = float(np.median(dl))
            saltos = [(pts[k], float(x)) for k, x in enumerate(dl) if x > max(0.5, 10 * med)]
            log(f"pts do áudio: {len(pts)} pacotes, passo mediano {med * 1000:.1f} ms, saltos: "
                + (", ".join(f"{t:.2f}s (+{x:.2f}s)" for t, x in saltos) if saltos else "nenhum"))
            for t, x in saltos:
                probs.append(f"salto de pts no áudio em {t:.2f}s (+{x:.2f}s): fala dessincronizada dali em diante")
        da = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration",
                  "-of", "csv=p=0", v]).strip()
        if da and da != "N/A" and abs(float(da) - d) > 0.5:
            probs.append(f"áudio dura {float(da):.2f}s e o vídeo {d:.2f}s")

        # silêncio
        r = ffmpeg_stderr(["-i", str(v), "-vn", "-af", "silencedetect=noise=-45dB:d=0.7", "-f", "null", "-"])
        sil, ini = [], None
        for l in r.splitlines():
            if "silence_start" in l:
                ini = float(l.split("silence_start:")[1])
            if "silence_end" in l and ini is not None:
                sil.append((ini, float(l.split("silence_end:")[1].split("|")[0])))
                ini = None
        if ini is not None:
            sil.append((ini, d))
        log("silêncios (>0,7 s): " + (", ".join(f"{s0:.2f}-{s1:.2f}" for s0, s1 in sil) if sil else "nenhum"))
        if sil and sil[-1][1] >= d - 0.1 and d - sil[-1][0] > a.silencio_fim:
            probs.append(f"silêncio de {d - sil[-1][0]:.2f}s no fim (a partir de {sil[-1][0]:.2f}s)")
        for s0, s1 in sil:
            if s1 - s0 > 2.0 and s1 < d - 0.1:
                avisos.append(f"silêncio de {s1 - s0:.1f}s em {s0:.2f}s")

    # 3) cortes de cena (quadro solto)
    r = ffmpeg_stderr(["-i", str(v), "-an", "-vf", "scdet=threshold=10,metadata=print", "-f", "null", "-"])
    cortes = [float(l.split("lavfi.scd.time:")[1]) for l in r.splitlines() if "lavfi.scd.time:" in l]
    soltos = [(c0, c1) for c0, c1 in zip(cortes, cortes[1:]) if c1 - c0 < 0.3]
    log(f"cortes de cena: {len(cortes)} | pares a <0,3 s: " + (", ".join(f"{c0:.2f}/{c1:.2f}" for c0, c1 in soltos) or "nenhum"))
    for c0, c1 in soltos:
        probs.append(f"quadro solto? cortes em {c0:.2f}s e {c1:.2f}s ({(c1 - c0) * 1000:.0f} ms)")

    # 4) setas de CTA x faixa do rodapé
    cap = cv2.VideoCapture(str(v))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    Wf, Hf = int(cap.get(3)), int(cap.get(4))
    nfr = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    amostras = []
    for k in [nfr - 1, nfr - 8, nfr - 20, nfr - 35, nfr - 50]:
        if k < 0:
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, k)
        ok, fr = cap.read()
        if ok:
            amostras.append((k, fr))
    faixa = None
    if a.faixa:
        faixa = tuple(int(x) for x in a.faixa.split(","))
    elif amostras:
        # faixa escura e uniforme no terço de baixo, presente em todas as amostras
        esc = None
        for _, fr in amostras:
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
            linha = (g.mean(axis=1) < 35) & (g.std(axis=1) < 22)
            esc = linha if esc is None else (esc & linha)
        ys = np.where(esc[int(Hf * 0.6):])[0] + int(Hf * 0.6)
        if len(ys) >= 20:
            runs, s0 = [], ys[0]
            for p, q in zip(ys[:-1], ys[1:]):
                if q - p > 2:
                    runs.append((s0, p))
                    s0 = q
            runs.append((s0, ys[-1]))
            y0, y1 = max(runs, key=lambda r: r[1] - r[0])
            if y1 - y0 >= 20:
                faixa = (int(y0), int(y1))
    setas_ult = False
    sobre = False
    bbox_txt = "não achei vermelho saturado"
    for k, fr in amostras:
        hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 0] < 8) | (hsv[..., 0] > 172)) & (hsv[..., 1] > 150) & (hsv[..., 2] > 110)
        m[: int(Hf * 0.5)] = False
        ys, xs = np.where(m)
        if len(ys) < 300:
            continue
        y0, y1 = int(np.percentile(ys, 2)), int(np.percentile(ys, 98))
        bbox_txt = f"y {y0}-{y1}, x {int(np.percentile(xs, 2))}-{int(np.percentile(xs, 98))}"
        if k == nfr - 1:
            setas_ult = True
        if faixa and y1 > faixa[0] + 4 and y0 < faixa[1]:
            sobre = True
    log(f"setas (vermelho) no fim: {bbox_txt} | no último quadro: {'sim' if setas_ult else 'NÃO'} | "
        f"faixa escura do rodapé: {f'{faixa[0]}-{faixa[1]}' if faixa else 'não detectada'}")
    if not setas_ult:
        avisos.append("não achei setas vermelhas no último quadro (CTA deve ficar até o fim)")
    if sobre:
        probs.append("setas de CTA em cima da faixa escura do rodapé (suba as setas ou a faixa)")

    # 5) folha de contato
    passo = a.passo
    while d / passo > 400:
        passo *= 2
    ims, t = [], 0.0
    lw = 160
    while t < d:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, im = cap.read()
        if not ok:
            break
        im = cv2.resize(im, (lw, int(lw * Hf / Wf)))
        cv2.rectangle(im, (0, 0), (62, 20), (0, 0, 0), -1)
        cv2.putText(im, f"{int(t // 60)}:{int(t % 60):02d}", (3, 15), 0, 0.5, (0, 255, 255), 1)
        ims.append(im)
        t += passo
    if ims:
        cols = 10
        while len(ims) % cols:
            ims.append(np.zeros_like(ims[0]))
        folha = np.vstack([np.hstack(ims[k:k + cols]) for k in range(0, len(ims), cols)])
        cv2.imwrite(str(jpg_out), folha, [cv2.IMWRITE_JPEG_QUALITY, 80])
        log(f"folha de contato (1 q/{passo:g}s): {jpg_out}")

    # 6) whisper
    if not a.sem_whisper and tem_a:
        from faster_whisper import WhisperModel
        wk = tmpdir("rev_")
        wav = wk / "a.wav"
        run(["ffmpeg", *(["-t", str(a.ate)] if a.ate else []), "-i", v, "-vn", "-ac", "1", "-ar", "16000", wav])
        m = WhisperModel(a.modelo, device="cpu", compute_type="int8", cpu_threads=4)
        _, det = m.transcribe(str(wav), language=None)
        log(f"idioma detectado: {det.language} ({det.language_probability:.2f})")
        if det.language != a.idioma:
            avisos.append(f"idioma detectado {det.language} ({det.language_probability:.2f}), esperado {a.idioma}")
        segs, _ = m.transcribe(str(wav), language=a.idioma, vad_filter=False, condition_on_previous_text=False)
        alvo = [(s.start, s.end, s.text.strip()) for s in segs]
        log(f"\n=== transcrição ({a.idioma}) ===")
        for s0, s1, tx in alvo:
            log(f"{s0:7.2f}-{s1:6.2f} {tx}")
        termos = ler_proibidos(a.proibidos)
        ach = [(t, s0, tx) for s0, s1, tx in alvo for t in termos if acha_termo(t, norm(tx))]
        log("\n=== termos proibidos ===")
        log("\n".join(f"[{t}] {s0:.1f}s: {tx}" for t, s0, tx in ach) if ach else
            ("nenhum" if termos else "(nenhuma lista passada em --proibidos)"))
        for t, s0, tx in ach:
            probs.append(f"termo proibido '{t}' em {s0:.1f}s: {tx[:80]}")
        if alvo and d - alvo[-1][1] > 3.0:
            avisos.append(f"última fala termina em {alvo[-1][1]:.1f}s; vídeo vai até {d:.1f}s")
        if a.idioma_residual:
            segs2, _ = m.transcribe(str(wav), language=a.idioma_residual, vad_filter=False,
                                    condition_on_previous_text=False)
            log(f"\n=== transcrição residual ({a.idioma_residual}) ===")
            # Whisper forçado no 2º idioma TRADUZ a fala do idioma alvo, então comparar palavras não serve
            # (toda frase sairia "diferente"). Só é suspeito o trecho com fala onde a transcrição no idioma
            # alvo NÃO achou fala (buraco): sobra do áudio original que a narração nova não cobre.
            # Limite: fala original vazando POR BAIXO da narração nova não é detectada aqui; para isso vale o
            # "idioma detectado" acima e ouvir o fundo separado (demucs) antes de usar.
            def cobertura(ini, fim):
                tot = max(1e-6, fim - ini)
                return sum(max(0.0, min(fim, s1) - max(ini, s0)) for s0, s1, _ in alvo) / tot
            for s in segs2:
                tx = s.text.strip()
                ws = set(re.findall(r"\w+", norm(tx)))
                susp = (s.no_speech_prob < 0.4 and s.avg_logprob > -0.7 and len(ws) >= 3
                        and cobertura(s.start, s.end) < 0.5)
                log(f"{s.start:7.2f}-{s.end:6.2f} {'!! ' if susp else '   '}{tx}")
                if susp:
                    probs.append(f"possível fala em {a.idioma_residual} em {s.start:.1f}s: {tx[:80]}")

    # 7) lipsync por trecho
    if a.lipsync:
        import checar_lipsync as CL
        log("\n=== lipsync ===")
        res = []
        for saida, audio_novo, original, rosto in CL.ler_especificacao(a.lipsync):
            if not Path(saida).exists():
                probs.append(f"lipsync: arquivo não encontrado {saida}")
                continue
            try:
                r = CL.checar(saida, audio_novo, original, rosto=CL.ler_rosto(rosto) if rosto else None)
            except ValueError as e:
                probs.append(f"lipsync {Path(saida).name}: {e}")
                continue
            res.append(r)
            log(CL.formatar(r))
            if r["status"] == "REPROVADO":
                probs.append(f"lipsync {Path(saida).name}: {r['motivo']}")
            elif r["status"] == "AVISO":
                avisos.append(f"lipsync {Path(saida).name}: {r['motivo']}")
            if original is None:
                avisos.append(f"lipsync {Path(saida).name} checado sem o original (sem o teste 'a boca mudou')")
        if len(res) > 1:
            ip = CL.indice_agregado(res)
            st = CL.classificar_pausa(ip)
            log(f"índice de pausa do conjunto ({len(res)} trechos): {'-' if ip is None else f'{ip:.2f}'} -> {st or '-'}")
            if st == "REPROVADO":
                probs.append(f"lipsync do conjunto: a boca não fecha nas pausas da voz nova (índice de pausa {ip:.2f} "
                             f"> {CL.MAX_PAUSA_AVISO})")
            elif st == "AVISO":
                avisos.append(f"lipsync do conjunto: índice de pausa {ip:.2f} entre {CL.MAX_PAUSA_OK} e "
                              f"{CL.MAX_PAUSA_AVISO}")

    # resumo
    log("\n=== RESULTADO ===")
    for p in probs:
        log("PROBLEMA: " + p)
    for p in avisos:
        log("aviso: " + p)
    log("OK: nenhum problema encontrado" if not probs else f"{len(probs)} problema(s)")
    txt_out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"relatório: {txt_out}")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
