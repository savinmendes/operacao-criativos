#!/bin/bash
# Refaz AD 18, AD 05 e AD 25 (longo + CURTO) com os takes re-encaixados por encaixar_edit_faixa.py (bug da cópia de branco fora da faixa).
set -e
export PYTHONIOENCODING=utf-8
T="C:/Users/PICHAU/Downloads/DRENAGEM-LATAM/producao/_trabalho"
W="C:/Users/PICHAU/Downloads/DRENAGEM-LATAM/producao"
FIX="$T/ad01/encaixar_edit_faixa.py"
cd "$T"
enc(){ ad=$1; t=$2; q=$3; out=$4; python "$FIX" $ad/flora/$t.mp4 $ad/flora/${t}_edit.mp4 $ad/flora/$out --dur $(python -c "print(f'{$q/30:.3f}')"); }
bk(){ ad=$1; shift; mkdir -p $ad/_antes_fix_faixa; for f in "$@"; do [ -f "$f" ] && cp -p "$f" $ad/_antes_fix_faixa/ || true; done; }

if [ "$1" = "ad18" ]; then
  bk ad18 ad18/flora/t1_final.mp4 ad18/flora/t2_final.mp4 ad18/flora/t3_final.mp4 "$W/AD 18 - LYMPHORIA-GOTITAS-DIA-A-DIA-ES-LATAM.mp4" "$W/AD 18 CURTO - LYMPHORIA-GOTITAS-DIA-A-DIA-ES-LATAM.mp4"
  enc ad18 t1 64 t1_final.mp4; enc ad18 t2 46 t2_final.mp4; enc ad18 t3 28 t3_final.mp4
  rm -f ad18/b*.mp4 ad18/parte1.mp4
  python processar_ad.py r18.json
  cd ad18
  ffmpeg -v error -y -i parte1.mp4 -filter_complex "[0:v]trim=0:31.10,setpts=PTS-STARTPTS[v0];[0:a]atrim=0:31.10,asetpts=PTS-STARTPTS,afade=t=out:st=31.06:d=0.04[a0];[0:v]trim=46.2:58.5,setpts=PTS-STARTPTS[v1];[0:a]atrim=46.2:58.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=12.26:d=0.04[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 15 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k curto_p1.mp4
  cd ..
  python montar_fim_universal.py "$T/ad18/curto" "$T/ad18/curto_p1.mp4" "$T/ad18/curto/narr_fim.mp3" "$W/AD 18 CURTO - LYMPHORIA-GOTITAS-DIA-A-DIA-ES-LATAM.mp4" --res 720
  echo "FIM ad18"
fi

if [ "$1" = "ad05" ]; then
  bk ad05 ad05/flora/t1_final.mp4 ad05/flora/t1_final_kling.mp4 ad05/flora/t2_final.mp4 ad05/flora/t3_final.mp4 ad05/flora/t4_final.mp4 ad05/flora/t5_final.mp4 ad05/flora/t5_final_kling.mp4 ad05/flora/t7_final.mp4 "$W/AD 05 - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4" "$W/AD 05 CURTO - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4"
  enc ad05 t1 70 t1_final_kling.mp4; enc ad05 t2 67 t2_final.mp4; enc ad05 t3 22 t3_final.mp4; enc ad05 t4 32 t4_final.mp4; enc ad05 t5 90 t5_final_kling.mp4; enc ad05 t7 34 t7_final.mp4
  cd ad05/flora
  python comp_movel.py t1.mp4 t1_final_kling.mp4 t1_final.mp4 "0.3:280,0,605,570" "0.4:280,0,605,570" "0.6:300,0,600,560" "0.8:250,0,580,530" "0.84:245,10,575,550" "0.86:0,0,0,0" "1.14:0,0,0,0" "1.16:210,320,530,925" "1.2:210,310,530,920" "1.4:200,370,525,980" "1.8:210,400,525,990" "2.2:210,370,530,980"
  python ../../blur_movel.py t1_final.mp4 t1_final_b.mp4 b1.json && mv t1_final_b.mp4 t1_final.mp4
  python comp_regiao.py t5.mp4 t5_final_kling.mp4 t5_final.mp4 235,735,540,1280
  cd "$T"
  rm -f ad05/b*.mp4 ad05/parte1.mp4 ad05/k0.mp4
  python orq.py r05.json --so-parte1
  cd ad05; python ../textos_lote.py parte1.mp4 parte1_fix.mp4 fix_puesta.json && mv parte1_fix.mp4 parte1.mp4; cd ..
  python montar_fim_universal.py $T/ad05 $T/ad05/parte1.mp4 $T/ad05/narr_fim.mp3 "$W/AD 05 - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4" --res 720
  rm -f ad05c/curto/s*.mp4 ad05c/curto/parte1_curto.mp4
  python curto2.py $T/ad05c $T/ad05/corpo_tratado.mp4 "$W/AD 05 CURTO - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4" 47.95-54.75 88.05-123.40 146.35-155.30 --hook $T/ad05/hook_final.mp4 --so-parte1
  cd ad05c/curto; python $T/textos_lote.py parte1_curto.mp4 p1fix.mp4 fix.json && mv p1fix.mp4 parte1_curto.mp4; cd "$T"
  python montar_fim_universal.py $T/ad05c/curto $T/ad05c/curto/parte1_curto.mp4 $T/ad05c/narr_fim.mp3 "$W/AD 05 CURTO - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4" --res 720
  echo "FIM ad05"
fi

if [ "$1" = "ad25" ]; then
  bk ad25 ad25/flora/t1_final.mp4 ad25/flora/t4_final.mp4 "$W/AD 25 - LYMPHORIA-VECINO-ES-LATAM.mp4" "$W/AD 25 CURTO - LYMPHORIA-VECINO-ES-LATAM.mp4"
  enc ad25 t1 54 t1_final.mp4; enc ad25 t4 175 t4_final.mp4
  rm -f ad25/b*.mp4 ad25/parte1.mp4
  python processar_ad.py r25.json
  rm -f ad25/curto/s*.mp4
  python curto.py ad25 ad25/curto/narr_fim.mp3 "$W/AD 25 CURTO - LYMPHORIA-VECINO-ES-LATAM.mp4" 0-6.45 36.8-46.58 48.4-59.05 83.2-89.0 112.18-116.2 198.1-206.35 231.5-235.25
  echo "FIM ad25"
fi
