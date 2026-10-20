cd "C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos"
E="C:/Users/PICHAU/Downloads/DEWALT-ADS/entregas"
P="$E/_revisao_final/proibidos_final.txt"
N=$(ls "$E"/DW7781_*.mp4 | wc -l); k=0
for f in "$E"/DW7781_*.mp4; do
  k=$((k+1))
  python "C:/Users/PICHAU/Downloads/Produtividade com ia/painel/painel.py" etapa revisao7781 "Revisão final DCD7781 (14 vídeos)" --texto "revisar_ad [$k/$N] $(basename "$f")" --k 1 --n 6 >/dev/null 2>&1
  PYTHONIOENCODING=utf-8 python ferramentas/revisar_ad.py "$f" --idioma es --proibidos "$P" --passo 2 --saida "$E/_revisao_final" > /dev/null 2>&1; echo "$(basename "$f") rc=$?"
done
echo FIM
