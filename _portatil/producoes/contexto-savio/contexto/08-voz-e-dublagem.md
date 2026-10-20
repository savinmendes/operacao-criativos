# Voz, narração, dublagem e áudio final

> Narração ElevenLabs (com alinhamento para a legenda), clonagem de voz, dublagem, troca de trecho de fala, trilha e loudness de entrega. Abra sempre que um criativo precisar de voz nova ou de mix final.

## Contexto de uso

**Serviço principal: ElevenLabs.**
- Pelo kit, via API direta: `tts_elevenlabs.py`, `clonar_voz.py`, `dublar.py`. A chave fica em `kit-edicao-criativos\.env` ou na variável `ELEVENLABS_API_KEY` (nunca ler nem imprimir).
- Também existe o MCP ElevenLabs. Pelo MCP: 1 geração por vez, sem pedir variações à toa.
- Modelo padrão: `eleven_multilingual_v2`.
- Custo de referência: ~US$0,165 por 1.000 caracteres. O script mostra antes de gerar; `--sim` pula a pergunta.
- A clonagem instantânea não cobra por uso no plano (só os caracteres gerados depois).

**Vozes conhecidas (ids não são segredo).**

| Nome / uso | voice_id | Fonte |
|---|---|---|
| VOZ DIVINA — San Benito (apelido `divina` no script) | `ArTYCGluU0cZhq1bF7Hp` | kit `CLAUDE.md`, `tts_elevenlabs.py` |
| Chilena — desmalezadora (apelido `chilena`) | `uHo8F3FY11rc2LxCwDSB` | idem |
| Jesus The Chosen ESPANHOL — usada também no FR do San Benito (13/10/2026) | `AkQxVSf1kENGmX9WjeDE` | memória SB FR, `tts_cta.py` |
| Narrador clonado Mayaverra/Lymphoria (AD 04) | `FNIhgYgEcJsdWbHRFiz6` | memória Lymphoria |
| HeyGen "JESU ESPANHOL" (voz do avatar no HeyGen, não ElevenLabs) | `485d82fb75ab42d397affd962ca338c4` | kit `CLAUDE.md` |

**Registro de clones.** `kit-edicao-criativos\VOZES-CLONADAS.md` tem a tabela completa, com lote, quem fala, voice_id, origem da amostra e observações:
- Oración ES (8 vozes);
- Podadora CL (2);
- Mopa H2O X5 (5);
- Enzimas UK (5);
- Vitaly → Lymphoria CL (4; inclui uma voz HeyGen `a16fc0d4eb2f4f2aa822a695f59266d4`, porque o clone ElevenLabs `SH5rTsQzlm6uv1YipARv` foi bloqueado por captcha).

Regra do arquivo: procurar antes de clonar e acrescentar uma linha depois de clonar.

**Regras de uso da voz (decisões da pessoa).**
- Criativos de marca própria: clonar o narrador original é liberado e é o padrão. Voz genérica quebra o padrão do criativo (lição do piloto Lymphoria).
- Criador de terceiros: voz de catálogo no idioma/sotaque do mercado, mesmo gênero e energia, **1 voz por criador**, mantida em todos os vídeos dele. Clone só no modo B2 (autorização do criador confirmada).
- Nunca apagar vozes. Reutilizar um clone existente da mesma voz quando a semelhança for alta.
- Lote Yara (09/10/2026): voz única por avatar obtida por clone + speech-to-speech (STS) do ElevenLabs, sem HeyGen. O STS mantém o tempo (±0,05 s), mas também mantém erro de pronúncia do take de origem.

**Loudness e mix (padrões).**
- Voz: −15 LUFS (`audio.py`/`montar_ad`: `loudnorm I=-15:TP=-1.5:LRA=11`).
- Trilha: o kit (`audio.py mix`) deixa a −29 LUFS, com corte em 2,5 kHz e ducking. **Padrão novo da pessoa (09/10/2026, Yara): −32 LUFS sob a fala, ducking de 11 dB.** A música a −24/−27 foi achada alta e obrigou a remixar 6 versões. Hoje o padrão do kit (−29) diverge da regra nova; ajustar à mão até o kit ser atualizado.
- Final: entre −16 e −13 LUFS, alvo ~−14 LUFS, **true peak ≤ −1 dBTP** (checklist do `revisar-criativo`). No FR do San Benito o mix final foi `loudnorm I=-14:TP=-1.5`. Original estourado se normaliza só no áudio, sem tocar no vídeo.
- Música viral (trend) liberada pela pessoa em versão instrumental via demucs + ducking; só citar no relatório.

## Lógica de uso

### 1. Narração nova (com alinhamento para a legenda)
```
python ferramentas/tts_elevenlabs.py "Esta máquina corta hasta árboles." -o narr.mp3 --voz chilena
python ferramentas/tts_elevenlabs.py --arquivo roteiro.txt -o audio/narr.mp3 --voz divina
python ferramentas/tts_elevenlabs.py --arquivo roteiro.txt -o audio/narr.mp3 --voz AkQxVSf1kENGmX9WjeDE --velocidade 0.95 --sim
```
- Gera `narr.mp3` + `narr.alinhamento.json` (tempo por caractere). Usar na legenda com `alinhamento:` na receita ou `legenda.py narr.mp3 --alinhamento narr.alinhamento.json -o leg.ass`.
- Parâmetros: `--voz` (apelido ou voice_id), `--modelo eleven_multilingual_v2`, `--estabilidade 0.5`, `--velocidade 1.0`, `--sim`.
- **Velocidade ≤1,1x.** Se não couber no tempo, enxugar o texto ou congelar um take.
- Roteiro no idioma do mercado, sem hora do dia e sem promessa de resultado.
- **Pronúncia:** nome de marca que o TTS erra → grafia fonética no texto do áudio (roteiro e legenda ficam com a grafia certa). Siglas e números por extenso, a mesma grafia em todos os vídeos do lote.

