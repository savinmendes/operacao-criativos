# uso: sh baixar.sh ids.txt  -> out/ls_<nome>.mp4 (espera ate todos prontos, max ~40 min)
for i in $(seq 1 110); do
  falta=0
  while read n id; do
    [ -s out/ls_$n.mp4 ] && continue
    code=$(curl -s -L -o out/ls_$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error out/ls_$n.tmp >/dev/null 2>&1; then mv out/ls_$n.tmp out/ls_$n.mp4; echo "$n pronto"; else rm -f out/ls_$n.tmp; falta=1; fi
  done < $1
  [ $falta = 0 ] && break
  sleep 30
done
echo FIM
