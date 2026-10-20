# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Operação de Tráfego Pago e Criativos (Grupo Chegou)

Este arquivo orienta o Claude Code durante todo o trabalho neste projeto. Leia-o por completo antes de executar qualquer tarefa relevante.

## Quem é a pessoa e o que ela faz aqui

A pessoa é gestora de tráfego pago e produtora de criativos, operando três frentes de negócio dentro do **Grupo Chegou**:

1. **Dropshipping COD** (pagamento na entrega, sem estoque na maioria dos produtos) — mercados: Chile, Colômbia, México, Guatemala, Romênia. Catálogo com dezenas de produtos por país (suplementos, eletrônicos, beleza, casa), cada um com fornecedor e custo próprios, controlados por país.
2. **Infoprodutos** (VSL + quiz + funil de upsell, via Hotmart/Digistore/Stripe) — ofertas: **Onda Tesla 2.0** (saúde auditiva), **Protocolo Glúteos Brasileños** (estética), **Oração de San Benito** (espiritualidade) — mercados Latam, Espanha e Worldwide.
3. **X1 After-Pay** — venda 1-a-1 de nutracêutico (**CartiCuri/CarteCure**, fitoterápico articular) via WhatsApp no Brasil, com entrega antes do pagamento, público 50+/aposentados.

Este espaço de trabalho serve para organizar a operação de tráfego pago, a produção de criativos, os relatórios de performance e a gestão de funis dessas três frentes: organizar arquivos, analisar tarefas, criar materiais, gerar relatórios, montar dashboards, produzir apresentações, criar PDFs, gerar infográficos, acompanhar tarefas em ferramentas externas e manter a rotina organizada.

**Cada frente tem lógica própria — nunca misture regras, métricas ou linguagem entre elas:**
- COD: foco em CPA, taxa de efetividade de entrega/pagamento e margem por produto/país/fornecedor.
- Infoprodutos: foco em VSL, quiz, funil de upsell, ticket, CAC e LTV por oferta/mercado.
- X1 After-Pay: foco em atendimento via WhatsApp, fechamento por closer, inadimplência/efetividade de pagamento pós-entrega, público 50+.

## Principais atividades

- Criar e gerenciar campanhas no Meta Ads, Kwai Ads e TikTok Ads.
- Produzir criativos do roteiro à edição final (vídeo e imagem).
- Analisar métricas de performance, CPA e margem por país/oferta.
- Organizar funis de venda (advertorial/quiz/VSL → checkout ou WhatsApp COD/after-pay).
- Acompanhar atendimento e fechamento de vendas (closers, no caso do X1 After-Pay).
- Documentar SOPs de produção e controlar catálogo de fornecedores/custos por país.

## Principais entregáveis

Criativos de vídeo e imagem, roteiros e hooks, VSLs, páginas de vendas/advertoriais/quiz, relatórios de performance de campanha (por oferta e por país), dashboards de métricas (CPA, efetividade de pagamento, margem de contribuição), apresentações internas, planilhas de controle de preço/fornecedor.

## Ferramentas usadas

Meta Ads, Kwai Ads, TikTok Ads, Notion (fonte de verdade de ofertas e preços), Google Drive, WhatsApp (atendimento e vendas), planilhas, VS Code.

## Edição de criativos (kit)

Para qualquer pedido de edição/produção de criativo (legenda, setas de CTA, tela dividida, narração, imagens/vídeos IA, finalizar AD), **leia antes `kit-edicao-criativos/CLAUDE.md`** e siga as skills `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`. Para lotes inteiros, `traduzir-criativo` (vídeo de outro idioma/mercado) e `adaptar-marca` (trocar marca/oferta de criativo próprio) definem o fluxo de estudo → briefing → produção → entrega. Os scripts ficam em `kit-edicao-criativos/ferramentas/` — rode-os com o diretório de trabalho em `kit-edicao-criativos/` (a chave do ElevenLabs está no `.env` de lá).

## Código e ferramentas (como rodar)

