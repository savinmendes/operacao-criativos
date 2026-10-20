# Série COMPLETA em FRANCÊS: 11 vídeos (14/10/2026)

**Origem:** os 11 vídeos em `C:\Users\PICHAU\Downloads\SB-MEDALLA-COMPLETA-ES\`. A estrutura, as cenas e a montagem são as mesmas. Cada script de montagem por persona está em `C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\personas\<slug>\completa\` (APP em `_trabalho\app\completa\`, MEDALLA em `_trabalho\montar_completa2.py`).

**Mercado:** francês geral, uma única publicação para todos os países francófonos. Tratamento por "tu", como no OP2 FR. O nome é "saint Benoît", com s minúsculo em "saint".

**Saída:** `C:\Users\PICHAU\Downloads\SB-MEDALLA-COMPLETA-FR\NN_SB-FR_<SLUG>_COMPLETA.mp4` + `_narracion.txt`. Use a mesma numeração 01–11 da pasta ES.

**Trabalho:** `C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fr\<slug>\`. Cada agente usa só a própria subpasta e grava `PRONTO.txt` ao terminar. Temporários do agente ficam em `_trabalho\fr\<slug>\_tmp\`, nunca no scratchpad compartilhado.

## O que muda em relação ao ES
1. **Vozes:** todas novas, nativas francesas (biblioteca do ElevenLabs, francês da França neutro, nada de sotaque latino). **Uma voz diferente por personagem**, registrada em `_trabalho\fr\_vozes_fr.json` (`{persona: {voice_id, nome}}`) ANTES de gerar. Confira o arquivo para não repetir. O padre também tem voz francesa própria.
2. **Avatares:** a selfie de cada persona é gerada de novo no HeyGen a partir do MESMO retrato triste usado na versão ES (está na pasta `completa\` da persona), com o áudio FR. O padre FR é gerado UMA vez pelo agente "padre" e reaproveitado pelos 11.
3. **Gráficos FR** (agente "padre", em `_trabalho\fr\_comum\graficos\`, mesmo estilo e mesmas posições dos ES):
   - `titulo_gancho_fr.png`: «QUELQUE CHOSE D'INATTENDU» / «EST ARRIVÉ PENDANT» / «LA PRIÈRE À SAINT BENOÎT». As cores das 3 faixas seguem o ES, e o título não pode cobrir o personagem.
   - `selo_ficticio_mini_fr.png`: «VIDÉO FICTIVE». Mesmo tamanho mini e mesma posição, colado no topo à direita.
   - CTA: «APPUIE SUR « EN SAVOIR PLUS »» com as mesmas setas amarelas.
4. **Legenda:** no mesmo estilo, gerada pelo alinhamento da voz FR. Confira os acentos (É, È, Ç, Ê, Î, Ô).
5. **Trilha, cenas, B-roll, takes do Kling e cortes:** iguais aos do ES. Só os tempos se ajustam à fala FR.

## Falas do padre (iguais nos 11)
1. « Des millions de personnes portent cette médaille… et personne ne leur a jamais expliqué ce que disent ses lettres. Ce n'est pas un manque de foi. C'est que personne ne leur a appris la bonne façon de la prier. »
2. « Quand on la prie de la bonne façon, la maison s'apaise, la peur s'en va… et on recommence à voir des issues là où l'on ne voyait que des portes fermées. »
3. « C'est pour ça que j'ai laissé l'explication complète, lettre par lettre, dans une transmission en direct ouverte 24 heures sur 24. Appuie sur « En savoir plus », juste en dessous, et viens prier avec nous. »

**Frase final da selfie (todas as personas):** « Jusqu'au jour où un prêtre m'a expliqué quelque chose que personne ne m'avait jamais dit sur la médaille de saint Benoît. »
Nas personagens mulheres, a frase é a mesma: "expliqué" não varia aqui.

## Falas por persona (gancho em off com voz firme / reza sussurrada com volume baixo e reverb / selfie)

| # | Slug | Gancho | Reza | Selfie (antes da frase final) |
|---|---|---|---|---|
| 01 | MEDALLA (comerciante) | J'ai prié à genoux dans mon restaurant vide… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… sors-moi de cette misère. | J'ai passé presque six mois sans clients. Je rentrais à la maison et je n'arrivais plus à regarder ma femme dans les yeux. Je me sentais un raté. |
| 02 | APP (chauffeur) | J'ai prié dans ma voiture, à trois heures du matin, sans une seule course… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… sors-moi de cette misère. | J'ai passé presque six mois presque sans courses. Mes enfants me demandaient des choses et je leur répondais : demain. Je me sentais un raté. |
| 03 | COSTURERA | J'ai prié à genoux à côté de ma machine à coudre arrêtée… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… sors-moi de cette misère. | J'ai passé presque six mois sans une seule commande. Mes mains, qui avaient toujours travaillé, ne servaient plus à rien. Je me sentais inutile. |
| 04 | ABUELA | J'ai prié devant une table dressée pour douze… et j'ai mangé seule. Et voilà ce qui s'est passé. | Ô glorieux saint Benoît… rends-moi ma famille. | J'ai passé des années à mettre la table pour tout le monde. Mes petits-enfants grandissaient et je ne les voyais qu'en photo. J'avais l'impression de ne plus compter pour personne. |
| 05 | MADRE | J'ai prié par terre dans ma cuisine, avec les factures sur la table… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… protège mes enfants. | Je travaillais du matin au soir et les fins de mois ne passaient quand même pas. Mon fils m'a demandé pourquoi j'étais toujours triste. J'avais l'impression de les décevoir. |
| 06 | CAMPESINO | J'ai prié à genoux dans ma terre desséchée… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… regarde ma terre. | J'ai passé des mois à regarder ma terre se dessécher. La terre de mon père et de mon grand-père… et j'allais la perdre. Je me sentais la honte de ma famille. |
| 07 | DESEMPLEADO | J'ai prié sur un banc du parc, avec mon dossier de CV… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… sors-moi de cette misère. | Passé cinquante ans, j'ai perdu mon travail. Je sortais tous les matins en costume pour que ma famille ne le sache pas. Je me sentais un bon à rien. |
| 08 | UCI | J'ai prié à genoux près du lit de mon mari, en soins intensifs… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… ne me l'enlève pas. | J'ai passé des jours et des nuits dans cette chambre, à regarder les machines. Je rentrais à la maison et son côté du lit était vide. Je sentais que je m'éteignais de l'intérieur. |
| 09 | FERIA | J'ai prié derrière mon étal plein de fruits, sans un seul client… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… enlève ce qui a fermé mon chemin. | Mon étal était plein et personne ne s'approchait. Je voyais les voisines tout vendre, et moi je rentrais avec mes fruits perdus. J'avais l'impression qu'on m'avait jeté le mauvais œil. |
| 10 | PAREJA | J'ai prié à genoux dans ma chambre, pendant que mon mari dormait sur le canapé… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… rends la paix à ma maison. | Mon mari et moi vivions comme deux étrangers. Trente ans ensemble, et on ne se regardait plus dans les yeux. J'avais l'impression de le perdre. |
| 11 | PENSION | J'ai prié à l'accueil de ma maison d'hôtes, avec toutes les clés accrochées… et voilà ce qui s'est passé. | Ô glorieux saint Benoît… sors-moi de cette misère. | J'ai passé presque six mois sans un seul client. La maison que j'ai construite avec mon mari tombait en ruine. J'avais l'impression de lui faire défaut. |

**Por que mudou em relação ao ES:**
- "escasez" vira "misère", que é a palavra natural em francês.
- "UCI" vira "soins intensifs", que se entende em França, Bélgica, Suíça, Canadá e África.
- "pensión" vira "maison d'hôtes", termo comum na França.
- "envidia" vira "mauvais œil", que é a forma como se fala de inveja na França e na África francófona.
- O motorista de aplicativo não ganha nome de app nem "VTC", termo que só existe na França. Ele é "chauffeur", sem marca.

## Regras (lições da série; ver `contexto/22` e skills)
- Avatar: sem `fechar_boca`, sem quadro segurado e sem fusão no rosto. Pausas viram jump cut ou B-roll. Expressividade baixa.
- Voz FR: confira a pronúncia de "saint Benoît", com Whisper `fr` transcrevendo de volta. Velocidade ≤ 1,1x. Se o gancho passar de ~7 s, encurte a pausa, sem acelerar a voz.
- Revisão: `revisar_ad.py --idioma fr --idioma-residual es`, sem nenhum espanhol na fala ou na tela. Zoom no rosto da selfie. CTA único. Selo FR do 1º ao último quadro.
- Teto por persona: 25 créditos HeyGen e 450 caracteres ElevenLabs. Flora: US$ 0, já que não há imagem nova.
- Texto do anúncio FR (título até 40 caracteres + texto principal, mesmo tom suave dos ES, sem promessa) vai no `_narracion.txt`.
