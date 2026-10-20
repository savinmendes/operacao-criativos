# Briefing: estudo dos anúncios Vitaly → adaptação para Lymphoria (Chile)

**A marca Vitaly é da pessoa**, assim como a Lymphoria. Por isso pode trocar marca, clonar voz e fazer lipsync.
- **Não pergunte nada.**
- **Nunca leia `.env`.**
- **Não gaste:** nada de ElevenLabs, Flora ou HeyGen. Este é só o estudo.
- **Não abra players.**

## Material
- **Pasta:** `C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\`.
  - `VIDEOS\` e `IMAGENS\`, numerados na ordem de impressões.
  - `00-indice.csv`, com texto, título, CTA e landing de cada anúncio.
- **Oferta Lymphoria hoje:**
  - **Página:** https://chileverificada.com/products/lymphoria (leia com WebFetch: nome, frasco, oferta, claims e preço).
  - **Memória:** `C:\Users\PICHAU\.claude\projects\c--Users-PICHAU-Downloads-Produtividade-com-ia\memory\project_lymphoria-adaptacao-ads.md` e `project_drenagem-latam.md`.
  - **Vencedores no TikTok:** `C:\Users\PICHAU\Downloads\APROVADOS E VALIDADOS TIKTOK\`. Só para comparar o estilo; não precisa transcrever.
- **Ferramentas:**
  - Kit em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`. Leia o `CLAUDE.md`: seção "Troca de marca em AD existente" e armadilhas.
  - faster-whisper (es), RapidOCR e ffmpeg.
  - Whisper e OCR em sequência, nunca em paralelo. Rode com `PYTHONIOENCODING=utf-8`.

## Para cada vídeo da sua parte
1. **Transcrição** com tempos (whisper small ou medium, es) e **folha de contato** de 1 quadro a cada 1 s.
2. **Ficha:**
   - duração;
   - formato (UGC, médico, depoimento, animação, antes/depois, tela dividida…);
   - gancho dos 0–3 s, falado e na tela;
   - estrutura (problema → mecanismo → prova → oferta → CTA);
   - quem fala e se o rosto aparece falando;
   - voz em off ou ao vivo;
   - música.
3. **Mapa de troca Vitaly → Lymphoria**, com tempos:
   - marca falada ("Vitaly");
   - marca escrita na tela;
   - frasco e rótulo em cena (tempo, tamanho, se dá para ler);
   - landing e oferta citadas ("Compre 1 Reciba 2", "Lleva 2 Paga 1", Cyber Day, preço);
   - ingredientes ou claims que **não batem com a ficha da Lymphoria**;
   - qualquer dado que precisa mudar (país, moeda, datas).
4. **Itens sensíveis de compliance.** **Liste só, não mude:**
   - cura;
   - doença;
   - perda de peso em kg;
   - antes/depois de corpo;
   - médico;
   - urgência.

   A decisão de manter ou suavizar é da pessoa.
5. **Esforço e custo da troca:**
   - **sem custo:** corte, cobrir texto, `trocar_rotulo_faixa.py`;
   - **voz:** voz clonada da narradora do próprio vídeo, para a frase com a marca;
   - **lipsync:** se o rosto fala "Vitaly";
   - **frasco legível:** Kling ou Flora edit.

   Dê o custo estimado em US$ e o tempo de cada vídeo.
6. **Nota de potencial (1–5)** para a Lymphoria e o motivo.

## Saída
- `C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\_estudo\VNN.md`, uma ficha por vídeo, mais as folhas em `_estudo\folhas\`.
- No relatório final, uma tabela-resumo das fichas da sua parte.
