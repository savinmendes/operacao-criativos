import json
S=json.load(open('_analise/enxuta.json',encoding='utf-8'))
head=open('_analise/doc_head.md',encoding='utf-8').read().replace('{N}',str(len(S)))
L=[head]; cur=None
for r in S:
    if r['aba']!=cur:
        cur=r['aba']; L.append(f"\n### Conjunto {cur.replace(' ','_')}\n")
    t=str(r['texto_principal']).replace('\n','  \n> ')
    L.append(f"**{r['nome_anuncio']}**  \n- Arquivo: `{cur.replace(' ','_')}/{r['arquivo']}`  \n- Título: {r['titulo']}  \n- Texto principal:\n\n> {t}\n\n- Botão: Más información · Família {r['familia']} · Posição na biblioteca {r['melhor_pos']} · {r['dias']} dias rodando\n")
open('CAMPANHA-TESTE-ENXUTA/BRIEFING_SUBIR_CAMPANHA.md','w',encoding='utf-8').write('\n'.join(L)); print('ok')
