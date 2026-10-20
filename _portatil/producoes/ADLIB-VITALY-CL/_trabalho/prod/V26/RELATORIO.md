# V26: Lymphoria, suavizado

- **Final:** `LYMPHORIA-ES-CL\V26 - LYMPHORIA-ADIOS-HINCHAZON.mp4` (41,3 s, 720x1280, 24,7 MB). A mesma cópia está em `SUAVIZADOS\V26 - SUAVIZADO.mp4`, ao lado de `V26 - ORIGINAL.mp4`.
- **Trocas:** a tabela completa está em `SUAVIZADOS\00-TROCAS.md`, seção V26.
- **Voz:**
  - O clone ElevenLabs da narradora (`SH5rTsQzlm6uv1YipARv`) foi criado, mas a ElevenLabs bloqueou o uso ("detected_captcha_voice": exige verificação por captcha). O clone não foi apagado.
  - Procurei uma voz parecida na biblioteca (938 candidatas): a melhor teve similaridade de 0,84, contra 0,93 da própria narradora, então descartei.
  - Usei o clone HeyGen da narradora: `a16fc0d4eb2f4f2aa822a695f59266d4`, motor orca, similaridade de 0,90.
  - As falas novas entram na faixa de voz separada pelo demucs, com a música original contínua por baixo.
  - Sem lipsync, porque a narração é em off.
- **Takes do frasco:** são takes Lymphoria já produzidos (`DRENAGEM-LATAM\producao\_trabalho\ugc\prod\`: V3, V1, P1 e P2). Não houve Kling.
- **Custo:** cerca de US$ 0,05 de ElevenLabs (4 testes de voz da biblioteca, 328 caracteres; as 4 tentativas bloqueadas não cobram). No HeyGen: 1 clone de voz + 4 sínteses de fala, pelos créditos do plano. Kling: 0.
- **Revisão:** `revisar_ad.py` deu RESULTADO OK.
  - O Whisper es não acha nenhum termo proibido.
  - O TTS pronuncia a marca como "Linforia".
  - Folha e zoom conferidos: caixas, textos grandes e takes.
- **Scripts:** `render_v26.py` (imagem), `plano_audio.json` + `..\comum\trocar_falas.py` (áudio) e `receita_final.json` (montar_ad).
- **Para olhar:**
  - O antes/depois de corpo e o "sin dieta, sin gimnasio" ficaram.
  - O fim é o simples, com fotos + oferta + selo + setas. O coordenador avisou que outro agente vai trocar os fins.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 30.97 s, parte 1 intacta, e fim novo com takes Lymphoria (ad19/t3_edit, ad14/t6_edit, ad03/t2_edit). Mesma voz do fim anterior (V26), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 39.9 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
