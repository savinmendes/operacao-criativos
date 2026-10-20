# San Benito FR: vencedores OP2 ASCENSAO e JESU V07 em francês

> Versão em francês de dois vencedores de San Benito (espanhol), refazendo só fala, boca e legenda. Abra ao traduzir mais vencedores SB ou ao refazer lipsync com nitidez.

## Contexto de uso
- **Frente:** Infoproduto — Oração de San Benito, mercado francófono.
- **Início e entrega:** 13/10/2026. A pessoa apontou **OP2 ASCENSAO** (~US$ 2,1 mil de gasto na vida, ativo em ES/US/EURO) e **JESU V07** como vencedores em espanhol.
- **Pasta:** `Downloads\SB-VENCEDORES_OP2-ASCENSAO_JESU-V07\` (cópias dos originais `SB-OP2-ASCENSAO.mp4` e `SB-JESU-V07.mp4`); saída em `FR\`; trabalho em `_trabalho\op2`, `_trabalho\v07` e `_trabalho\revisor`.
- **Decisões da pessoa:**
  - francês geral (mesma publicação para todos os países francófonos), tratamento "tu";
  - mesma página de destino do espanhol;
  - mesma voz ElevenLabs "Jesus The Chosen ESPANHOL" (`AkQxVSf1kENGmX9WjeDE`);
  - San Benito → "saint Benoît";
  - **caminho 1:** refazer só fala, boca e legenda; visual igual. Material limpo (conferido em 13/10/2026): b-rolls em `Downloads\SAN BENITO B-ROLS\` (115 arquivos, `SB-BRV-NN <cena> KLING25.mp4`), corpo limpo `Downloads\1-VIDEOS\SB-CORPO_CTA_COMPLETO_JESU.mp4` (a pasta `1-VIDEOS` é criada pelo arrumador diário do Downloads, ver `../16-ferramentas-e-servicos.md`), ganchos em `Downloads\HOOKS SAO BENITO\` (ex.: `SB-HOOK-OP2_AV30_ASCENSAO.mp4`);
  - "máximo de agentes": 1 agente por AD + revisor.
- **Entregue (v2, após revisor independente):**
  - `FR\SB-FR-OP2-ASCENSAO.mp4` — 1080x1920, 27,4 s (original ES 30,27 s);
  - `FR\SB-FR-JESU-V07.mp4` — 1080x1920, 31,9 s;
  - `.txt` de cada um com roteiro ES, roteiro FR e texto do anúncio (ex.: título "La prière perdue de saint Benoît"); v1 guardadas como `_v1` em `FR\_versoes-antigas\`.
- **CTA:** "Appuie sur « En savoir plus »" (não "Touche"), botão do Meta LEARN_MORE.
- **Regra de compliance do texto do anúncio (FR, 13/10/2026):** o texto não promete resultado, não fala de hora do dia e não afirma condição pessoal de quem vê (ex.: "Tu peux être entouré de monde et pourtant te sentir complètement seul", em vez de afirmar que quem vê está só); a fala do vídeo mantém o mesmo teor do ES aprovado, sem suavizar nem intensificar.
- **Custo:** HeyGen ~346 créditos no total (saldo 7.982 → 7.636); ElevenLabs < US$ 0,40.
- **Pendências:** nenhuma registrada além de subir e ler resultado — precisa de revisão manual se houver.

## Lógica de uso
1. Transcrever o ES e escrever o roteiro FR frase a frase, mantendo a mesma ordem de cenas (o `.txt` de entrega mostra o pareamento cena × frase).
2. Gerar a voz FR com a mesma voz do ES; esticar pausas quando preciso (`op2\esticar_pausas.py`).
3. Lipsync do Jesus no HeyGen (regras do lote Oración: `mode speed`, PT/ES original na entrada, recorte no rosto, trechos ≤ 12 s).
4. **O lipsync deixa o rosto mole:** colar só boca e queixo do HeyGen sobre o take original com `_trabalho\v07\colar_boca.py in.mp4 out.mp4 dest.mp4 [--fechar ini:fim ...]` (elipse suave, cor pelo anel de pele, nitidez casada; leitura bt601 fixa). Recupera a nitidez.
5. **Os AD SB-JESU foram feitos fora do kit** (sem receita JSON): estrutura = gancho + `SB-CORPO_CTA_COMPLETO_JESU` com b-rolls por cima; legenda queimada em caixa alta branco + amarelo. O kit não tem esse estilo de legenda: usar os scripts próprios em `_trabalho` (`gerar_legenda_v2.py`, `compor_v2.py`, `achar_broll.py`, `alinhar_broll.py`, `cortes.py`).
6. Termos proibidos em `proibidos_fr.txt` (UTF-8) + `revisar_ad.py` + revisor independente (whisper fr + folha + boca).
- **Se a pessoa pedir mais:** repetir o mesmo caminho para os outros vencedores de [san-benito-es-vencedores.md](san-benito-es-vencedores.md) (ADS 6, ADS 20, ADS 12.x), 1 agente por AD + revisor.

## Relacionados
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [san-benito-es-vencedores.md](san-benito-es-vencedores.md), [oracion-es-latam.md](oracion-es-latam.md)
