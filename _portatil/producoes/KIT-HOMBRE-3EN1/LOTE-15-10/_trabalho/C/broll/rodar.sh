VG="/c/Users/PICHAU/Downloads/ADLIB-104060992792639/producao/_trabalho/_vg/Scripts/python.exe"
A=/c/Users/PICHAU/Downloads/YARA-CL/_ref/venc_122121238329420219.mp4
B=/c/Users/PICHAU/Downloads/YARA-CL/_ref/venc_122121238455420219.mp4
while read n s de ate; do
  [ "$s" = A ] && S=$A || S=$B
  "$VG" limpar_leg.py $S $n.mp4 $de $ate < /dev/null 2>&1 | tail -1
done <<LISTA
br_armaf2 A 12.0 15.5
br_asad1 A 25.0 29.8
br_asad2 A 33.0 36.6
br_9pmbox A 39.0 42.6
br_9pm1 A 44.0 47.0
br_final A 54.9 56.9
br_armaf3 B 4.0 8.0
br_9pm3 B 40.0 43.0
LISTA
echo FIM
