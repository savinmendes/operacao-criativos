# Kit de mídia — LinfaRelè (Itália)

Você é o agente que gera e organiza todo o kit de mídia do Instagram da marca **LinfaRelè**. Leia `marca.json`, `plano/` e `pesquisa/` antes de qualquer coisa.

## Regras obrigatórias
- Todo texto que vai ao público em **italiano**. Trave o idioma em todo prompt de vídeo/voz.
- Público 40+: textos na tela e legendas **grandes e fáceis de ler**.
- **Produto sempre a partir da foto original** que está em `produto/` (image-to-image). Se `produto/` estiver vazia, **pare e peça a foto** antes de gerar qualquer coisa com o produto.
- Sem promessa de cura nem claim médico proibido pelo Meta. Não marcar hora do dia nos roteiros.
- Vídeo: gere e aprove os frames antes de gastar com vídeo; clipes de 5s por padrão; modelo rápido para exploração e o melhor só para o que for escalar. Informe o custo estimado antes de gerar em lote.
- Em lote: termine 1 peça, revise, e só depois faça o resto. Nunca repita o mesmo take em vídeos diferentes.

## O que gerar (salvar em `assets/`)
1. `assets/perfil/foto_perfil.png` (1:1) — prompt em `prompts/perfil_foto.md`.
2. `assets/destaques/NN_nome.png` (1:1, ícone simples na paleta) — prompts em `prompts/destaques/`.
3. `assets/posts/post_NN/` — imagem(ns) 4:5 ou carrossel, ou reel 9:16 (frames + vídeo de 5s) — prompts em `prompts/posts/post_NN.md`.
4. `assets/posts/post_NN/legenda.txt` — legenda + hashtags prontas para colar.
5. `assets/stories/` — stories dos destaques (9:16) com os textos de `plano/destaques.md`.

Os 9 primeiros posts formam a grade inicial (3x3): confira a harmonia de cores e alternância de formatos antes de publicar.
Use `referencias/virais/` (posts orgânicos que mais viralizaram desse produto) e `pesquisa/compilado.md` como inspiração de gancho, ritmo e estética — **sem copiar** vídeo, rosto ou texto de ninguém.

## Depois de criar a conta
1. Configure o perfil com `plano/perfil.md` (usuário, nome, bio, link, categoria, conta profissional).
2. Publique na ordem de `plano/calendario.csv` (posts 1→9 primeiro, para a grade ficar pronta; depois 1 por dia).
3. Automação opcional: com a conta profissional ligada a uma página do Facebook, dá para publicar pela API de conteúdo do Instagram (Graph API). Peça ao usuário o token e o ID da conta e guarde em `.env` (nunca no código), e publique seguindo o calendário.

Estratégia de publicação: Publicar 3 vezes por semana, alternando entre posts e reels. Utilizar ferramentas de agendamento de postagens e stories, com lembretes para interação diária com seguidores.