Não é um repositório git nem um projeto único: são ferramentas Python independentes (Windows, Python 3.12, `ffmpeg`/`ffprobe` no PATH). Cada uma roda a partir da própria pasta.

| Ferramenta | O que é | Testes / execução |
|---|---|---|
| `kit-edicao-criativos/` | Pipeline de edição de ADs (legenda, setas, selo, upscale, troca de marca, dublagem). Regras próprias em `kit-edicao-criativos/CLAUDE.md` | `pip install -r requirements.txt`; teste rápido: `python ferramentas\finalizar.py video.mp4 --so-revisar` |
| `ferramentas/calculadora-cod/` | Unit economics do COD: `lib/modelo.py` é a conta; `adaptadores/` traduzem cada fonte (ex.: `helpship_csv.py`) para o contrato de pedidos descrito no README | `python -m unittest discover -s tests` |
| `ferramentas/corrigir-videos-tiktok/` | Site local (`servidor.py`, porta 8750) que corrige resolução/bitrate em lote | `python -m unittest discover -s tests` |
| `ferramentas/gerador-criativos-video/` | Gera criativo a partir de `roteiro.json` via fal.ai + ElevenLabs + HeyGen (API direta, `.env` próprio) | `python -m pytest tests/test_smoke.py -v` |
| `ferramentas/transcritor-youtube/` | Fila de links → transcrição (legenda do YouTube, senão Whisper local) | `python -m unittest discover -s tests -v` |
| `ferramentas/empacotar-skills.py` | Gera os .zip das skills de `.claude/skills/` para subir no claude.ai (a pasta local é a fonte de verdade) | `python ferramentas/empacotar-skills.py` |

Rodar um teste só: `python -m unittest tests.test_modelo.<Classe>.<metodo>` (dentro da pasta da ferramenta).

### Arquitetura do kit de edição (o que exige ler vários arquivos)
- `ferramentas/comum.py` define resolução/FPS/fontes; `montar_ad.py` lê uma receita JSON e delega a `montar_ad_rapido.py` (1 passada de ffmpeg: partes → legenda ASS de `legenda.py` → overlays de `overlays.py` → setas de CTA → compressão). Por fim chama `finalizar.py`, que decodifica tudo, checa resolução e áudio e gera `<nome>_frames.jpg` para revisão. `--classico` força o caminho antigo.
- Receita: `corpo` + `hook {"tipo":"antes"}` + `legenda` (`alinhamento:` do ElevenLabs, `transcrever` ou `texto:`) + `legenda_hook` (opcional, com `corrigir` para nomes de marca) + `selo` + `cta` + `resolucao` ("720" ou "1080") + `limite_mb`.
- Troca de marca em AD existente (fluxo usado nos lotes Lymphoria/Linfarele):
  1. `upscale_video.py` (Real-ESRGAN).
  2. Takes cortados com ≥3 s (padding com quadro congelado) e editados no Kling O1 Edit (Flora).
  3. `encaixar_edit.py` realinha o take de 24 fps ao tempo original e restaura a legenda queimada.
  4. `substituir_trechos.py` encaixa os takes no vídeo.
  5. `desfocar_regioes.py` e `trocar_texto_tela.py` cuidam de telas de celular e legendas.
  6. `trocar_trecho_audio.py` troca a fala com voz clonada (`clonar_voz.py` + `tts_elevenlabs.py`).
  7. O fim novo é montado e passa por `montar_ad.py`.
  As receitas por AD e os orquestradores (`processar_ad.py`, `processar_it.py`) ficam em `Downloads/LHYMPORIA AD 01-20/*/_trabalho/`.
