# EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE → UK (08/10/2026)

Saída: `UK\EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE - UK.mp4`. Tem 720x1280, 30 fps e 36,03 s, como o original. O vídeo foi copiado do original sem recodificar, então quadros e cor são idênticos; só o áudio mudou.

## Frase trocada (uma emenda, de 32,42 s até o fim)
- **Original (32,46–35,94 s):** "I'll link this below for you guys, but orange parts, they're still available, and I'm pretty sure they're under 20 dollars."
- **Nova (32,46–35,98 s):** "I'll link this below for you guys. They're still in stock, and I'm pretty sure they're under twenty pounds."
- **Emenda:** fica na pausa natural entre "I've tried a few" e "I'll", em 32,40–32,50 s (voz em −47 dB). Não há pausa antes de "but", então a emenda só podia ficar aí.
  - "I'll link this below for you guys" foi regravado com a voz clonada, com as mesmas palavras.
- **Fora do trecho:** áudio original intocado.
- **Dentro do trecho:** fundo do demucs (no_vocals) somado à voz nova (atempo 1,04 e +4,0 dB).
  - Volume: −21,1 LUFS, contra −21,2 LUFS do original no mesmo trecho.
- **Resto da transcrição:** não há outra menção a EUA, TikTok ou dólar.
- **Tela:** não tem elemento de TikTok, nem $, nem EUA. A legenda queimada "how i eat what i want without getting bloated af" fica.

## ElevenLabs
- **Voz:** "ENZIMAS UK EN 04 creator", id `WBrVsgRJbIDJhv90lRC8`. Clonada dos 36 s de voz isolada pelo demucs.
- **TTS:** 1 geração de **107 caracteres** (`tts1.mp3`), com estabilidade 0,4 e velocidade 1,1.

## HeyGen (mode speed, áudio original no vídeo de entrada, voz nova separada)
Os três jobs voltaram com a **boca intacta**: o `checar_lipsync` deu "mudou em 0% dos quadros", e a comparação visual confirma.

| Job | Entrada | id |
|---|---|---|
| A | quadro inteiro, q973–1080 (3,6 s) | a4b85eb18ec94b9ba5f39edcb66fff43 |
| B | q990–1061, reduzido a 0,6 com borda lisa | e0137780d6114bdbb9c8bc0490018e75 |
| C | q990–1061, quadro inteiro, legenda queimada apagada com LaMa (ela passa em cima da boca) | c29f004ad255402eb30d41780a8e97f4 |

Causa provável: o HeyGen não segue a boca. O frasco cobre a boca na maior parte do trecho, e há câmera na mão com borrão e cortes.

Decidi parar de gastar e fiquei **só com a troca de áudio**:
- **A boca só aparece em cerca de 1 s (q1019–1048, 33,97–34,93 s).**
  - Ali a fala nova coincide com a antiga: "they're still … and I'm pretty".
  - Só "in stock" e "available" diferem, em cerca de 0,4 s.
- **No resto do trecho, o frasco cobre a boca:** q976–1016 e q1050–1080.

**Créditos:** saldo de 8.797 antes e 8.797 logo depois, com outros agentes usando a mesma conta. A cobrança pode aparecer até cerca de 1 h depois: conferir de novo.

## Índice de lipsync
- Não se aplica: não há boca refeita e não há pausa na fala nova dentro do trecho visível.
- Na janela visível (33,97–34,93 s), a abertura da boca acompanha tanto a fala nova quanto a antiga:
  - correlação com a fala nova: 0,37;
  - correlação com a fala original: 0,35.

## Revisão (`revisar_ad.py --lipsync`, whisper medium en)
- **Transcrição final:** "…I'll link this below for you guys. They're still in stock, and I'm pretty sure they're under 20 pounds". Não sobra nada da frase antiga.
- **Termos proibidos:** nenhum.
- **Áudio:** decodifica OK, sem saltos de pts e sem silêncio.
- **"Problemas" apontados:**
  - "quadro solto 34,50/34,53": já está no vídeo original, porque o stream de vídeo foi copiado.
  - "boca não mudou": esperado, já que não houve lipsync (explicado acima).
  - As "setas vermelhas" detectadas são o rótulo rosa do frasco (falso positivo).

## Pendências
1. **Preço "under twenty pounds":** precisa de confirmação da pessoa.
2. **Saldo HeyGen:** reconferir cerca de 1 h depois. Os 3 jobs falharam e podem ter sido cobrados (estimativa ≤ 10 créditos).
3. **Opcional:** se quiser a boca refeita em "in stock" (cerca de 0,4 s visível), precisaria de outra ferramenta de lipsync que tolere oclusão; o HeyGen não pegou.
4. **"triple dipper" (0–3 s):** é um prato da rede americana Chili's. Não está na lista de trocas aprovadas, então ficou. Confirmar se incomoda no UK.
5. **Transcrição:** o whisper ouve "Physician's Choice" como "position series/Physicians sure". É a fala original, que não foi mexida.
