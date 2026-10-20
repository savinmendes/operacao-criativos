# Relatório: conceitos C1 e C3 (lote enxuto Lymphoria COD Chile, 10/10/2026)

## Entregas (720x1280, 9:16)
| Arquivo | Duração | Abertura (quadro 1) | Voz |
|---|---|---|---|
| LYM-CL_C1_trabajadora-de-pie_avatar-ugc_a.mp4 | 42,5 s | Avatar HeyGen cajera 38 + manchete "12 HORAS DE PIE" | ElevenLabs "Catalina - Chilean Spanish" (6Gr4AVmTax1pMJO0lHRK) |
| LYM-CL_C1_trabajadora-de-pie_pov-voz-off_b.mp4 | 43,2 s | Pernas de garçonete andando entre mesas (POV sem rosto) + manchete "¿Llegas con los tobillos hinchados?" | ElevenLabs "Camila" chilena (oJIuRMopN0sojGjwD6rQ), vel. 1,05 |
| LYM-CL_C3_jubilada-60_avatar-ugc_a.mp4 | 43,2 s | Avatar HeyGen abuela 64 + manchete "¡Volví a usar mi anillo!" | ElevenLabs "Angela - Warm, Calm" chilena (prblQcKOdF08ozhxP2mk) |
| LYM-CL_C3_jubilada-60_testimonio-off_b.mp4 | 44,1 s | Mãos de 60+ tentando passar anel que não entra + manchete "¿Tus anillos ya no entran?" | ElevenLabs "Luisa - Friendly, Calm" latina madura (efcRUax7uSa9kpBwtDPe), atempo 1,04 |

Fim (padrão ESTUDO-CTA v2): takes Lymphoria em movimento (3 por vídeo, combinação diferente em cada um), legenda normal, selo pequeno amarelo "PAGO CONTRA ENTREGA" a partir de "pagas", setas vermelhas a partir de "Toca" até o último quadro. Sem preço, sem card. Fala final: "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Toca el botón de abajo y pide el tuyo."
Música de fundo a -32 LUFS sob a voz (-16): V10, V12 e V26 (demucs, sem voz) e AD 24 do lote Drenagem. Legenda pelo roteiro (alinhamento do ElevenLabs). Troca de plano a cada 1,1–4 s.

## Material usado
- Takes Lymphoria (LHYMPORIA AD 01-20 e ugc\prod), conferidos a 5 q/s contra texto queimado. O take ad22/flora/t2 tem legenda "No pu… uar el" queimada e foi tirado.
- Banco Vitaly V12 (pernas inchadas, pernas no sofá, pés de meia), recortado entre o título e a legenda queimados.
- 11 B-rolls HeyGen Video 1 (5 s, 768p), créditos já pagos: pés com sapato de trabalho, garçonete, sofá, massagem no tornozelo, pés no caixa, anel que não entra, anel que entra, pantufas 60+, sapatos 60+, abuela no parque, abuela na janela. Nenhum mostra produto.
- Avatares por prompt: "LYM-CL C1 Cajera 38 v2" (198fb0ed70b760a408a8ce3d305fc4d9) e "LYM-CL C3 Abuela 64" (7e74d5b3a79a64af6f1adc39f2ff161d). A v1 da cajera saiu com a interface da câmera do celular na imagem e foi descartada.

## Custo real
- ElevenLabs: 4.239 caracteres, cerca de US$ 0,70. Inclui 3 narrações descartadas (US$ 0,31) porque as primeiras passavam de 45 s.
- HeyGen: saldo de 8.793 para 8.690, ou seja, 103 créditos e US$ 0. É o teto, porque outros agentes do lote usaram a mesma conta ao mesmo tempo. Da minha parte foram 4 looks, 11 clipes Video 1 e 4 renders de avatar de ~42 s (2 deles foram testes de boca).
- Flora/Kling/Seedance: nada.

## Revisão (revisar_ad.py, proibidos Vitaly/kilos/kg/cura/cáncer/Mayaverra)
- Os 4 vídeos têm decodificação OK, nenhum salto de pts, nenhum silêncio > 0,7 s, nenhum quadro solto, setas no último quadro e nenhum termo proibido. O idioma detectado é es (0,98–0,99).
- O whisper escreve "linforia"/"estilinja" para Lymphoria/stillingia. A pronúncia é a da voz chilena, sem erro de palavra.
- **Lipsync (checar_lipsync.py) REPROVA os 2 avatares** (índice 1,25 C1-A / 1,57 C3-A):
  - **Causa:** o Avatar IV sorri mostrando os dentes nas pausas, e o teste conta isso como boca aberta. Refazer com expressividade baixa e com foto de boca fechada deu o mesmo índice (1,24 / 1,26).
  - **O teste não serve para avatar inteiro:** a UGC 01 do lote Drenagem, já aprovada (heygen_01.mp4), também dá 1,01.
  - **Conferência a olho**, com recorte da boca a 10 q/s: a boca fecha antes de cada frase e abre junto com a fala, sem atraso visível. **Precisa de revisão manual da pessoa no celular.**
  - **Se reprovar:** usar Avatar V ou a v3 da cajera de boca fechada (`_trabalho\prod\_enxuto_c1c3\c1a\av3.mp4`, já renderizada). Basta trocar `av.mp4` no plano e remontar.

## Reproduzir
`ADLIB-VITALY-CL\_trabalho\prod\_enxuto_c1c3\`:
1. `mkplans.py` gera os planos.
2. `montar_corpo.py cX/plano.json` monta o corpo.
3. `mkreceita.py cX` gera a receita.
4. `montar_ad.py cX/receita.json` monta o AD. As revisões ficam em `rev\`.