- **Tradução de criativo de outro idioma** (fluxo usado em `Downloads/PODADORA-CL/`, inglês → espanhol do Chile):
  1. Transcrever com faster-whisper e ler o texto da tela com RapidOCR (`rapidocr_onnxruntime`).
  2. Reescrever o roteiro para o mercado: sem preço estrangeiro, com a oferta local.
  3. Gerar a fala com voz clonada (`clonar_voz.py` + `tts_elevenlabs.py`).
  4. Separar a música da voz original com `python -m demucs --two-stems=vocals` e usar só o `no_vocals.wav`.
  5. Cobrir o texto queimado, recortar trechos, desfocar terceiros e trocar o áudio pela narração + fundo do demucs:
     `preparar_corpo_traducao.py prep.json` (faixa/caixas opacas, título/caixa de gancho nova, aviso no rodapé,
     desfoque por chaves interpoladas, fim congelado para caber o CTA; gera `corpo.mp4` + `alinhamento.json`).
     Era o `preparar_corpo.py`/`montar_base.py`/`construir_base.py` dos lotes Podadora e Wyze.
  6. Montar com `montar_ad.py`. Quando o original tem o rosto do criador, o corpo sai de `montar_corpo_avatar.py plano.json`
     (avatar HeyGen intercalado com takes recortados abaixo do rosto, tela cheia ou dividida).
- **Variações gancho × corpo** a partir de vídeos já prontos: `gerar_variacao.py` do kit (era `_variacoes/gerar_variacao.py`
  da Podadora e `variacoes/gerar_var.py` + `prep_fonte.py` do Drenagem).
  - `gerar_variacao.py banco <video>` gera o banco de tomadas (`scdet` + grupos de cena contínua + transcrição por palavra);
    `gerar_variacao.py fundo <video> --ate <corte>` separa a música (demucs); `gerar_variacao.py montar config.json` monta.
  - Corta com margem nas bordas de cada tomada (o `scdet` não é exato) e não repete pedaços da mesma cena contínua.
  - Modo A: gancho novo (fala + cenas do banco + caixas por frase) + AD pronto a partir do `corte`. Modo B: corpo novo
    montado do banco sobre uma narração (+ `receita_final.json` para o `montar_ad.py`). Formato em `exemplos/variacao_exemplo.json`.
  - Estáticos e carrossel saem de quadros reais com `_variacoes/est/gerar_estaticos.py` (ainda na pasta do lote).
