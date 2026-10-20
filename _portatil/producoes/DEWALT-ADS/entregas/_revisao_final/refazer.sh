set -e
cd "C:/Users/PICHAU/Downloads/DEWALT-ADS/edicao"
PYTHONIOENCODING=utf-8 python rodar_lote.py > _lote_revisao7781b.log 2>&1
echo LOTE_OK
cd "C:/Users/PICHAU/Downloads/DEWALT-ADS/edicao/_legenda_sinc"
rm -f _resumo_sinc.json
PYTHONIOENCODING=utf-8 python medir_lote.py > medir_lote3.log 2>&1
echo SINC_OK
set +e
bash "C:/Users/PICHAU/Downloads/DEWALT-ADS/entregas/_revisao_final/rodar_revisao.sh" > "C:/Users/PICHAU/Downloads/DEWALT-ADS/entregas/_revisao_final/rodar_revisao3.log" 2>&1
echo REV_OK
