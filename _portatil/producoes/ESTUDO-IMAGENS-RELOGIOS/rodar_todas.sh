cd "/c/Users/PICHAU/Downloads/ESTUDO-IMAGENS-RELOGIOS"
export PYTHONIOENCODING=utf-8
mkdir -p dados
coleta(){ python coletar.py "$1" "$2" "dados/$2.json" >> log.txt 2>&1; }
coleta Pelvini pelvini & coleta Mockberg mockberg & coleta Venezianico venezianico & coleta AlphaGear alphagear & wait
coleta Monomods monomods & coleta "Pascal Design" pascaldesign & coleta Laphont laphont & coleta "Marble Veil" marbleveil & wait
coleta "Chrono Customs" chronocustoms & coleta "Lucky Fours" luckyfours & coleta "Aston Paris" astonparis & wait
echo FIM >> log.txt
