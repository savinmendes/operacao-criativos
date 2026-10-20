# baixa as saidas prontas e finaliza cada uma. uso: sh baixar.sh  (ate ~100 min)
cd "/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/_trabalho/lipsync/LOTE_2"
for i in $(seq 1 200); do
  falta=0
  while read n id; do
    [ -s out/ls_$n.mp4 ] && continue
    code=$(curl -s -L -o out/ls_$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error out/ls_$n.tmp >/dev/null 2>&1; then mv out/ls_$n.tmp out/ls_$n.mp4; echo "$n pronto $(date +%H:%M)"; PYTHONIOENCODING=utf-8 python scripts/finalizar.py $n 2>&1 | grep -v -i "warn\|W0000\|INFO\|feedback" ; else rm -f out/ls_$n.tmp; falta=1; fi
  done < ids.txt
  k=$(ls out/ls_*.mp4 2>/dev/null | wc -l)
  python "/c/Users/PICHAU/Downloads/Produtividade com ia/painel/painel.py" etapa vsl-de-lip2 "Lipsync lote 2" --texto "[$k/70] saidas HeyGen baixadas e finalizadas" --k 3 --n 5 >/dev/null 2>&1
  [ $falta = 0 ] && break
  sleep 30
done
echo FIM
