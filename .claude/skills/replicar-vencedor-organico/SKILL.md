---
name: replicar-vencedor-organico
description: Pega um vídeo orgânico que já viralizou num perfil PRÓPRIO (ranking por likes) e o replica como anúncio de uma oferta, mantendo os takes, a estrutura e o ritmo do original, trocando só a figura de autoridade pela persona da página que anuncia e adaptando fala, textos de tela e CTA ao funil. Inclui baixar e ranquear o perfil, raio-x, roteiro para aprovação, produção barata com o que já existe, ganchos alternativos e revisão. Use quando a pessoa pedir "replica o ranking N", "adapta esse viral para a oferta X", "faz igual ao top do perfil para o anúncio", ou mandar um ranking de vídeos do próprio perfil para virar criativo.
---

# Replicar vencedor orgânico

O vídeo orgânico de muitos likes já provou gancho, história e ritmo. A receita mantém tudo isso e muda só o que liga o vídeo ao funil: idioma, quem tem autoridade, o que o vídeo promete e o CTA. Montagem, mídia IA e revisão seguem `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`; leia antes o `CLAUDE.md` do kit (armadilhas de lipsync, cor, LaMa, salto de pts). Nunca leia nem imprima `.env`.

## 0. Contexto (sempre primeiro)
- Leia o arquivo da receita da oferta em `contexto/receitas/` (ex.: `contexto/receitas/<oferta>-ranking.md`). Ele guarda: nome e rosto da persona da página, vozes, o que o funil entrega e o que **não** pode ser revelado no anúncio, título e texto do anúncio, botão, selo, pastas de referência e o que já foi produzido. A skill não guarda dado de oferta: se o arquivo não existir, crie-o com a pessoa antes de produzir.
- Confirme que o perfil é **da própria pessoa** (ou autorizado). Se for de terceiro: só estrutura e ritmo; rostos, falas e "provas" são recriados do zero (ver `completar-criativo`, regra de referência de terceiros).
- Registre as etapas no painel do projeto (`painel/painel.py`), se existir.

## 1. Ranking (sem custo)
1. Vídeos do perfil baixados na maior qualidade, nomeados `NN_<likes>k_<código>.mp4` + `_legenda.txt`, numa pasta única ordenada; `00_RANKING_VIDEOS.txt` com likes, comentários, data e link.
2. Avise se o perfil não carregou inteiro (ranking incompleto).
3. Comece pelos de mais likes (`feedback`: priorizar vencedores).

## 2. Raio-x do original (sem custo)
Na pasta `_analise_NN/`:
1. Transcrição (faster-whisper; idioma automático) → `transcricao.txt`.
2. Folha de contato (1 quadro a cada 2–2,5 s) + close dos 3 primeiros segundos.
3. Tabela da estrutura: tempo · bloco · o que acontece (gancho, depoimento, autoridade, ritual/mecanismo, prova, objeção, CTA).
4. Por que viralizou (1–3 motivos concretos) e **o que quebra no funil** (ex.: revela algo que o funil ensina diferente, CTA para outro produto, escassez falsa, fala depois do CTA, duração).
5. Compare com o que já foi produzido (arquivo da receita): se a história repete uma peça existente, diga qual é o diferencial deste original.

## 3. Roteiro para aprovação
`_analise_NN/ROTEIRO_<oferta>_RANKINGNN_v1.md`, tabela `# · tempo · quem · fala · cena`:
- **Mesmos takes do original, na mesma ordem.** Muda só a figura de autoridade → persona da página, **no mesmo cenário do original** (mesmo fundo, móveis, microfone, enquadramento).
- Fala no idioma do mercado, reescrita (não traduzida palavra a palavra), no tom pedido (a pessoa prefere incisivo).
- O ritual/mecanismo **não revela** o que o funil ensina: mostrar o começo e cortar ("¡Alto! el resto no lo puedo decir aquí") para o clique fechar o loop.
- Fora: nomes e marcas de terceiros, produto de outra oferta, números de prova copiados de outro perfil, escassez falsa, fala depois do CTA. Um CTA só, no fim.
- Citação religiosa/bíblica: conferir a referência real (o original pode errar).
- Mostre o roteiro completo no chat e **espere aprovação explícita** antes de gastar (regra de criativo).

## 4. Produção (caminho barato, reaproveitando)
- **Personagens dos takes originais**: lipsync (HeyGen speed; entrada com o áudio original, áudio novo separado, ≤12 s). Rosto de perfil ou ilegível não sincroniza: avise e deixe a pessoa decidir (aceitar / outra ferramenta / regerar a cena).
- **Legenda queimada antiga**: sobre corpo ou fundo, cubra com a legenda nova numa caixa opaca no mesmo lugar (alpha ≥ 250). **Sobre rosto, não use LaMa** (fica borrado): gere um retrato novo nítido do mesmo personagem a partir do quadro mais limpo e anime no avatar (HeyGen Avatar IV 720p), boca fechada e expressão certa no retrato base.
- **Persona da página**: retrato no cenário do original a partir da referência da receita; avatar cortado nas fronteiras das palavras; pausas cobertas por b-roll; uma inserção a cada 3–4 s (nunca 20 s+ só de avatar).
- **Vozes**: uma por personagem, registradas no arquivo de vozes da receita; sem clonar se a conta estiver no limite.
- **Efeitos-padrão da receita** (faixa/rodapé no idioma, glitch no corte do ritual, "EN VIVO", setas para o botão, selo, trilha em 2 climas a −32 LUFS).
- **Áudio**: voz gritada/TTS brilhante chia — passe de-esser + shelf nos agudos só no trecho (compensar volume) e confira o perfil de agudos por trecho antes de entregar.
- B-roll: só o que **prova** o que é dito; sem marca de terceiro visível; nenhum take repetido.

## 5. Ganchos alternativos (opcional, mesmo corpo)
5 aberturas visualmente diferentes sobre o mesmo corpo: origem validada (título vencedor da conta), contraintuitivo, loop aberto, filtro de identidade, cena cotidiana. Reaproveite takes do original; no máximo 1 cena nova gerada.

## 6. Revisão e entrega
- `revisar_ad.py --idioma <alvo> --idioma-residual <origem>`, OCR a cada 0,5 s sem texto no idioma antigo, folha de contato olhada, lipsync a olho, setas fora da legenda, sem salto de pts.
- Entrega em `_analise_NN/ENTREGA/` com `_texto-anuncio.txt` (título, botão, texto principal do vencedor da conta). Versões anteriores ficam em `producao/` (`_v1`, `_v2`); nunca sobrescreva sem guardar.
- Abra o vídeo e a pasta para a pessoa; link clicável via junção em `08-entregas/`.
- Atualize o arquivo da receita (o que foi produzido, custo real, o que deu errado) para o próximo ranking sair melhor.
