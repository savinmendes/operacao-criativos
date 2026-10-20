# V10: Lymphoria, suavizado

- **Final:** `LYMPHORIA-ES-CL\V10 - LYMPHORIA-CARRITO-MENOPAUSIA.mp4` (77,0 s, a mesma duração do original, 720x1280, 19,5 MB). A mesma cópia está em `SUAVIZADOS\V10 - SUAVIZADO.mp4`, ao lado de `V10 - ORIGINAL.mp4`.
- **Trocas:** a tabela completa está em `SUAVIZADOS\00-TROCAS.md`, seção V10.
- **Voz:**
  - Clone ElevenLabs da mulher: `eLDgbtnf2Ub9I9whr89p`, amostra da faixa de voz do demucs, 0–77 s.
  - As frases foram geradas com contexto e recortadas pelo alinhamento.
  - Cada bloco foi encaixado no tempo original: atempo entre 0,95 e 1,03, com pausas distribuídas no bloco da oferta.
  - O ganho foi igualado à voz original. A música de fundo segue contínua.
- **Rótulo 0–7,6 s:** remendo "LYMPHORIA" na faixa marrom, rastreado por fluxo óptico (`rastrear_rotulo.py` + `patch_rotulo.py`, com âncoras nos quadros 0 e 136). Grátis, sem Kling.
- **Custo:** cerca de US$ 0,09 de ElevenLabs (528 caracteres). Kling e HeyGen: 0.
- **Revisão:** `revisar_ad.py` deu RESULTADO OK.
  - Na 1ª rodada houve um quadro solto em 63,83 s: era a saída animada do card antigo. Recriei essa saída encolhendo o cartão novo.
  - Também corrigi o "45" que aparecia desfocado na entrada do selo e um resto do "45" sob o "90".
- **Ajuste pedido pelo coordenador:** o cartão da oferta (55–64 s) ficou **sem preços**.
- **Para olhar:**
  - Menopausia e antes/depois.
  - "hoy es el día, hoy es tu día" (74,7–76,6 s), com o rosto e sem lipsync.
  - A troca de "no interfiere con la mayoría de los medicamentos" virou "es cien por ciento natural, sin estimulantes, y además sabe a miel". Ocupa o trecho 39,6–44,4 s inteiro, para não repetir "100% natural, sin estimulantes" duas vezes seguidas.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 70.97 s, parte 1 intacta, e fim novo com takes Lymphoria (ad14/t4_edit). Mesma voz do fim anterior (fala original da criadora), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 77.0 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