- **Baixar vídeo sempre na maior qualidade (≥720p).** Na Biblioteca de Anúncios do Meta o `<video src>` do player é a versão SD (360p): capture o `video_hd_url` nas respostas da página com Playwright + Chrome headless (modelo pronto: `Downloads/ADLIB-104060992792639/buscar_hd.py`) e confira com `ffprobe`. Deduplique por md5 (a mesma página sobe o mesmo vídeo em vários anúncios). yt-dlp: `-f "bv*+ba/b"`. Fonte abaixo de 720p: avisar antes de produzir.
- **Armadilhas que já custaram retrabalho:**
  - **Lipsync HeyGen (`create_lipsync`) sobre vídeo existente:** o vídeo de entrada precisa ter o **áudio ORIGINAL** (idioma de origem) e o áudio novo vai separado. Mandar o vídeo já com o áudio novo embutido faz o HeyGen devolver a boca intacta (custa ~1 crédito e parece "pronto"). Confira comparando a região da boca original × saída. Mande trechos de **até ~12 s**: um de 24 s travou por mais de 30 min, e em 2 partes de 12 s saiu em 4 min. **Use `mode speed`, não `precision`**: no precision, nas pausas do áudio novo a boca continua articulando o idioma original. Com 2+ rostos no plano, recorte a entrada só no rosto de quem fala e cole de volta (elipse suave em boca e queixo). Plano B sem crédito: colar uma boca fechada do próprio trecho nas pausas (`ADLIB-104060992792639/producao/_trabalho/ad01/lipsync2/fechar.py`). Critério de aceite: `checar_lipsync.py` com índice de pausa ≤ 0,6 medido no rosto de quem fala.
    - **Job do HeyGen parado:** se passar de ~45 min em "processing", reenvie igual. O reenvio costuma voltar em ~25 min.
    - **Custo:** a cobrança do speed aparece até ~1 h depois. Meça o saldo (`get_current_user`) antes e ~1 h depois do último job. O lote Oración (18 ADs, ~1–2 min cada) custou **~150–170 créditos no total (~9 por AD)**. A conta "1 crédito/s" dos primeiros testes superestimou 10x.
    - Lições completas: `ADLIB-104060992792639/producao/_trabalho/LICOES-LIPSYNC.md`.
  - **Cor escurecendo a cada passada (lote Oración):** ler quadros com cv2/ffmpeg e regravar perdia 2–3 níveis de luma por passada. O motivo: o cv2 lê bt709 quando há etiqueta e bt601 quando não há, e os encoders gravam bt601 com etiqueta bt709. Nos scripts que leem e regravam quadros, use leitura e gravação com a matriz bt601/tv **fixa**: `ADLIB-104060992792639/producao/_trabalho/ad13/lipsync3/comum3.py` (`quadros()` + `ENC_VF` + `ENC_TAG`). Num trecho colado (lipsync), ajuste a cor pelo anel de pele em volta da boca (`_lote/cor_trecho.py`). Confira a média de luma original × final.
  - **Remover legenda queimada sem borrão e sem custo:** LaMa na GPU local. O venv fica em `ADLIB-104060992792639/producao/_trabalho/_vg` e o modelo pronto em `_lote/lama_base.py`. É a alternativa gratuita ao Vmake.
  - **PowerShell × Git Bash:** rode `revisar_ad.py --lipsync "a:b:c,..."` pelo PowerShell, porque o Git Bash converte os `:` como caminhos. A lista de termos proibidos vai num `.txt` em UTF-8, porque dentro de um `.ps1` o PowerShell 5.1 corrompe os acentos.
  - **Kling O1 Edit** recusa vídeo com menos de 3 s. Corte com `-ss ini -t dur` + `tpad=stop_mode=clone`. Com `-frames:v` o padding é cortado.
  - **Bash:** scripts do kit que imprimem "≈" ou acentos quebram no cp1252. Rode com `PYTHONIOENCODING=utf-8`.
  - **CPU:** Whisper e OCR em paralelo disputam a CPU e ficam até 10× mais lentos. Rode em sequência.
  - **Faixa sobre texto queimado:** precisa ser quase opaca (alpha ≥ 250), senão o texto original aparece por baixo.
  - **`encaixar_edit.py` (corrigido em 05/10/2026):** a restauração da legenda copiava do original todo pixel branco do quadro inteiro, e isso trazia de volta o texto branco do rótulo antigo por cima do take do Kling. Agora a cópia fica limitada à faixa da legenda (0,62–0,90 da altura). Confira o rótulo com zoom: a folha de contato não mostra esse defeito.
  - **Kling em cenas Pixar** costuma trocar o rosto ou deixar o personagem fotorrealista. Uma alternativa sem custo é `trocar_rotulo_faixa.py` do kit (era `ad25/band_fix.py`, `ad03/band_fix2.py`, `ad24/band_fix3.py` e `band_box.py`): acha a faixa do rótulo pela cor (`--auto`, ROI com chaves por quadro), segue pelas linhas (`--seguir`, `--cor escuro`) ou usa caixa marcada à mão (`--caixa`), apaga o texto e reescreve a marca no mesmo ângulo. Outra é colar só a região do frasco editado sobre o original (`ad05/flora/comp_regiao.py`).
  - **Revisão automática:** `revisar_ad.py` do kit junta os revisores dos lotes (whisper no idioma alvo + residual, termos proibidos, folha de contato, quadro solto, silêncio no fim, salto de pts no áudio e setas sobre a faixa) e sai com código 1 quando acha problema.
  - **Selo e setas:** na receita em 720p, use selo `y≈1110` e `cta.y≈1490` quando houver faixa no rodapé, para as setas não ficarem em cima dela.
  - **Revisão:** subagentes revisores (whisper es/en + OCR + folha de contato) pegaram defeitos que a folha `_frames.jpg` não mostra: quadros soltos nos cortes, silêncio no fim e setas sobre o aviso.
  - **`montar_ad_rapido.py` (corrigido em 05/10/2026):** corpo montado por concat `-c copy` de takes com metadados de cor diferentes (HeyGen sem tag + vídeo original `tv/bt709`) fazia o ffmpeg "reconfigurar o filtergraph" no meio do vídeo: as entradas PNG (setas/manchete) já estavam em EOF e sumiam dali em diante, e o buffer do `loudnorm` (~3 s) era descartado, abrindo um salto de pts de 3 s no áudio (no AD 06 do lote Wyze: 8,49→11,49 s, fala dessincronizada). Agora o corpo entra com `-reinit_filter 0`. O `silencedetect` NÃO pega esse defeito (o salto fica nos timestamps): confira com `ffprobe -select_streams a -show_entries packet=pts_time` ou compare a duração do áudio decodificado com a do corpo. O `--classico` não é afetado (usa `-vf`/`-af` separados).
