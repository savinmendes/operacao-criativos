#!/bin/bash
# uso: lote.sh <corpo> <var_inicial>   -> 10 variações G1..G10
cd "$(dirname "$0")"
c=$1; n=$2
for k in ${KS:-1 2 3 4 5 6 7 8 9 10}; do
  v=$(printf "%02d" $((n+k-1)))
  echo "[$(date +%H:%M)] [$k/10] VAR $v G$k x AD$c"
  PYTHONIOENCODING=utf-8 python gerar_var.py $v G$k $c 2>&1 | grep -E "^ok|Error|error|Traceback|SystemExit" 
done
echo LOTE_OK $c
