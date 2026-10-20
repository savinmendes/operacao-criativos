from pathlib import Path
p = Path('RELATORIO.md'); t = p.read_text(encoding='utf-8')
a = t.index('- **Único "PROBLEMA" do kit: i1r'); b = t.index('- Folha `revisao', a)
novo = '''- **i1r refeito (autorizado pelo coordenador, até 10 créditos):**
  - HeyGen `speed`, 69,57–75,97 s (192 q, 6,4 s ≈ 6–7 créditos), com o recorte rastreado do `rastreado.py`: 320x568, fixo, cerca de 3x o rosto.
  - Nesse plano aberto o rosto é pequeno (~110 px) e o detector não o achava no quadro inteiro. O `rastreado.py` ganhou `roi` (detecção num recorte ampliado 2x) e `semente`.
  - A saída voltou com 192 quadros exatos e foi colada só na boca e no queixo. As emendas em 2087 e 2279 caem em cortes de câmera.
  - **Resultado: correlação ES 0,13, índice de pausa — (sem pausa ≥ 8 q; a fala ES é contínua).** A boca mudou em 93 % dos quadros e a correlação com o PT é 0,14.
  - Medi também a saída crua do HeyGen, antes de colar: 0,13 (100 % mudou). **A meta de ≥ 0,15 não foi atingida**, e o kit continua dando PROBLEMA nesse trecho.
  - Na folha de 3 em 3 quadros (saída × entrada, com barras de áudio ES/PT), a boca é nova em todo o trecho e articula, mas sem fechar nitidamente. Não há pausa no ES para mostrar fechamento.
  - A correlação baixa vem da fala ES sem pausa (envelope quase plano), igual ao b1 e ao g1.
  - Ficou a versão nova (recorte maior, boca nova em 93 %). A anterior está em `_antes_loteB\`.
  - Não houve 2ª tentativa: o saldo autorizado (~3,6 créditos) não cobre 6,4 s.
- **Créditos do lote B no AD 16:** 12,0 s (j1, k1) + 6,4 s (i1r) = 18,4 s ≈ 18–19 créditos.
- **Revisão depois do i1r:** `revisao\revisar_loteB_i1.log`, com a mesma lista UTF-8.
  - Nenhum termo proibido, es 0,98, nenhum silêncio, 8 cortes, setas no último quadro;
  - **índice de pausa do conjunto: 0,18**;
  - o único PROBLEMA continua sendo o i1r (0,13).
'''
t = t[:a] + novo + t[b:]
p.write_text(t, encoding='utf-8'); print('ok')
