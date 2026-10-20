cd "C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos"
E="C:/Users/PICHAU/Downloads/YARA-CL/entregas"
P="$E/_proibidos.txt"
for f in "$E"/volume/YARA-BF_H*.mp4; do
  PYTHONIOENCODING=utf-8 python ferramentas/revisar_ad.py "$f" --idioma es --proibidos "$P" --saida "$E/volume/_revisao" > /dev/null 2>&1; echo "$(basename "$f") rc=$?"
done
for f in "$E"/AD-C_yara-kit3_bf_es-cl*.mp4; do
  PYTHONIOENCODING=utf-8 python ferramentas/revisar_ad.py "$f" --idioma es --proibidos "$P" --saida "C:/Users/PICHAU/Downloads/YARA-CL/producao/musica_baixa/_revisao" > /dev/null 2>&1; echo "$(basename "$f") rc=$?"
done
