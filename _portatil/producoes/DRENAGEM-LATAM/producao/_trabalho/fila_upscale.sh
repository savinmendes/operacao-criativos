#!/bin/bash
# Fila sequencial (GPU) de upscale 2x → adNN/full_up720.mp4 ; do mais curto ao mais longo
B="/c/Users/PICHAU/Downloads/DRENAGEM-LATAM"; K="/c/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/ferramentas"
for n in 18 25 20 05 30 21 04 01 24 03; do
  o="$B/producao/_trabalho/ad$n"; mkdir -p "$o"
  [ -f "$o/full_up720.mp4" ] && continue
  echo "[$(date +%H:%M)] inicio ad$n" 
  PYTHONIOENCODING=utf-8 python "$K/upscale_video.py" "$B/originais/$n.mp4" "$o/tmp_up.mp4" --escala 2 && mv "$o/tmp_up.mp4" "$o/full_up720.mp4"
  echo "[$(date +%H:%M)] fim ad$n"
done
echo FILA_OK
