# Música trend Chile — AD-C Yara Kit 3 (Black Friday, COD Chile)

Data da pesquisa: 09/10/2026. Música comercial: decisão e risco de direitos assumidos pela dona do anúncio.

## Fontes consultadas
- Spotify Chile diário e semanal (kworb.net/spotify/country/cl_daily.html e cl_weekly.html), parada de 08/10/2026.
- Shazam Chile: Top 200, Viral ("as músicas que mais crescem esta semana, descobertas em telas e redes") e Discovery (shazam.com/charts/.../chile), consultado em 09/10/2026.
- TikTok discover "canciones-en-tendencia-de-chile" (renderizado com Chrome).
- TikTok Creative Center (música por região CL): o ranking de músicas agora exige login; sem acesso anônimo. Não foi usado.

## Candidatas (evidência)
| # | Música | Evidência |
|---|---|---|
| 1 | KAROL G, Judeline, rusowsky — BbY WOW | #1 Spotify CL diário e semanal (9 semanas); #1 Shazam Top CL; trend de dança do TikTok (LOS MENOR3S, Remezcla) |
| 2 | HUGEL & SOLTO (FR) — Jamaican (Bam Bam) | #6 Shazam Viral CL, #9 Shazam Top CL; trend de dança "bam bam" no TikTok |
| 3 | Aitana — SUPERESTRELLA | #17 Spotify CL diário / #18 semanal (subindo +2); #40 Shazam CL; som viral do TikTok desde o Mundial 2026 (+500 mi views, que.es 07/2026) |
| 4 | HUGEL, Imael Angel, Ultra Naté — Movin' To The Sun | #7 Shazam Top CL |
| 5 | DJ.ILHAM — DIGIDI DIGIDI | #1 Shazam Discovery CL; trend de dança no TikTok (tom infantil/meme) |
| 6 | ROA ft. Anuel AA — VAMO A VEL | #2 Spotify CL (subindo) |
| 7 | Rafaga — Lejos de Ti | #1 Shazam Viral CL (cumbia) |
| 8 | LATIN MAFIA & Fred again.. — Te Estoy Correteando | #29 Spotify CL, #8 Shazam CL |
| 9 | Lucky Brown, Jere Klein & Nes — Bella | destaque na página TikTok "canciones en tendencia de Chile" |

Escolhidas (perfume feminino + BF: animada/sensual, voz feminina ou dança de trend): 1, 2 e 3.

## Áudio baixado (yt-dlp -f bestaudio, opus ~135 kbps → wav), conferido por transcrição (transc_songs.txt)
| Arquivo | Fonte | Trecho usado (s da música) | Ponto forte em 1,5 s do AD |
|---|---|---|---|
| bbywow.wav | https://www.youtube.com/watch?v=fRIhCiUVaKs (canal oficial KAROL G, Visualizer) | 30,55 → 78,9 (refrão "Suena tu canción" + "Baby wow") | entrada do beat em 32,05 s |
| bambam.wav | https://www.youtube.com/watch?v=hghqd1eBTYQ (MoBlack Records, Original Mix) | 60,55 → 108,9 (drop principal + groove) | drop em 62,05 s |
| superestrella.wav | https://www.youtube.com/watch?v=vz_vU53JvvI (canal oficial Aitana) | 54,60 → 102,9 (refrão "Él me dice que quiere divertirse" ×2) | entrada do refrão em 56,10 s |

## Mixagem (mixar.py)
- demucs htdemucs --two-stems=vocals (CPU) → só `no_vocals.wav` (instrumental) sob a voz: `sep/htdemucs/<nome>/`.
- O vocal original da música NÃO entrou: a narração do AD é contínua de 0 s até 48 s (inclusive no título e no cartão final), então ele brigaria com a fala.
- Música sob a voz ≈ -24 LUFS (após ducking), sidechaincompress pela voz (thr 0.03, ratio 5, att 15 ms, rel 350 ms), +3,5 dB no título (0–1,5 s) e no cartão final (últimos 1,8 s), fade-out 0,8 s, ganho final para -14,5 LUFS + limitador (pico ≤ -1,3 dBTP), vídeo -c:v copy.
- Parâmetros de cada mix: mix_<nome>.json.

## Revisão (09/10/2026)
- revisar_ad.py (es, termos proibidos de entregas/_proibidos.txt): OK nas 3 versões (decodificação, pts sem saltos, sem silêncio, 21 cortes, setas no fim). Relatórios em revisao_<nome>/.
- Whisper small es: mesmo texto da versão sem música, frase a frase (os erros de nome de marca, como "Yara Moi" e "Elixir", já aparecem iguais na versão original).
- Duração: vídeo 48,133 s = áudio decodificado 48,133 s nas 3 versões. Loudness final -14,5/-14,6/-14,5 LUFS, pico -1,5/-1,8/-1,3 dBTP.
