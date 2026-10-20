# 30 variações gancho × corpo — Lymphoria (04/10/2026)

Saída: `producao/VARIACOES/VAR 01..30` (720x1280, H.264/AAC, 283–313 s, 35–39 MB).
Scripts: `prep_fonte.py` (banco scdet + transcrição), `gerar_var.py` (variação), `revisar_var.py` (revisão), `lote.sh`, `corpos.json`, `ganchos.json`.

Corpos (final .mp4 da pasta producao, do corte até o fim COD; cauda silenciosa cortada para 0,6 s):
- VAR 01–10: AD 20 (masculino), corte 10,93 s, antes de "Otra vez vas a llegar tarde"; voz xYPon3lV4FsEOMk5vd1Y.
- VAR 11–20: AD 05 (feminino), corte 20,35 s, antes de "Así que culpé a mi cuerpo"; voz BCCHRwYb332ahRN0gT7H.
- VAR 21–30: AD 30 (feminino), corte 24,63 s, antes de "Llegué a casa, me miré en el espejo"; voz x7Q3zqDG9jz6G8aiQCio. Passa dos 8–15 s pedidos: cortar antes deixaria o corpo começando por "Durante diez minutos…" ou "Me miró sin verme…", frases que só fazem sentido depois do gancho original da fila.

Gancho: fala TTS com a voz clonada do narrador do corpo. As tomadas saem primeiro do trecho anterior ao corte do próprio AD, que não aparece no corpo, com margem de +0,15/-0,2 s e sem repetir grupo de cena. Na tela, uma caixa branca (Poppins Bold 46) mostra cada frase e cobre a legenda queimada original. O fundo é a música do próprio corpo (demucs no_vocals) e termina exatamente no corte.
Adaptações de gênero (corpo AD20): G1 "esposa/mejor amigo", G2 "el hombre que hacía reír a mi esposa / diez años menos", G3 "exesposa/novio", G4 "peso de la edad". Nos corpos femininos, G10 virou "Esa pancita no es grasa" (com cenas femininas).
TTS: 30 falas, 3.592 caracteres, cerca de US$ 0,59.
Revisão: as 30 passaram por decodificação, formato, whisper do gancho e da emenda, scdet e silêncio. O VAR 24 deu um alerta falso ("Llegué" na emenda): conferi a energia do áudio e rodei o whisper de novo, e a palavra está inteira. Os VAR 19, 27 e 29 vieram com a emenda vazia no whisper; rodei de novo a partir do corte e a fala está inteira. Também rodei o whisper no vídeo inteiro dos VAR 10, 20 e 30 (um por corpo): nenhuma palavra proibida.

## Correção 05/10: VAR 11–20 refeitas (corpo AD 05 corrigido)
- `prep_fonte.py 05` + `lote.sh 05 11`. As falas TTS vieram do cache, sem custo.
- Mudanças:
  - Os takes do frasco ficaram sem as letras do rótulo antigo, tanto no corpo quanto nos ganchos que usam tomadas do AD 05.
  - As últimas tomadas de alguns ganchos mudaram, porque o banco do scdet foi regenerado.
  - Os totais ficaram 0,2–0,3 s menores na cauda.
- `revisar_var.py 11..20`: todas OK (log_rev05_fix.txt).
- Versões antigas em `_antes_fix_faixa/`.
- VAR 21–30 não foram refeitas: o AD 30 não foi afetado, porque usou `--sem-legenda` + `colar_caixa_verde.py`.
