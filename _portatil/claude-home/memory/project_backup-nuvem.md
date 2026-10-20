---
name: project-backup-nuvem
description: Arquivo de projetos antigos no Google Drive (5 TB) via rclone — legado CartiCuri + brutos subindo desde 14/10/2026; apagar do PC só após check + ok da pessoa
metadata:
  type: project
---

14/10/2026: disco C (SSD único 1 TB NVMe) chegou a 98% cheio; limpei 15 GB de intermediários (mont*/avatar v1) do SB-REEL-MEDALLA-ES. Pessoa tem Google Drive de 5 TB (usado ~11 GB). Google Drive para computador instalado (unidade G:), mas upload em massa vai por rclone (`gdrive:` reconectado, conta 5 TB) porque o Drive desktop faz cache local e o disco não comporta.
Script: `ferramentas/backup-nuvem/subir_arquivo.ps1` (copy + check --one-way), logs em `ferramentas/backup-nuvem/logs/` (status.txt). Destino `gdrive:ARQUIVO-PROJETOS/legado-carticuri-x1` (138,7 GB) e `/trabalho-brutos` (89,6 GB). ~7,7 MiB/s → ~8–9 h no total.
Próximo: após CHECK_FIM exit 0, pedir confirmação e apagar do PC. Depois: lotes fechados (Lymphoria 46,6 GB, Oración/ADLIB 40,6 GB — no PC manter _vg, _lote, scripts usados pelo kit —, Drenagem 14,5 GB…). Nunca subir pessoal/financeiro/recibos. rclone usa client_id compartilhado que será aposentado em 2026 — se falhar, criar client_id próprio.

**16/10/2026:** as 2 subidas terminaram e foram verificadas: legado 2.994 arquivos / 138,4 GiB; brutos 2.615 / 89,6 GiB, 0 diferenças. A pasta 'VOVÓ 80/VOVO EDIT BROLLS ' (nome com espaço no fim) falhava no rclone; os 2 arquivos dela subiram via cópia temporária sem o espaço, e a verificação deu ok. Falta o ok da pessoa para apagar os locais.
**16/10/2026 (cont.):** a pessoa deu o ok e as duas pastas locais foram apagadas (3.357 arquivos, ~132 GB; a lista ficou em logs/apagados_do_pc_*.txt). O disco C ficou com 244 GB livres. Pasta no Drive: https://drive.google.com/drive/folders/10TF1XjmrDIDMrOqJE1G-PvF02gE6n456
