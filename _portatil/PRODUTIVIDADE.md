# Ferramentas de produtividade, economia de tokens e prevenção de erros

Tudo isto vai junto no repositório. Depois de rodar o `restaurar.ps1`, o PC novo trabalha igual a este.
A lista completa das skills, com a descrição de cada uma, está em `SKILLS-CATALOGO.md` e é atualizada a cada `coletar.py`.

## 1. O que roda sozinho no Claude Code

| Ferramenta | O que faz | Onde está |
|---|---|---|
| **Mod «progresso»** | Barrinha de progresso no chat, recolhida e expansível. Mostra a barra de limite de 5 h e o modelo, faz os próximos passos virarem perguntas de múltipla escolha e, no fim de cada tarefa, dá **dicas de economia de tokens** (arquivo grande lido inteiro, leitura repetida, modelo pesado em tarefa simples, conversa longa, pedido vago, comandos demais) | `claude-home/mods/progresso` (ligado pela variável `CLAUDE_CODE_PLUGIN_DIRS`) |
| **Hook de voz** | Fala «Sávio, terminei» quando o Claude termina, e registra a atividade | `claude-home/hooks/` (`falar.ps1`, `atividade.py`) |
| **Painel ao vivo** | Página em http://127.0.0.1:8765 com as etapas, as imagens e os custos de cada produção, aberta numa aba do VS Code | `painel/` (`iniciar.ps1`, `painel.py`) |
| **Central de Projetos** | Uma conversa que manda pedidos para o Claude de cada projeto e mostra a sala de agentes | Repositório separado: `Grupo-Chegou-Geral/central-de-projetos` |
| **Permissões já liberadas** | Comandos e ferramentas que não pedem confirmação | `claude-home/settings.local.projeto.json` |
| **CLAUDE.md global e do projeto** | Regras de trabalho, armadilhas técnicas e estrutura das pastas | `claude-home/CLAUDE.md` e `CLAUDE.md` na raiz |
| **Memória** | Cerca de 60 fatos: preferências, lotes feitos e lições | `claude-home/memory/` |

## 2. Skills (receitas que evitam reexplicar e errar)

- **Produção de criativo:**
  - `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`: montar, gerar e revisar;
  - `traduzir-criativo` e `adaptar-marca`: lotes;
  - `replicar-vencedor-organico`: reel viral vira anúncio;
  - `completar-criativo`: raio-x de um criativo pronto;
  - `estrategista-criativo`: plano de produção;
  - `andromeda`: diversidade do lote e estrutura de campanha;
  - `analista-de-copy`: copy antes e depois de rodar.
- **Inteligência:** `consultor-de-cases` (base de 49 podcasts + 8 dossiês) e as skills de mineração e espionagem do claude.ai (mineração de ângulo, clickbait, formatos virais, infoproduto escalado, espião de funil, dissecação de criativo, benchmarking, estudo de público).
- **COD e loja:** páginas de produto Shopify, espelhar e clonar loja entre países, varredura e processamento de pedidos COD, auditoria de novedades Dropi, transportadoras, comparar fornecedores.
- **Organização:** `organizacao-de-arquivos`, `morning` (rotina do dia), `manter-central-operacao`.

Receitas por oferta (os dados que as skills genéricas leem em tempo de execução): `contexto/receitas/`.

## 3. Economia de tokens (regras que já funcionam)

1. **Trabalho pesado sem token:** transcrição (Whisper local), separação de voz e música (demucs), OCR, folhas de contato e revisão automática (`revisar_ad.py`) rodam localmente. O Claude só lê o resultado.
2. **Estudo antes de produzir, em texto:** transcrição + folha de contato (1 imagem) no lugar de assistir vídeo quadro a quadro.
3. **Subagentes para volume:** lotes grandes vão para agentes em paralelo, de preferência no Sonnet para tarefas mecânicas como fichar e montar. A conversa principal só recebe o resumo.
4. **Um script em vez de dez comandos.** Cada saída de terminal entra no contexto, então o melhor é um script que roda a sequência e imprime só o resumo.
5. **Leitura cirúrgica:** em arquivo grande, aponte a função ou o trecho em vez de ler inteiro.
6. **Narração mínima:** uma linha no começo e um resumo no fim.
7. **Pedido específico:** diga arquivo, pasta e resultado esperado. Pedido vago gera exploração cara.
8. **Conversa longa:** use `/compact` ou abra sessão nova quando trocar de assunto.
9. **Contexto que se repete** (oferta, regras, persona) fica em arquivo de receita e skill, não é reescrito no chat.
10. **Material pesado de leitura** (ex.: fichar 49 podcasts) pode ir para outro Claude em lotes, para poupar o limite semanal daqui.

## 4. Prevenção de erros (checagens fixas)

- **Antes de gastar:** roteiro aprovado com «confirmo» e orçamento com custo + tempo + opção mais barata.
- **Checklist de abertura numa mensagem só:** oferta, preço sim ou não, escassez real, mercado e idioma, orçamento de mídia, música, formato.
- **Revisão automática** `revisar_ad.py --idioma X --idioma-residual Y`: fala residual, termos proibidos, quadro solto, silêncio, salto de pts, setas.
- **OCR a cada 0,5 s** sem texto no idioma antigo, folha de contato olhada e lipsync conferido a olho.
- **Chiado:** medir os agudos por trecho em toda voz TTS ou gritada e em toda trilha separada pelo demucs.
- **Nunca alterar a base:** a correção vira arquivo novo e as versões antigas ficam guardadas (v1, v2).
- **Agentes em paralelo:** divisão definida antes, subpasta própria por agente, arquivo `PRONTO.txt`, teto de custo por agente e no máximo 1 refação paga sem avisar.
- **Antes de subir para o GitHub:** `coletar.py` pula URLs assinadas e chaves, e vale varrer de novo antes do push.

## 5. Manter os dois PCs iguais
```
git pull                          # antes de começar
python _portatil\coletar.py       # depois de trabalhar: memória, mods, skills, scripts dos lotes
git add -A && git commit -m "..." && git push
powershell -File _portatil\restaurar.ps1   # no outro PC, depois do pull
```