- Chaves: `kit-edicao-criativos/.env` (ElevenLabs) e `skills/vmake-skill/scripts/.env` (Vmake). Não ler nem imprimir.
- MCPs do projeto (`.mcp.json`): `dropkiller`, `chegou-operacoes`. Do kit: Flora, HeyGen, ElevenLabs.

## Público final

- Consumidores finais dos anúncios: leads COD, compradores de infoproduto, clientes X1 (50+).
- Internamente: uso próprio e da equipe de closers, produção e mentorados.

## Estrutura do projeto

```
contexto/                  → perfil de trabalho, regras de organização, prioridades da rotina,
                              modelo de relatório, preferências visuais, tom de comunicação e
                              informações importantes para orientar as tarefas
00-inbox/                  → arquivos novos ainda não triados ou categorizados
01-arquivos-organizados/   → arquivos já processados e movidos para seus destinos finais
02-relatorios/             → relatórios de performance de campanha e operação (por frente/oferta/país)
03-dashboards/             → dashboards de métricas e indicadores
04-apresentacoes/          → apresentações internas (estratégia, resultados, planejamento)
05-pdfs-didaticos/         → materiais de apoio, guias e documentação de processos
06-infograficos/           → resumos visuais, comparações e fluxos de processo
07-notion-sync/            → arquivos sincronizados/exportados do Notion (catálogo de preços, hubs de oferta)
sops/                      → procedimentos operacionais padrão da produção e das campanhas
templates/                 → modelos reutilizáveis (roteiro, relatório, briefing de criativo etc.)
```

> Estado atual do disco: existem `Contexto/` (maiúscula, ainda vazia), `01-arquivos-organizados/`, `02-relatorios/`, `03-dashboards/`, `05-pdfs-didaticos/`, `06-infograficos/`, `ferramentas/`, `skills/`, `kit-edicao-criativos/` e os atalhos `entregas-lymphoria/` e `entregas-linfarele/` (junctions para `Downloads/LHYMPORIA AD 01-20/`). As pastas `00-inbox/`, `04-apresentacoes/`, `07-notion-sync/`, `sops/` e `templates/` ainda não foram criadas: crie quando a primeira saída daquele tipo for gerada.
>
> Nota: hoje existe uma pasta legada `001- INBOX/` com arquivos de mídia, pessoais e administrativos ainda não triados. Ao organizar essa pasta, siga as regras de segurança e separação abaixo (nunca mover/apagar sem autorização, sempre gerar índice) — trate-a como o atual `00-inbox/` até que a triagem esteja concluída.

## Regras principais do projeto

