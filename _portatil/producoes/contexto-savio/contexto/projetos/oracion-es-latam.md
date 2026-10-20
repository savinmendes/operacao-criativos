# Oración ES LATAM: 18 vídeos de oração PT → ES (página Keiko Tanaka)

> Tradução com voz clonada e lipsync HeyGen de 18 criativos de oração da página da pessoa. Abra ao continuar esse lote, ao fazer a versão Espanha ou ao fazer lipsync sobre vídeo existente.

## Contexto de uso
- **Frente:** Infoproduto (espiritualidade). Produto e oferta novos **ainda não definidos** no momento da entrega (CTA genérico, sem selo).
- **Fonte:** página da Biblioteca do Meta id 104060992792639 ("Keiko Tanaka"), **da pessoa** (confirmado em 07/10/2026). Os originais se perderam; a fonte são as cópias HD da Biblioteca (`UNICOS_HD\`, capturadas com `buscar_hd.py`).
- **Pasta:** `Downloads\ADLIB-104060992792639\` (atalho `entregas-adlib-keiko/`). Entrega numerada em `ENTREGA-ES-LATAM\` (01–18 + `00-RELATORIO.md`); trabalho em `producao\_trabalho\adNN\RELATORIO.md`; revisões independentes em `producao\_trabalho\revisao\` (lotes A, B, C); briefings `BRIEFING-PILOTO.md`, `BRIEFING-TESTE-11.md`, `BRIEFING-LOTE.md`.
- **Entregue em 08/10/2026:** 18 vídeos 720x1280 em espanhol neutro (EUA hispânico + LATAM), de 0:18 a 2:00. Temas: Tres bendiciones (01, 02), Padre romero (03), Envidia (04), Familia (05), Nudo (06, 10, 16, 17), Cinta blanca (07), Bendición detenida (08), Serpientes (09, 12, 14, 18), Desatadora (11), Paz (13), Regalo (15). 12×14 e 01×02 são testes A/B de gancho com o mesmo corpo.
- **Formato aprovado pela pessoa:** plano original (Jesus atrás) + a mesma personagem falando espanhol (voz clonada) + lipsync. **Avatar completo foi testado e rejeitado.**
- **Retirado do roteiro:** promessas de dinheiro (depósito, PIX, valores), cura e doença, ameaças ("se pular, a bênção some"), contagem regressiva, depoimentos com resultado (viraram "sintió paz y esperanza"), pessoa famosa. Na imagem: legenda PT apagada; cédulas, PIX, hospital e remédios trocados ou reenquadrados.
- **Custos:** ElevenLabs ~US$ 6–7. HeyGen: o relatório estimou ~1.500–1.800 créditos pela conta "1 crédito/s"; a medição posterior (registrada no CLAUDE.md do projeto) deu **~150–170 créditos no total (~9 por AD)** — a conta por segundo superestimou 10x. Remoção de legenda e cor: local, sem custo.
- **Qualidade:** índice de pausa de todos entre 0,07 e 0,44 (meta ≤ 0,6; o AD 11, aprovado pela pessoa, ficou em 0,38). O revisor reprovou e mandou corrigir 01, 02, 05, 08, 09, 10, 13, 16, 17 e 18 antes da aprovação.
- **Pendências:** produto novo e oferta (selo/CTA específico; remontagem sem custo de lipsync); versão Espanha (castelhano); textos dos anúncios; olhar risco Meta nas aberturas reenquadradas do 10 e do 16 e no homem triste do 17; trechos de fala contínua aprovados a olho (16 em 69–76 s, 09 trecho O).

## Lógica de uso
1. **Baixar sempre em HD:** na Biblioteca do Meta o `<video src>` é 360p; capturar o `video_hd_url` com Playwright (`buscar_hd.py`), conferir com `ffprobe` e deduplicar por md5.
2. **Roteiro ES** neutro, sem as promessas e ameaças listadas acima; mantidos fé, Desatadora de Nudos, "oración de nueve palabras", urgência suave e CTA "Toca el botón de abajo".
3. **Voz:** clone de cada personagem no ElevenLabs.
4. **Legenda queimada:** remover com LaMa na GPU local (venv `producao\_trabalho\_vg`, modelo em `_lote\lama_base.py`).
5. **Lipsync HeyGen (`create_lipsync`)** — regras que funcionaram (detalhe em `producao\_trabalho\LICOES-LIPSYNC.md`):
   - **`mode speed`, nunca `precision`** (no precision a boca segue o português nas pausas);
   - o vídeo de entrada leva o **áudio PT original**; o ES vai separado (sem fala real na entrada o HeyGen recusa ou devolve a boca intacta);
   - recortar a entrada **só no rosto de quem fala** e colar de volta (elipse suave em boca e queixo);
   - trechos de **até ~12 s**; job parado > ~45 min → reenviar igual (volta em ~25 min);
   - plano B sem crédito: colar boca fechada do próprio trecho nas pausas (`ad01\lipsync2\fechar.py`);
   - medir saldo (`get_current_user`) antes e ~1 h depois do último job (a cobrança do speed atrasa).
6. **Aceite:** `checar_lipsync.py` com índice de pausa ≤ 0,6 no rosto de quem fala + revisor independente por lote.
7. **Cor:** ler e gravar com matriz bt601/tv fixa (`ad13\lipsync3\comum3.py`: `quadros()` + `ENC_VF` + `ENC_TAG`), senão escurece 2–3 níveis de luma por passada; ajustar trecho colado pelo anel de pele (`_lote\cor_trecho.py`) e comparar a luma média original × final.
- **Se a pessoa pedir mais:** versão Espanha = trocar só o texto/voz e refazer lipsync nos trechos; quando a oferta existir, remontar com selo e CTA específico sem novo lipsync.

## Relacionados
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [san-benito-es-vencedores.md](san-benito-es-vencedores.md), [san-benito-fr.md](san-benito-fr.md)
