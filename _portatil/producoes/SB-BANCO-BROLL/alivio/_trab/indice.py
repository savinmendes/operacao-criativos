import json, subprocess, glob, os
base = r"C:\Users\PICHAU\Downloads\SB-BANCO-BROLL\alivio"
D = {
"01":("Amanhecer entrando pela janela de cozinha simples, cortina balancando, raios de sol e poeira sobre mesa com caneca de barro","amanhecer,janela,cozinha,luz-quente,sem-pessoas,esperanca",""),
"02":("Quarto simples ao nascer do sol, janela de madeira aberta, luz sobre cama com manta listrada e cruz na parede","amanhecer,janela,quarto,cruz,sem-pessoas,luz-quente","flare verde no fim cortado"),
"03":("Mulher ~62 anos de olhos fechados sorrindo ao sol no patio, close","mulher,60+,sol,olhos-fechados,sorriso,close,alivio",""),
"04":("Homem ~52 anos de bigode na porta de casa, olhos fechados, sorri ao sol do fim de tarde","homem,50+,sol,olhos-fechados,sorriso,porta,alivio",""),
"05":("Abraco de familia (pai, mae, filha adolescente) na porta de casa colorida, luz dourada","familia,abraco,porta,reencontro,luz-quente",""),
"06":("Duas irmas idosas se abracando emocionadas na porta de madeira","idosas,abraco,porta,reencontro,emocao",""),
"07":("Avo de cabelo branco rindo no sofa com dois netos","avo,netos,riso,sala,familia,60+",""),
"08":("Avo rindo no quintal com a neta abracando seu pescoco, varal ao fundo","avo,neta,quintal,riso,varal,contraluz",""),
"09":("Fila de clientes felizes em banca de frutas de bairro, vendedor entrega sacola","fila,clientes,banca,frutas,bairro,prosperidade,comercio",""),
"10":("Padaria de bairro: dona entrega saco de pao, fila de clientes na porta (take curto)","padaria,fila,clientes,comercio,prosperidade","so 1,8 s util: saco duplica depois; 2 geracoes falharam"),
"11":("Close de maos entregando maco de cedulas genericas sobre balcao","dinheiro,maos,balcao,pagamento,prosperidade,close","cedulas sem texto legivel; maco afina apos 4,4 s"),
"12":("Comerciante idoso de oculos recebe dinheiro sorrindo na mercearia","comerciante,dinheiro,mercearia,60+,prosperidade","dinheiro some das maos apos 3,5 s"),
"13":("Mulher ~55 no telefone na cozinha, mao no peito, lagrimas de alegria (boa noticia)","mulher,telefone,boa-noticia,emocao,cozinha",""),
"14":("Homem ~63 no telefone no quintal, ri aliviado, olha para o ceu","homem,60+,telefone,boa-noticia,alivio,quintal",""),
"15":("Mesa farta de familia de tres geracoes passando pratos, luz quente","mesa-farta,familia,refeicao,abundancia,prosperidade",""),
"16":("Close de mesa farta: maos servindo ensopado da panela de barro, vapor","mesa-farta,comida,maos,close,abundancia",""),
"17":("Casal idoso de maos dadas caminhando de costas por rua de pedra ao por do sol","casal,idosos,maos-dadas,rua,por-do-sol,costas",""),
"18":("Close das maos entrelacadas de casal caminhando em trilha ao por do sol","casal,maos-dadas,close,por-do-sol,uniao",""),
"19":("Homem ~50 na laje respira fundo olhando o horizonte ao amanhecer, perfil","homem,50+,respirar,horizonte,amanhecer,alivio,laje",""),
"20":("Homem ~42 de costas na cerca do campo respira fundo olhando o sol nascer com neblina","homem,respirar,horizonte,campo,amanhecer,costas",""),
"21":("Mulher ~48 dancando sozinha feliz na cozinha com pano de prato","mulher,danca,cozinha,alegria,liberdade",""),
"22":("Idosa ~65 de avental girando e rindo sozinha na cozinha, corpo inteiro","idosa,60+,danca,cozinha,alegria",""),
"23":("Menino corre na rua de terra para o abraco do pai que o levanta, contraluz dourado","crianca,pai,abraco,corrida,reencontro,rua,contraluz",""),
"24":("Pai ajoelhado abraca forte a filha pequena na porta de casa, emocionado","pai,filha,abraco,emocao,porta",""),
"25":("Porta de madeira se abrindo e luz dourada inundando quarto escuro","porta,luz,abertura,esperanca,sem-pessoas,simbolico",""),
"26":("Idosa de xale abre porta azul para patio ensolarado, vista por cima do ombro","idosa,porta,luz,patio,esperanca,costas",""),
"27":("Bando de passaros cruzando o ceu laranja do amanhecer sobre telhados e torre de igreja","passaros,amanhecer,ceu,telhados,igreja,sem-pessoas",""),
"28":("Pombas brancas levantando voo do campo ao amanhecer, contra o sol","pombas,voo,amanhecer,campo,paz,sem-pessoas","leve borrao nas asas"),
"29":("Timelapse de hibisco vermelho abrindo com gotas de orvalho","flor,timelapse,abrindo,hibisco,renovacao,macro",""),
"30":("Margaridas em vaso de barro na janela ao sol, botoes balancando (abertura sutil)","flor,margaridas,janela,sol,renovacao","abertura sutil"),
}
IMG=190.38; VID=2121
extra={"10":VID,"11":VID}
itens=[]
for f in sorted(glob.glob(os.path.join(base,"alivio_*.mp4"))):
    nome=os.path.basename(f); nn=nome.split("_")[1]
    dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    d,t,obs=D[nn]
    itens.append({"arquivo":nome,"descricao":d,"tags":t.split(","),"in":0.0,"out":round(dur,2),"duracao_util":round(dur,2),
      "resolucao":"720x1280","fps":30,"modelo":"gpt-image-2.5-sunburst -> kling-2.5-turbo i2v 5s 9:16",
      "creditos":round(IMG+VID+extra.get(nn,0),2),"obs":obs})
tot=round(sum(i["creditos"] for i in itens),2)
json.dump({"tema":"alivio","data":"2026-10-15","flow_elevenlabs":"EBXpnzIfFiT43RSWlAm7","takes":len(itens),"creditos_total":tot,
 "obs_creditos":"2 regeracoes canceladas pelo provedor (takes 10 e 11) nao somadas; se cobradas, +4242","itens":itens},
 open(os.path.join(base,"indice.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(len(itens), tot)
