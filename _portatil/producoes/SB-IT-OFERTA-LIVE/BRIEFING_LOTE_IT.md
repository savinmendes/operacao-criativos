# Lote SB IT — oferta "preghiera in diretta" (aprovado com "confirmo" em 16/10/2026)
Mercado: Itália (EUR). Italiano natural e neutro, tom espiritual. "San Benito" → **"San Benedetto"**.
Destino: a ORAÇÃO AO VIVO em italiano. CTA final padrão: **"Tocca «Scopri di più» qui sotto e unisciti alla preghiera in diretta"** (botão do Meta LEARN_MORE = "Scopri di più"). O vídeo nunca mostra produto nem preço.
Compliance: mesmo teor do original/EN (promessas e urgência), sem suavizar (decisão da pessoa).

## Base = o lote EN que já está pronto
Cada vídeo IT parte da versão EN do mesmo número: `C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\<pasta EN>\` (o `.mp4` EN, o `_roteiro-en.txt`, o `_texto-anuncio.txt` e o `_trabalho\` com bases limpas sem legenda, entradas do HeyGen com o áudio ORIGINAL, demucs/música, scripts de legenda/mix/composição). REUTILIZE tudo o que puder (base limpa, cortes, trilha, setas, estilo de legenda, timeline). NÃO escreva nada nas pastas EN: copie o que precisar para o seu `_trabalho` IT.
Leia também o `BRIEFING_LOTE_EN.md` (mesma pasta EN) — o método e as armadilhas são os mesmos; só muda o idioma.

## Método B (validado em FR e EN)
1. Roteiro IT a partir do roteiro ES/EN: tradução natural (não literal), duração parecida com o EN, CTA da live em italiano. Texto na tela (títulos/cartões) reescrito em italiano no mesmo estilo.
2. Voz ElevenLabs (chave em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`, não imprima), modelo multilíngue (eleven_multilingual_v2 ou v3) com `language_code` "it" se o modelo aceitar. Use a MESMA voz do EN daquele vídeo (veja o roteiro EN: "Jesus The Chosen" AkQxVSf1kENGmX9WjeDE ou "Brian" nPczCjzI2devNBz1zQrb). Conta no LIMITE de vozes: não crie, não clone, não apague voz. Confira pelo whisper IT que a pronúncia saiu italiana (sem sotaque inglês forte); se sair ruim, teste a outra configuração do modelo antes de trocar de voz.
3. Lipsync HeyGen mode **speed**: vídeo de entrada com o áudio ORIGINAL (use o `heygen_in` do EN), áudio IT separado, trechos ≤ ~12 s, recorte só no rosto de quem fala. Aceite: `checar_lipsync.py` pausa ≤ 0,6. Job parado > 45 min: reenviar igual. Cor bt601 fixa, `-reinit_filter 0`, conferir salto de pts no áudio.
4. Legenda IT palavra a palavra no estilo do EN (caixa alta, palavra falada destacada, palavras-chave em vermelho), setas amarelas nos CTAs, música do original (demucs) ~-32 LUFS sob a fala, selo/rodapé traduzido se houver.
5. 720p no mínimo (mesma resolução do EN).

## QA
`revisar_ad.py` do kit (rode de `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`, PYTHONIOENCODING=utf-8) com whisper **it**. Proibidos (arquivo .txt UTF-8): inglês residual ("Tap", "Learn More", "live prayer", "Saint Benedict", "join"), espanhol/francês residual ("San Benito", "en vivo", "oración", "Toca"), preço, "R$", "$", "€". Confira folha de contato, quadro solto, silêncio no fim, boca nas pausas. Depois 1 subagente revisor independente rápido; corrija o que ele achar. NÃO abra os vídeos.

## Saída
`C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\<NN>_<NOME>\SB-IT-<NOME>.mp4` + `SB-IT-<NOME>_roteiro-it.txt` (roteiro EN × IT + decisões) + `SB-IT-<NOME>_texto-anuncio.txt` (Titolo ≤40 / Testo principale / Versione breve ≤125 / Pulsante: LEARN_MORE "Scopri di più"; adaptado do `_texto-anuncio.txt` EN, sem preço, chamando para a preghiera in diretta) + `SB-IT-<NOME>_frames.jpg`.
Trabalho só em `<NN>_<NOME>\_trabalho\`. Ao terminar, crie `<NN>_<NOME>\PRONTO.txt`. Apague intermediários pesados (frames extraídos, wav temporários) ao final, mantendo scripts e o mp4.
Painel: `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa sbit-<nome> "<título>" --texto "..."` (e img/custo/fim).
Custos: ElevenLabs centavos; HeyGen speed com créditos do plano (não meça saldo, o coordenador mede). Nada pago fora disso; Flora sem saldo.
Relatório final (curto): arquivo, duração, voz, nº de jobs HeyGen, o que ficou imperfeito com tempos.
