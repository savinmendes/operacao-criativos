# uso: sh baixar.sh ids.txt -> ls_<nome>.mp4 (espera ate todos prontos)
for i in $(seq 1 80); do
  falta=0
  while read n id; do
    [ -s ls_$n.mp4 ] && continue
    code=$(curl -s -L -o ls_$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error ls_$n.tmp >/dev/null 2>&1; then mv ls_$n.tmp ls_$n.mp4; echo "$n pronto"; else rm -f ls_$n.tmp; falta=1; fi
  done < $1
  [ $falta = 0 ] && break
  sleep 30
done
echo FIM
