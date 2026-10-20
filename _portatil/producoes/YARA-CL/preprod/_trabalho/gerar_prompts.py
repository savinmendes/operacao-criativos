# -*- coding: utf-8 -*-
import json
rot = json.load(open(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod\roteiro.json", encoding="utf-8"))
falas = {g["id"]: g["fala"] for g in rot["ganchos"]}

CENA = ("Foto vertical 9:16, fotorrealista, luz de estúdio suave e quente. Interior de uma perfumaria de luxo: "
        "prateleiras iluminadas com frascos genéricos desfocados ao fundo, bancada de mármore branco em primeiro plano. "
        "Loja DECORADA PARA BLACK FRIDAY: ao fundo, atrás da mulher, um letreiro elegante em letras douradas sobre painel preto "
        "escrito exatamente \"BLACK FRIDAY\" (só esse texto, grafia correta), balões/laços pretos e dourados discretos, "
        "etiquetas pretas com detalhes dourados nas prateleiras SEM texto legível. "
        "NÃO inclua nenhum outro letreiro, logotipo ou marca (nada de ESSENZALUX nem marcas de perfume no cenário). ")
PROD = ("Use a imagem de referência produto_1.jpg como referência EXATA dos frascos: Yara (rosa-claro com laço/anel prateado), "
        "Yara Moi (branco com laço/anel dourado) e Yara Elixir (rosa-salmão com laço/anel rosé/cobre), mesmo formato cilíndrico, "
        "tampa, medalhão central e escrita árabe; mantenha proporção e cores fiéis, sem inventar texto novo nos frascos. "
        "Os 3 frascos (3 PERFUMES) aparecem na bancada de mármore em frente à mulher, em pé, com realismo, sombras e reflexos corretos. ")
FIM = ("Mulher olhando para a câmera, expressão confiante e simpática, boca fechada em leve sorriso, enquadramento da cintura para cima, "
       "centralizada, espaço livre no topo da imagem. Sem texto além de \"BLACK FRIDAY\" no letreiro. 9:16.")

personas = {
 "H1": ("mulher latina de ~30 anos, cabelo preto longo e liso, maquiagem marcante, blazer preto estruturado com botões dourados e brincos dourados",
        "segura na mão direita, na altura do ombro, o frasco Yara Elixir (rosa-salmão, anel rosé) voltado para a câmera; na bancada ficam Yara e Yara Moi + um segundo Yara Elixir NÃO — na bancada ficam somente os outros dois para totalizar os 3 do kit"),
 "H2": ("mulher europeia de ~35 anos, loira, cabelo preso em coque baixo, blazer cor champanhe sobre blusa de seda marfim, colar fino dourado",
        "segura na mão direita, perto do rosto, o frasco Yara (rosa-claro, anel prateado) como quem acabou de borrifar; na bancada ficam Yara Moi e Yara Elixir"),
 "H3": ("mulher latina de ~40 anos, cabelo castanho médio ondulado, vestido de cetim vinho/bordô, pulseira dourada",
        "segura com as duas mãos, à frente do peito, o frasco Yara Moi (branco, anel dourado) como quem apresenta um presente; na bancada ficam Yara e Yara Elixir e uma caixa de presente preta com laço dourado SEM texto"),
 "H4": ("mulher latina de ~28 anos, pele morena, cabelo cacheado volumoso preso meio solto, blusa de cetim branca, argolas douradas",
        "segura na mão esquerda, na altura do ombro, o frasco Yara (rosa-claro, anel prateado); na bancada ficam Yara Moi e Yara Elixir"),
}
# H1: deixar a regra de 3 frascos clara (sem duplicar)
personas["H1"] = (personas["H1"][0], "segura na mão direita, na altura do ombro, o frasco Yara Elixir (rosa-salmão, anel rosé) voltado para a câmera; na bancada ficam Yara e Yara Moi (total de 3 frascos na cena, nenhum repetido)")

SEED = ("a mulher fala olhando para camera e com confiança em ESPANHOL: \"{fala}\". "
        "SEM CORTES DE CAMERA E NEM MUDANÇA DE ANGULO E NEM ZOOM, NEM EFEITOS DE AUDIO OU VIDEO.")

ganchos = []
for gid, (pessoa, mao) in personas.items():
    ganchos.append({
      "gancho": gid,
      "fala": falas[gid],
      "imagem_base_gpt_image_2": {
        "modelo": "GPT Image 2 (Flora i2i-gpt-image-2), 9:16, qualidade high",
        "referencias": ["_ref/produto_1.jpg (frascos — obrigatória)", "_ref/flora_n101.png (opcional: composição/enquadramento da consultora na bancada)"],
        "prompt": f"Consultora de perfumaria elegante: {pessoa}. Ela {mao}. " + CENA + PROD + FIM,
        "nome_sugerido": f"YARA-BF-{gid}_CONSULTORA",
      },
      "video_seedance_2": {
        "modelo": "Seedance 2.0 (Flora), image-to-video, 8 s, 9:16, com áudio/fala",
        "entrada": f"imagem aprovada YARA-BF-{gid}_CONSULTORA",
        "prompt": SEED.format(fala=falas[gid]),
        "conferir": ["fala em espanhol completa dentro de 8 s (sem cortar a última palavra)",
                     "frascos sem deformar / sem texto inventado", "sem corte/zoom", "sotaque latino neutro; se vier espanhol da Espanha, refazer acrescentando 'sotaque latino-americano (chileno)'"],
      },
    })

alternativa = {
  "descricao": "Fluxo que já funciona no canvas do cliente (2 passos sobre uma cena-base existente, ex.: flora_n101.png): troca dos perfumes + troca de persona. Depois, pedir a troca do letreiro.",
  "passo_1_troca_perfumes": "altere os perfumes da mesa e da mão da mulher pelos perfumes da referencia. coloque os perfumes com realismo. 3 PERFUMES",
  "passo_2_troca_persona": "troque caracteristica fisicas da mulher e roupas/cores de roupas. matenha todo o cenario e obeto identicos.",
  "passo_3_letreiro_bf": "troque o letreiro do fundo por um painel preto com o texto \"BLACK FRIDAY\" em letras douradas, sem logotipo e sem nenhuma outra palavra. acrescente decoração discreta preta e dourada de Black Friday nas prateleiras, sem texto. mantenha a mulher, os perfumes, a bancada e o enquadramento idênticos.",
}

packshot = {
  "uso": "plano B do sticker_kit.png (se o recorte local não servir) e base do cartão final",
  "modelo": "GPT Image 2 (Flora i2i), 1:1 ou 3:2, qualidade high",
  "referencias": ["_ref/produto_1.jpg"],
  "prompt": ("Packshot de estúdio sobre FUNDO BRANCO PURO (#FFFFFF), sem sombra colorida, sem chão de mármore, sem texto, sem ícones, sem sinais de '+'. "
             "Somente os 3 frascos da referência produto_1.jpg, em pé, lado a lado, de frente, na ordem da esquerda para a direita: "
             "Yara (rosa-claro, anel prateado) | Yara Moi (branco, anel dourado) | Yara Elixir (rosa-salmão, anel rosé). "
             "Réplica EXATA de formato, cores, tampas, medalhão e escrita dos frascos da referência; mesma altura; espaçamento igual; "
             "frascos inteiros (topo e base visíveis), iluminação suave de estúdio, sombra de contato mínima cinza neutra."),
  "pos": "recortar com rembg (u2net) — venv em scratchpad ou `pip install rembg[cpu]` — e trocar sticker_kit.png",
}

orcamento = {
  "observacao": "NADA foi gerado. Valores do CLAUDE.md do kit; Seedance 2.0 não tem preço registrado no kit — conferir run_cost no Flora antes de rodar.",
  "gpt_image_2": "5 imagens (4 consultoras + 1 packshot) × ~US$0,073 ≈ US$0,37 (+ refações)",
  "seedance_2_8s": "4 vídeos × preço do Seedance 2.0 8 s (a orçar no Flora)",
  "qa_gemini": "4 × ~US$0,025 ≈ US$0,10",
}

out = {"ganchos": ganchos, "alternativa_fluxo_cliente": alternativa, "packshot_fundo_branco": packshot, "orcamento_estimado": orcamento}
json.dump(out, open(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod\prompts_flora.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(ganchos))
