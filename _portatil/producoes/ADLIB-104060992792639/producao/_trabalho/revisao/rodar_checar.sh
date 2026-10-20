K="/c/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/ferramentas/checar_lipsync.py"
T="/c/Users/PICHAU/Downloads/ADLIB-104060992792639/producao/_trabalho"
export PYTHONIOENCODING=utf-8
for n in s01 s02 s03 s04 s05 s06 s07 s08 s09 s10 s11 s12 s13; do
  d="$T/ad01/lipsync"; echo "### AD01 $n"; python "$K" "$d/ls_$n.mp4" --audio-novo "$d/es_$n.mp3" --original "$d/pt_$n.mp4" 2>&1 | grep -v -i -E "warning|W0000|I0000|inference_feedback|absl"
done
for n in j1 w01 w02 w03 w04 w05 w06 w07 w08 w09 w10 w11 w12 w13; do
  d="$T/ad13/lipsync"; echo "### AD13 $n"; python "$K" "$d/ls_$n.mp4" --audio-novo "$d/es_$n.mp3" --original "$d/pt_$n.mp4" 2>&1 | grep -v -i -E "warning|W0000|I0000|inference_feedback|absl"
done
echo FIM
