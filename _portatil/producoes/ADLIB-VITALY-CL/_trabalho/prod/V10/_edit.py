p='patch_rotulo.py'; s=open(p,encoding='utf-8').read()
s=s.replace('    cor = tuple(int(c) for c in np.median(reg[lum < np.percentile(lum, 60)], axis=0))','    cor = (29, 71, 52)   # verde da faixa do rótulo Lymphoria (antes: marrom do frasco Vitaly)')
s=s.replace('cor=(242, 232, 212, 255))','cor=(244, 242, 234, 255))')
open(p,'w',encoding='utf-8').write(s)
p='render_v10.py'; s=open(p,encoding='utf-8').read()
s=s.replace('p2 = T.ler_quadros(str(PROD / "P2_frasco_miel.mp4"))                                  # 90 q',
r'''p2 = T.ler_quadros(str(PROD / "P2_frasco_miel.mp4"))                                  # 90 q
FL = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
VF = "scale=720:1280:flags=lanczos,fps=30"
tk_card = [T.ler_quadros(str(FL / t), vf=VF, ss=0.2, t=3.0)[:89] for t in
           ("ad10/flora/t1_edit.mp4", "ad11/flora/t3_edit.mp4", "ad11/flora/t4_edit.mp4")]  # 3 x 89 q, sem texto''')
a=s.index('    elif K_BR1 <= k < K_CARD1:'); b=s.index('    elif K_SELO0 <= k < K_SELO_POP:')
s=s[:a]+'''    elif K_BR1 <= k < K_CARD1 + 6:                         # card do guia (Vitaly) -> takes limpos do frasco Lymphoria (sem cartão)
        i = k - K_BR1
        im = Image.fromarray(take(tk_card[min(2, i // 89)], i % 89 if i < 267 else 88))
'''+s[b:]
s=s.replace('''    elif K_SELO_POP <= k < K_SELO1:                        # "45 DÍAS" -> "90 DÍAS"''','''    elif K_SELO1 <= k < K_ROD:                             # saída animada do selo (mostrava "45"): congela o selo "90"
        a = ref.astype(np.float32).copy()
        a[SY0:SY1, SX0:SX1] += SELO_DELTA
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    elif K_SELO_POP <= k < K_SELO1:                        # "45 DÍAS" -> "90 DÍAS"''')
open(p,'w',encoding='utf-8').write(s)
