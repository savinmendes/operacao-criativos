---
name: feedback-licoes-producao-video
description: Regras de produção de vídeo com IA que a pessoa corrigiu em 13–14/10/2026 (avatar, Kling, gancho, trilha, selo, CTA, vozes, agentes) — consultar antes de qualquer lote
metadata:
  type: feedback
---

Antes de produzir vídeo com avatar/IA, aplicar (a pessoa corrigiu cada uma ao assistir):
- Avatar: nunca segurar/fundir quadros no rosto para fechar a boca (gera fantasma/congelado) → cortar em fronteira de palavra + B-roll/jump cut. Retrato base triste e de boca fechada (senão sorri com dentes).
- Kling: sem porta abrindo, sem entrar/sair de veículo; enquadramento final já gerado (zoom ≤1,2x); confirmar a olho antes de refazer por alarme do QA de IA.
- Gancho: personagem ~25% da altura e a dor legível no 1º quadro; título não cobre o personagem. Fala da dor = personagem frustrado olhando o próprio vazio.
- Trilha em 2 climas (tensão → esperança na virada). Selo "vídeo fictício" pequeno colado no topo; sem moldura falsa de live com nome.
- 1 CTA só, sem fala depois; loop aberto fechado antes do CTA. 1 voz diferente por avatar.
- Agentes paralelos: dividir antes de gerar, PRONTO.txt, subpasta própria. Não suavizar texto do anúncio sem perguntar.
**Why:** cada item custou uma versão refeita na série SB Medalla. **How to apply:** já está nas skills gerar-midia-ia / editar-criativo / revisar-criativo / completar-criativo e no CLAUDE.md; relatório completo em `02-relatorios/2026-10_infoproduto_revisao-producao-san-benito.md`.

Relacionado: [[project-sb-reel-medalla-es]], [[feedback-compliance-perguntar]]

14/10/2026 (Grimório V2 ES): lip sync sobre o original falhou em plano com mão perto da boca/movimento rápido → refazer como vídeo NOVO do HeyGen a partir de um quadro limpo (sem mão). Legenda trocada sobre faixa reconstruída pelo LaMa ficou borrada → pessoa preferiu legenda dentro de CAIXA opaca (alpha ≥250) cobrindo a faixa antiga. ElevenLabs tem limite de 160 vozes na conta (14/10 apagadas 30 de catálogo; log em 02-relatorios/2026-10_vozes-apagadas-elevenlabs.json).