- Sempre leia os arquivos relevantes da pasta `contexto/` antes de executar tarefas importantes. Use-os para entender como a pessoa trabalha, quais são suas prioridades por frente de negócio, como os materiais devem ser organizados, qual tom usar nos relatórios e quais preferências visuais seguir.
- Informações pessoais, dados sensíveis, agenda, viagens, compromissos, documentos privados e dados financeiros pessoais devem ser tratados apenas como contexto de organização e produtividade. Nunca devem aparecer em materiais externos (criativos, páginas de vendas, relatórios para clientes/mentorados) a menos que explicitamente solicitado.
- Arquivos pessoais, recibos, comprovantes, documentos privados e arquivos administrativos devem ser separados dos materiais de campanha, criativos e comerciais. Nunca misture arquivos pessoais com materiais destinados a anúncios, funis ou entrega a terceiros.
- Nunca apague arquivos sem autorização explícita. Quando houver dúvida, copie os arquivos para a nova pasta organizada em vez de mover ou alterar os originais.
- Nunca invente dados sobre produtos, fornecedores, custos, ofertas, mercados, métricas de campanha, tarefas, compromissos ou resultados. Quando algo não estiver claro, registre como "precisa de revisão manual".
- Ao organizar arquivos, sempre gere um índice com nome original, novo nome, categoria, frente de negócio (COD/Infoproduto/X1), nova localização e observações. Também gere um relatório final explicando o que foi feito.
- Ao criar materiais, sempre considere objetivo, público-alvo, frente de negócio, país/mercado, formato de saída, nível de profundidade, tom de comunicação e uso final do material.

## Regras para apresentações

Estrutura padrão sugerida (adaptável ao objetivo do material — reunião, planejamento, treinamento de closers, resultado de campanha):

Capa → Contexto/introdução → Objetivo do material → Problema/tema/assunto principal → Explicação central → Exemplos ou aplicações práticas → Passo a passo/método/processo → Atividade/reflexão/ação prática → Erros comuns, cuidados ou pontos de atenção → Resumo final → Próximos passos → Encerramento.

## Regras para roteiros e materiais de apoio

- Roteiros de criativo (vídeo/imagem) devem ter: hook, sequência clara, falas de apoio, prova/exemplo, chamada para ação (CTA) e, quando aplicável, transições e fechamento.
- Ao criar materiais de apoio (SOPs, briefings, checklists de produção), prefira formatos visuais, didáticos e fáceis de consultar depois: PDF, checklist, resumo visual, guia, infográfico ou documento explicativo.

## Regras para relatórios e dashboards

- Relatórios de performance devem usar tom profissional, objetivo, organizado e didático, e incluir: contexto (frente/oferta/país/período), o que foi analisado, principais achados, pontos de atenção, recomendações e próximos passos práticos.
- Dashboards devem usar apenas dados disponíveis (extraídos de Meta Ads/Kwai Ads/TikTok Ads/Notion/planilhas). Nunca inventar métricas como CPA, ROAS, ticket médio ou margem. Se faltarem dados, explicar a limitação.
- Priorize indicadores relevantes por frente: CPA e margem por produto/país (COD); CAC, ticket e conversão de funil (Infoprodutos); taxa de efetividade de pagamento e fechamento por closer (X1 After-Pay).

## Regras para ferramentas externas e priorização de tarefas

Ao trabalhar com Notion, planilhas, calendários ou exports, considere colunas típicas: A fazer, Fazendo, Em revisão, Aguardando, Feito, Prioridade alta, Próximos prazos, Ideias, Materiais pendentes.

Ordem de priorização de tarefas:
1. Tarefas com prazo mais próximo.
2. Tarefas de prioridade alta.
3. Tarefas em andamento.
4. Tarefas que desbloqueiam outras (ex.: criativo pendente travando lançamento de campanha).
5. Materiais necessários para compromissos já agendados.
6. Entregáveis reutilizáveis (templates, SOPs).
7. Organização de arquivos importantes (catálogo, fornecedores, Notion).
8. Melhorias visuais e refinamentos.

Se faltarem dados para priorizar corretamente, registre a limitação e indique quais informações precisam de revisão manual.

## Regras para criação de Skills genéricas

Ao criar Claude Skills para este projeto, mantenha-as genéricas e reutilizáveis, definindo apenas o fluxo de trabalho e o processo. Não inclua detalhes específicos de produtos, fornecedores, ofertas, mercados, agenda ou ferramentas específicas diretamente na skill. As skills devem servir para diferentes contextos de tráfego pago, produção de criativos e gestão de funis.

