---
name: project-sb-reel-medalla-es
description: SB Medalla ES — teste de produção a partir do reel Sagrado Verso, personagens IA novos, selo VIDEO FICTICIO, entregue 13/10/2026 (2:01, ~US$2,30 + ~70 cr HeyGen)
metadata:
  type: project
---

13/10/2026: a pessoa quis testar as ferramentas refazendo a estrutura do reel "Sagrado Verso" (DeKy6u6xSr0, vende livro Grimório) para a oferta San Benito ES. Roteiro final escrito pela pessoa (oração da medalha CSSML/NDSMD/VRS…, "Camino de Fe con San Benito", CTA "Ver más"). Pasta `Downloads/SB-REEL-MEDALLA-ES/`, final `SB-ES_MEDALLA_FICTICIO.mp4`.
Regras que fixei: não copiar falas nem rostos do reel de terceiro (personagens IA novos só por texto), sem nome real de padre, selo "VIDEO FICTICIO" topo direito no vídeo inteiro.
Vozes biblioteca ElevenLabs: comerciante Santiago (VXZKNah1ssrzM8c81OiY), sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu); latim com grafia fonética no TTS (míki, cue, Númcuam).
Lição: HeyGen avatar-from-image sorri com dentes nas pausas → `_trabalho/fechar_boca.py` (cola boca fechada/segura quadro) aprovou checar_lipsync. Gemini QA deu falso alarme no Kling salão cheio — conferir no olho.
Pendente decisão da pessoa: "Ahora mismo está ocurriendo una transmisión en vivo" (regra do kit: nada de "ao vivo agora").

Relacionado: [[project-san-benito-es-vencedores]], [[feedback-compliance-perguntar]]

v2 (13/10/2026, 1:11,7): sem moldura EN VIVO (só selo VIDEO FICTICIO), padre fala o texto do OP2 + CTA live. Bugs da v1 = retoque fechar_boca.py (quadros fantasma por fusão, rosto congelado 0,3–0,5 s, salto com zoom). Lição corrigida: NÃO segurar/fundir quadros no rosto; cortar avatar nas fronteiras das palavras e cobrir pausas com b-roll/jump cut. checar_lipsync não mede quando não sobram pausas no rosto — validar a olho a 30 fps.

13–14/10/2026: série completa de personas (mesmo padre da v2): comerciante, taxista (cancelado pela pessoa depois), motorista de app + 9 novas (costurera, abuela, madre, campesino, desempleado, UCI opção B — virada com paciente acordando, feria, pareja, pensión). Briefing `personas/BRIEFING.md`; vozes 1 por avatar registradas em `_trabalho/personas/_vozes.json` (pessoa quer voz diferente para cada avatar). Custo lote 9: ~US$8,50 Flora/Kling + ~90–150 cr HeyGen. Regras Kling: sem porta/entrar em veículo; HeyGen sorri com dentes em fala triste (sem solução boa).

14/10/2026 — Série COMPLETA (formato aprovado após /completar-criativo): gancho amplo novo + "frustrado" novo (Flora/Kling) + selfie de retrato triste boca fechada + padre único (mecanismo das letras da medalha + CTA único "Más información", live 24 h confirmada pela pessoa) + trilha 2 climas (tensão→esperança) + selo mini no topo. 11 vídeos em `Downloads/SB-MEDALLA-COMPLETA-ES/`. Briefing `personas/BRIEFING_COMPLETA.md`. Custo série ~US$10 Flora/Kling. App ganhou voz própria (Alejandro Durán sKgg4MPUDBy69X7iv3fA).

14/10/2026 — Série COMPLETA em FRANCÊS (11 vídeos) em `Downloads/SB-MEDALLA-COMPLETA-FR/` (briefing `personas/BRIEFING_FR.md`, trabalho `_trabalho/fr/`). Mesmo visual (retratos/takes ES), vozes FR nativas distintas (registro `_trabalho/fr/_vozes_fr.json`; padre "Alexandre" gP52hjM48hyNoVCbizxO), padre FR único reaproveitado. Adaptação cultural: misère, soins intensifs, maison d'hôtes, mauvais œil, chauffeur sem VTC/app, saint Benoît, «Appuie sur « En savoir plus »». Visual latino mantido; sugerido testar e, nos vencedores, fazer versão com personas/cenários da África francófona. Títulos FR únicos por persona.
