# Briefing comum: lote "Humillación" (10 personas), aprovado pela pessoa em 14/10/2026. Ela está DORMINDO: não pergunte nada. Decida e registre.
Roteiro OFICIAL: `C:\Users\PICHAU\Downloads\TESTE1-SB-ES\v5-personas\ROTEIRO_PERSONAS_v2.md`. A sua persona usa exatamente o texto de lá; [PEDIDO] e [CTA] são as linhas fixas do topo, com o NOMBRE trocado.
Referência visual e técnica APROVADA: `TESTE1-SB-ES\v4\SB-ES_NOTICIA-AURELIO_B-ORACION-COMPLETA_FICTICIO.mp4` (abertura com a reportera em PiP, moldura de post "Fe en Noticias / Trabajador es humillado y algo impactante sucede", legenda ES palavra a palavra, selo VIDEO FICTICIO colado no topo à direita, setas TOCA «VER MÁS»).
Scripts dessa versão: `TESTE1-SB-ES\v3\_trabalho\final_B\` (montar_v4B.py, abertura, titulo.py), `v3\_trabalho\v4_reporter_pip\` (PiP da reportera: compor_reporter.py, img\reportera_verde.png, chroma), `v3\_trabalho\abertura_v2\` (briga Seedance 3:4 + compor_abertura.py), `v3\_trabalho\BRIEFING_COMUM.md` (método e lições), `C:\Users\PICHAU\Downloads\Produtividade com ia\CLAUDE.md` (armadilhas: cor bt601, -reinit_filter 0, salto de pts, lipsync etc.).
LEIA tudo isso antes de começar.

## Estrutura do vídeo (~55–65 s, 720×1280 30 fps), termina no CTA
1. 0–~3,5 s: a REPORTERA em PiP (chroma, caixa como no v4) fala a linha "Imágenes impactantes: … por su fe." por cima da AÇÃO violenta (o agressor arranca o crucifixo/terço, joga no chão e quebra as coisas). Zoom de 130% no impacto + título no topo da janela do post (texto adaptado à persona, estilo do titulo.py, ex.: "LO HUMILLARON POR SU FE… AL DÍA SIGUIENTE PASÓ ESTO"; feminino quando for mulher).
2. Agressor e persona falam (Seedance 2.0 i2v, take ÚNICO contínuo com ÁUDIO NATIVO ES LATAM, aspect 3:4 forçado, câmera de rua/celular fixa, ~10 s, os 2 primeiros ~3 s SEM fala, como no prompt de `abertura_v2`). Os mesmos 2 personagens do início ao fim, sem cortes. Transcreva (faster-whisper medium cpu int8 es) e confira as falas exatas; regere 1 vez se errar.
3. Sem fala: a persona junta o crucifixo/terço do chão (close nas mãos) com trilha TRISTE → lugar vazio → poucas pessoas → lugar cheio, com a trilha virando esperança (veja `final\trilha.py` da v3 / ElevenLabs Sound Effects). Kling 2.5 Turbo i2v econômico, a partir de imagens do mesmo cenário e da mesma persona.
4. REPORTERA em tela (HeyGen Avatar IV 720p a partir de `v2\_trabalho\imagens\reportera_gpt.png`, voz Gabriela hHjbwzYZW17oh0p05AKv, parâmetros do L04): a linha "Al día siguiente…" da persona.
5. PERSONA em tela, entrevistada com o microfone da reportera, no local de trabalho (HeyGen Avatar IV 720p a partir da imagem da persona): depoimento + [PEDIDO], em jobs ≤ ~12 s, pausas internas ≤ 0,25 s. As frases sem rosto podem ir em voz off sobre b-roll da própria persona (plano inédito).
6. REPORTERA em tela: [CTA]. Setas TOCA «VER MÁS» do início dessa fala até o último quadro. NADA é falado depois.
Selo VIDEO FICTICIO o vídeo todo. Moldura de post o vídeo todo (como a parte de notícia do v4). Legenda pelo roteiro.

## Regras
- A persona tem UM rosto só (briga, virada, entrevista): gere primeiro a imagem-mestra da persona (GPT Image 2 1k) e use-a como referência em TODAS as outras imagens (briga, vazio, cheio, entrevista). Mesma roupa.
- A voz da persona no depoimento é a do ElevenLabs atribuída abaixo. Na briga, a voz vem do Seedance. Se der, aproxime com speech-to-speech (eleven_multilingual_sts_v2, ver `contexto/estrategias-criativos.md` "Voz única") só na fala da persona, isolando com demucs; se degradar, mantenha o nativo e registre.
- Nenhum plano de b-roll repetido dentro do vídeo. Sem texto em português ou inglês na imagem. Cuidado com "Holy Bible" e "PAID".
- HeyGen sempre em 720p. Intervalos ruins (dentes nas pausas, 1º quadro) cobertos com corte ou b-roll, nunca congelar o rosto.
- Teto por persona: Flora US$ 3,50 (cote antes; registre o real). ElevenLabs centavos.
- Painel: `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa sbv5-<persona>-<etapa> ...` (img, custo, fim).
- CPU: há 10 agentes em paralelo. Use whisper medium só para o QA final, small para os checks intermediários, e não rode LaMa sem necessidade.
- Pasta de trabalho: `TESTE1-SB-ES\v5-personas\_trabalho\<persona>\` (só escreva nela). Saída: `TESTE1-SB-ES\v5-personas\SB-ES_HUMILLACION_<ID>-<NOMBRE>_FICTICIO.mp4` + `_narracion.txt` + `_frames.jpg` + `_texto-anuncio.txt` (título "🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏"; texto principal da v4 B, fechando com "Mira la oración en vivo 👇").
- QA: revisar_ad.py do kit (rodar da pasta do kit; termos proibidos: grimorio, collar, ao vivo, pix, R$, "Fé em"), salto de pts, whisper medium es contra o roteiro, folha de contato 0–15 s a 30 fps (mesmo rosto? ação clara?), anti-repetição. Depois 1 subagente revisor independente rápido, e corrija o que ele achar.
- NÃO abra o vídeo com Start-Process (a pessoa está dormindo). Relatório final curto: arquivo, duração, custos reais (US$ e créditos), vozes, imperfeições com tempos.

## Vozes ElevenLabs da persona (fixas, não troque)
P0 Aurelio: Santiago VXZKNah1ssrzM8c81OiY · P1 Ramón: Salvatore wfTWLJ20rcMqvU8gIiAB · P2 Rosa: Luisa efcRUax7uSa9kpBwtDPe · P3 Carmen: Alisson SmgKjOvC1aIujLWcMzqq · P4 Julio: Alberto Rodriguez l1zE9xgNpUTaQCZzpNJa · P5 Marta: María Blanco HRi5Prm2B3PevwpDmVLP · P6 Ernesto: escolha na biblioteca um homem 50+ com sotaque MEXICANO que não esteja nesta lista · P7 Antonio: Pa Gabriel Zkg9LlmGNlBWLgWjzTnu · P8 Tomás: escolha na biblioteca um homem 60+ com sotaque COLOMBIANO/ANDINO, diferente de todos desta lista · P9 Lucía: Azu D3ws14YxTqcjPaXEOehR.
Reportera: Gabriela hHjbwzYZW17oh0p05AKv (todas).
