# roda finalizar.py a cada 60 s ate os 69 trechos estarem prontos (max ~100 min)
cd "/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/_trabalho/lipsync/LOTE_4"
for k in $(seq 1 100); do
  PYTHONIOENCODING=utf-8 python scripts/finalizar.py jobs.json 2>&1 | grep -v -E "^W0000|WARNING|INFO" >> _t/loop.log
  n=$(python -c "import json;print(len(json.load(open('relatorio.json',encoding='utf-8'))))")
  python "/c/Users/PICHAU/Downloads/Produtividade com ia/painel/painel.py" etapa vsl-de-lip4 "Lipsync lote 4" --texto "[$n/69] trechos baixados e medidos" --k $n --n 69 >/dev/null 2>&1
  echo "rodada $k: $n/69 $(date +%H:%M)" >> _t/loop.log
  [ "$n" -ge 69 ] && break
  sleep 60
done
echo FIM >> _t/loop.log
