# Monta a versão CURTA do AD 01 a partir do parte1.mp4 já tratado (sem Maya Verra) + fim B universal.
import subprocess, sys
from pathlib import Path
P = Path(__file__).parent
SEGS = [(0, 14.34), (243.84, 271.45), (326.42, 334.95), (342.45, 347.0), (353.24, 359.26)]
CAUDA = 0.25  # respiro: imagem segue, áudio some em fade
src = P / "parte1.mp4"
parts = []
for i, (a, b) in enumerate(SEGS):
    o = P / f"curto_s{i}.mp4"
    d = b - a + (CAUDA if i < len(SEGS) - 1 else 0.15)
    af = f"afade=t=in:d=0.03,afade=t=out:st={b - a:.3f}:d={d - (b - a):.3f}" if i < len(SEGS) - 1 else f"afade=t=in:d=0.03,afade=t=out:st={b-a:.3f}:d=0.15"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(src), "-af", af,
                    "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(o)], check=True)
    parts.append(o)
lst = P / "curto_lista.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
p1c = P / "parte1_curto.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(p1c)], check=True)
fx = P / "parte1_curto_fx.mp4"
subprocess.run([sys.executable, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\trocar_texto_tela.py",
                str(p1c), str(fx), "--de", "14.2", "--ate", "16.5", "--caixa", "60,900,660,1070", "--texto", "no era solo vanidad",
                "--ref", "15.3", "--px", "40", "--fonte", "Poppins-Medium.ttf"], check=True)
# p1c = fx  # desativado: a troca da legenda de 2 linhas deixava borrão no queixo; mantida a legenda original
saida = P.parent.parent / "AD 01 CURTO - LYMPHORIA-MENOPAUSIA-ES-LATAM.mp4"
pasta_c = P / "curto"; pasta_c.mkdir(exist_ok=True)
subprocess.run([sys.executable, str(P.parent / "montar_fim_universal.py"), str(pasta_c), str(p1c),
                str(P / "narr_fim_curto.mp3"), str(saida), "--res", "720"], check=True)
print("PRONTO", saida)
