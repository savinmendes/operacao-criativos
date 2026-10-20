# uso: sh medir.sh nome x,y,w,h
K="/c/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/ferramentas/checar_lipsync.py"
PYTHONIOENCODING=utf-8 python "$K" out/full_$1.mp4 --audio-novo in/es_$1.mp3 --original in/orig_$1.mp4 --rosto $2 2>&1 | grep -v "W0000\|INFO\|WARNING\|inference\|absl" | grep -i "pausa\|mudou\|APROV\|REPROV\|AVISO\|corr" | tr '\n' ' '
echo