### 2. Regravar uma frase só, mantendo a entonação
Chamada `text-to-speech/<voice_id>/with-timestamps` com `previous_text` e `next_text` (as frases vizinhas) e `voice_settings` (`stability` 0.5, `similarity_boost` 0.75, `speed` 0.9 no caso do CTA FR). Depois emendar no meio do intervalo entre as palavras vizinhas, com fade de 10 ms, e recalcular o alinhamento. Modelo pronto: `SB-VENCEDORES_OP2-ASCENSAO_JESU-V07\_trabalho\v07\tts_cta.py` + `splice.py`.

### 3. Clonar voz
```
python ferramentas/clonar_voz.py video_ou_audio.mp4 --nome "AD04 narrador" --de 28 --ate 107
```
- Imprime o voice_id. Pega um trecho de fala contínua (ideal 1–2 min) e remove ruído/trilha no ElevenLabs.
- Melhor amostra: a voz isolada pelo demucs (`vocals.wav`). Com menos de 30 s de fala o clone sai pior: avisar a pessoa.
- Registrar em `VOZES-CLONADAS.md`.

### 4. Trocar um trecho de fala sem dessincronizar
```
python ferramentas/trocar_trecho_audio.py entrada.mp4 nova_fala.mp3 saida.mp4 --de 179.8 --ate 183.5
```
A fala nova é esticada ou comprimida para caber exatamente (limite 0,8x–1,25x), com cruzamento de 40 ms. Em localização: emenda em pausa natural, ±0,3 s, velocidade 0,9–1,1x, mesmo LUFS.

### 5. Corrigir uma palavra errada num take gerado (sem regerar)
Silenciar o trecho e colar a palavra em TTS com a mesma voz, preservando a duração. Modelo: `YARA-CL/producao/onda2/colar_palavra.py`. Conferir com whisper depois.

### 6. Dublagem automática (ElevenLabs Dubbing)
```
python ferramentas/dublar.py video.mp4 dub.mp3 --de es --para it [--ate 52.4]
```
Clona as vozes por personagem e mantém o fundo, sem marca d'água, usando créditos do plano. A tradução é **literal**: preço e marca estrangeiros continuam. Revisar e trocar trechos depois, ou preferir roteiro reescrito + TTS.

### 7. Música sem voz (demucs)
```
python -m demucs --two-stems=vocals arquivo.wav          # -d cuda com GPU livre
python ferramentas/gerar_variacao.py fundo "AD 20 - X.mp4" --ate 10.933 --saida fontes/20/bed.wav
```
Usar só `no_vocals.wav`. Se a voz original vazar, entregar sem trilha e anotar. Para alinhar o fundo a cenas que mudaram de duração, recortar o `no_vocals` cena a cena pelo fim de cada cena, com rampas curtas (modelo `_trabalho\v07\bed.py`).

### 8. Mix e loudness
```
python ferramentas/audio.py normalizar narr.mp3 -o narr_norm.wav            # voz a -15 LUFS
python ferramentas/audio.py mix narr.wav trilha.mp3 -o mix.wav             # voz -15 + trilha -29 com ducking
python ferramentas/audio.py trocar video.mp4 narr.mp3 -o out.mp4 [--trilha musica.mp3]
python ferramentas/audio.py pausas video.mp4 -o out.mp4 --min 0.35 --manter 0.12
```
Para a regra de −32 LUFS da trilha, usar mixador próprio (ex.: `YARA-CL/producao/musica/mixar_generico.py video leito saida [base_db]`) ou ajustar o volume da trilha antes do mix. Conferir no mix final I entre −16 e −13 e TP ≤ −1 dBTP. O kit não tem um script próprio para medir isso (o `revisar_ad.py` não mede loudness); o comando de medição usado pelo revisor independente não está registrado nas fontes — precisa de revisão manual.

### Armadilhas
- Integração ElevenLabs dentro do HeyGen com key ID errado (`VOICE_CONFIG_ERROR`): gerar o áudio pelo kit e mandar para o lipsync.
- Alinhamento do ElevenLabs adianta até 190 ms palavras depois de pausa (achado na revisão DeWalt, 10/10/2026): no `montar.py` modo roteiro do lote, o início passou a vir da energia da fala, limitado a ±80 ms do CTC. Medir com `medir_sinc.py` do lote.
- Seedance/STS erram palavras raras e "ñ" ("muñecas" → "mullegas"); o STS mantém o erro. Transcrever cada take antes de usar.
- Scripts que imprimem "≈" ou acentos quebram no cp1252 do Git Bash: `PYTHONIOENCODING=utf-8`.
- Clone de profissional de saúde para fala nova foi bloqueado pelo filtro (Vitaly V03/V11): não insistir.

### Checklist de saída
- [ ] Voz certa (clone do narrador / 1 voz por criador) e registrada.
- [ ] Velocidade ≤1,1x; pronúncia da marca conferida no whisper.
- [ ] Voz −15 LUFS, trilha −32 LUFS sob a fala, final ~−14 LUFS e TP ≤ −1 dBTP.
- [ ] Caracteres TTS e custo anotados no relatório.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