## Regras para criação de agentes genéricos

Ao criar agents para este projeto, mantenha-os genéricos e reutilizáveis. Nunca escreva detalhes específicos de produtos, fornecedores, ofertas, clientes ou agenda diretamente nos arquivos dos agents. Os agents devem buscar contexto em tempo de execução (em `contexto/`, `07-notion-sync/` etc.) para continuarem reutilizáveis. Cada agent deve ter função clara e sem sobreposição com outros agentes.

## Regras de roteamento visual

- **Apresentação**: conteúdo para reunião, treinamento de equipe/closers, planejamento estratégico, explicação ao vivo.
- **PDF**: material de apoio, SOP, guia, documentação de processo, entrega final ou consulta posterior.
- **Dashboard**: quando houver dados de campanha, métricas, prazos, progresso ou indicadores.
- **Infográfico**: comparação, passo a passo, resumo visual, regra ou processo curto.
- **Checklist**: execução prática, conferência, revisão de criativo ou rotina de publicação.
- **Flashcards**: memorização, revisão rápida de conceitos/roteiros/objeções.
- **Planilha**: dados tabulares, controle de fornecedor/preço, acompanhamento de tarefas, base estruturada.

## Regras de nomes de arquivos

Padrão: `AAAA-MM_frente_tipo_assunto.extensao` (usar a frente de negócio — `cod`, `infoproduto` ou `x1` — quando fizer sentido). Sem data clara: `frente_tipo_assunto.extensao`. Sem espaços, letras minúsculas, separadas por hífen ou underline.

Exemplos:
- `2026-06_cod_relatorio_performance-chile.pdf`
- `2026-06_infoproduto_apresentacao_planejamento-onda-tesla.pptx`
- `2026-06_x1_dashboard_efetividade-pagamento.xlsx`
- `2026-06_cod_planilha_fornecedores-colombia.xlsx`
- `pessoal_comprovante_aluguel.pdf`
- `sop_infografico_fluxo-producao-criativo.png`

## Regras para tarefas envolvendo materiais incompletos

Ao criar materiais, sempre verifique se existem arquivos complementares importantes (roteiro, apresentação, PDF de apoio, resumo, checklist, infográfico, dashboard, planilha, material visual, relatório final). Se algo estiver faltando, sugira criar ou registre como pendência.

## Regras de segurança

- Nunca apague, sobrescreva ou modifique arquivos originais sem autorização clara.
- Nunca exponha dados pessoais, financeiros, de fornecedores ou custos internos em criativos, páginas de vendas ou materiais externos.
- Nunca misture arquivos pessoais com arquivos de campanha, criativos ou comerciais.
- Nunca invente dados, métricas, nomes de fornecedores, custos, datas, clientes ou resultados.
- Sempre indique quando algo precisa de revisão manual e explique limitações quando os dados forem insuficientes.
- Sempre confirme antes de executar alterações destrutivas (mover/apagar arquivos em massa, especialmente na pasta legada `001- INBOX/`).
- Sempre gere outputs na pasta apropriada, mantendo organização, clareza e rastreabilidade.

## Checklist de qualidade antes de finalizar qualquer tarefa

- O objetivo da pessoa foi atendido?
- A frente de negócio correta (COD/Infoproduto/X1) foi considerada?
- Os arquivos relevantes de `contexto/` foram consultados quando necessário?
- O output foi salvo na pasta correta?
- O nome do arquivo está claro e padronizado?
- O conteúdo está correto, organizado e sem informações inventadas?
- A gramática, ortografia e acentuação foram revisadas (considerando também termos em espanhol/inglês quando aplicável ao mercado)?
- Dados pessoais, financeiros ou de fornecedores foram protegidos?
- Arquivos originais foram preservados?
- Foi gerado índice, relatório ou resumo quando necessário?
- As limitações foram explicadas?
- Os próximos passos ficaram claros?
