# processa cada out.mp4 que chegar (ate todos os ids de ids_resto.txt terem <id>.mp4)
cd "$(dirname "$0")"
while true; do
  falta=0
  while read n id; do
    [ -s ../$n.mp4 ] && continue
    if [ -s ../work/$n/out.mp4 ]; then PYTHONIOENCODING=utf-8 python colar.py $n 2>&1 | grep -E "^L0|ERRO|Trace"; [ -s ../$n.mp4 ] || echo "$n FALHOU_COLAR" ; else falta=1; fi
  done < ../_tmp/ids_resto.txt
  [ $falta = 0 ] && break
  grep -q FIM ../_tmp/baixar_resto.log && break
  sleep 20
done
echo LOOPFIM
