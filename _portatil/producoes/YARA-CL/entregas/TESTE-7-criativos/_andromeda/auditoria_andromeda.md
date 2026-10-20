# Auditoria Andromeda: lote de teste Yara BF (COD Chile), 09/10/2026

Skill `andromeda`, modo 2 (auditar) + lacunas do modo 1. Fontes: `aberturas.json` / `aberturas_grade.jpg`
(nesta pasta), `producao/edicao/volume/cfg_H*.json`, `producao/roteiro_final.json`, `ESTRUTURA_CAMPANHA.txt`.

## Ficha por criativo

| Anúncio | Abertura (0–2 s) | Pessoa / cenário | Fala | Mensagem | Família |
|---|---|---|---|---|---|
| CJ01 H1 | consultora no balcão BF + "PAGA 2 LLEVA 3" | consultora, balcão | T1 (liquidação, paga 2 leva 3) | oferta BF | F1 |
| CJ06 AD-A | igual ao H1 (similaridade 0,90) | consultora, balcão | T1 + T3/T4 | oferta BF | F1 |
| CJ07 AD-C | igual ao H1 (0,92) e ao AD-A (0,97) | consultora, balcão | T1 + notas + CTA | oferta BF | F1 |
| CJ02 H2 | consultora em zoom "PAGA 2 / LLEVA 3" | consultora, balcão (zoom) | T10 + T1 | oferta BF | F1b (só enquadramento) |
| CJ03 H3 | close cheirando o frasco + "¿Ya probaste…?" | consultora, close | T4 + T1 | curiosidade → oferta BF | F2 |
| CJ04 H4 | mãos abrindo caixa, "LIQUIDACIÓN" | só produto (b-roll) | T1 em off | oferta BF | F3 |
| CJ05 H5 | 3 frascos com nome, um por vez | só produto (b-roll) | T1 em off | oferta BF | F3b |

## Veredito: subir com ressalvas

- **Em abertura são ~4 famílias** (F1, F2, F3 e as variações F1b/F3b), **mas a mensagem é uma só**. Os 7
  anúncios usam a mesma fala de gancho (T1), a mesma voz, a mesma pessoa e o mesmo ângulo (oferta BF). Para a
  regra "≥ 4 famílias, cada uma diferente em ≥ 2 dimensões", só H3, H4 e H5 diferem do H1 em 2 dimensões
  (visual e formato). Ninguém difere em **mensagem**.
- **CJ01, CJ06 e CJ07 tendem a ser tratados como o mesmo criativo** (aberturas de 0,90 a 0,97). No teste ABO
  isso desperdiça 3 conjuntos lendo praticamente a mesma coisa (US$ 42/dia dos US$ 100).
- **Um persona só, um nível de consciência só** (pronto para comprar / consciente do produto) e uma etapa do
  funil (fundo). Pela leitura de funil (`referencia.md` §5b), falta topo: nada traz quem ainda não conhece
  perfume árabe.

## Parecidos demais: o que refazer

1. **Ficar com 1 de CJ01/CJ06/CJ07.** O AD-C (mais completo) ou o H1 (mais curto). Os outros 2 conjuntos
   recebem conceitos novos (abaixo).
2. Se quiser manter o AD-A, trocar a abertura dele por uma cena que só ele tem (ex.: o close do T4 ou a loja
   movimentada das 3 cenas novas).

## Lacunas da matriz (conceitos a criar)

Personas e ângulos são **hipóteses** (sem pesquisa de comentários/avaliações ainda).

| ID | Persona (micro-momento) | Ângulo | Consciência / etapa | Abertura visual | Hipótese |
|---|---|---|---|---|---|
| N1 | Quem procura presente de Natal/amigo secreto | ocasião (presente) | consciente do produto / meio | caixa sendo embrulhada ou entregue | Na ocasião, a decisão é sobre o outro; o kit de 3 resolve "presente + um para mim" |
| N2 | Quem nunca usou perfume árabe e viu a tendência | descoberta / identidade | consciente da solução / topo | reação ao cheirar pela 1ª vez (outra pessoa, mais jovem) | Quem não conhece precisa de curiosidade, não de oferta |
| N3 | Quem tem medo de comprar online | remoção de risco (paga ao receber) | pronto para comprar / fundo | campainha, entrega na porta, pagamento na mão | No COD, "paga ao receber" é ângulo próprio, não rodapé |
| N4 | Quem quer perfume que dure o dia | sensorial / durabilidade | consciente do problema / meio | manhã × noite, mesma pessoa | Fixação é a dúvida nº 1 em perfume barato (validar nos comentários) |
| N5 | Quem gosta de variar (dia, cita, noite) | rotina (3 momentos) | consciente do produto / meio | 3 cenas: escritório, encontro, festa | Já existe no texto do anúncio; vira conceito visual com elenco próprio |

- **Elenco:** hoje só a consultora. Para abrir públicos, pelo menos 1 mulher mais jovem (N2) e 1 pessoa
  comprando presente (N1), com sotaque chileno.
- **Formato:** só vídeo 9:16. Falta estático de oferta (fundo de funil barato) e carrossel dos 3 frascos.
- **Compliance:** sem risco de saúde. Atenção a "muy por debajo del mercado" e "quedan pocas unidades":
  precisam ser verdadeiros (a escassez foi aprovada pela pessoa em 09/10). Comparar com perfume de grife pelo
  nome é risco de marca de terceiros: decisão da pessoa.

## Estrutura (observações)

- 7 conjuntos ABO a US$ 14/dia: pela referência, a verba por conjunto de teste deveria ser ≥ 3× o CPA-alvo,
  que ainda está **pendente**. Sem ele, a regra "2× CPA sem venda" não tem número.
- Alternativa com a mesma verba: 4–5 conjuntos (1 por conceito/família), 2–3 anúncios cada, em vez de 7 com
  1 anúncio.
- Decidir por pedido **entregue/pago** por anúncio (UTM com o nome do anúncio já previsto), não pelo CPA do
  gerenciador.
