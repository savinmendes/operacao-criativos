---
name: reference-banco-san-benito-artifact
description: Banco San Benito na nuvem = artifact claude.ai (b-rolls aprovados SB-BRV-XX em lotes + imagens-base dos avatares); consultar antes de gerar b-roll SB
metadata:
  node_type: memory
  type: reference
  originSessionId: b1265e31-6073-4e56-bb4d-84393cd16696
  modified: 2026-10-15T13:12:32.372Z
---

O banco oficial de b-roll da pessoa é o artifact **"Banco San Benito"**: https://claude.ai/artifact/1VqxaY3k7jthFBVP4NkRZk (privado, dono = a pessoa).
- **Abas:** "B-rolls (vídeo)", com IDs `SB-BRV-NN`, e "Imagens-base", com os avatares dos criativos.
- **Lotes de b-roll:** 1 · 01–50; 2 · Pediste una señal; 3 · UGC + Rezar mucho; 4 · Belezas naturais.
- **Busca:** por cena, frase ou ID.
- **Capacidades:** `assets` e `downloads`.
- **Arquivos:** ~126 publicados. Cada item tem file, scene, lote, tag e desc (prompt em inglês). O nome bate com o arquivo usado na produção.
- **Pendentes no próprio banco:** SB-BRV-51 (farol) e SB-BRV-74 (relógio de sol).

**How to apply:** antes de gerar b-roll SB, consultar este banco. Material novo aprovado entra nele como lote novo, em vez de criar outro lugar. Leia o artifact com `Artifact read`. Para publicar, use `artifact-capabilities` (assets). Em 15/10/2026 entrou o **Lote 5 · Banco IA**: SB-BRV-101 a 225, os 125 takes de `Downloads/SB-BANCO-BROLL`, com os vídeos no asset store. A página foi reorganizada por **momento do roteiro**, com 12 usos: gancho, dor, dinheiro, ataque, oração, autoridade, forma correta, virada, alívio, urgência, live/CTA e respiro. Cada clipe tem `usos[]`, com o principal primeiro. Script de reconstrução: `Produtividade com ia/_upload_broll/build.py`; mapa de assets em `map*.txt`. Ver [[reference-sb-banco-broll]].
