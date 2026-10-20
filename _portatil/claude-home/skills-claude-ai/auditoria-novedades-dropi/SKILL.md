---
name: "auditoria-novedades-dropi"
description: "Audita as novedades da Dropi Chile (Tienda Tuya): agrupa por motivo, confere as fotos de evidência do courier (EXIF, hora, conteúdo) atrás de tentativas falsas, cruza com a Talkyria para achar soluções já combinadas com o cliente e não aplicadas, monta o plano e aplica as soluções na Dropi."
---

# Auditoria de novedades Dropi (Chile)

Responder sempre em português do Brasil, direto, com números. O usuário (Savin) não é técnico.

## 0. Fonte da verdade: a tela de Novedades da Dropi (sempre primeiro)

A lista real do que está pendente é a tela `https://app.dropi.cl/dashboard/novelties`, não o banco. O banco do Chegou Operações fica atrasado e tem pedidos que já saíram da tela.

1. Abrir a tela de Novedades. Ela abre mostrando só **10 linhas por página**. Mudar o seletor "Mostrar" para 1000 via `javascript_tool` (set do `select` + evento `change`, depois esperar uns 9 segundos).
2. **Conferir que o "Mostrar" pegou**: o `select` tem que estar em "1000" e a quantidade de linhas tem que ser maior que 10, ou então o "Siguiente" tem que estar desabilitado. Ver só 10 linhas quase sempre quer dizer que o seletor não mudou, e não que só existem 10 pendências. Em 06/10/2026 eram 92 em aberto, e uma leitura com o seletor travado em 10 fez parecer que eram 10.
3. Ler a tabela inteira e extrair, de cada linha: nº do pedido, transportadora, motivo da novedad (`Novedad: ...`) e data. Guardar em `window.__nv` e ler o resultado em pedaços (contagem por motivo e lista de ids), porque a saída do javascript_tool é truncada:
   ```js
   window.__nv=[...document.querySelectorAll('tbody tr')].map(r=>{const t=r.innerText;return {id:t.match(/^\s*(\d{7})/)?.[1], c:t.match(/Transportadora: (\w+)/)?.[1], n:t.match(/Novedad: ([^\n]+)/)?.[1]}}).filter(x=>x.id)
   ```
4. Essa lista é o escopo da auditoria. O banco (passo 1) serve só para os detalhes desses pedidos: movimentos, fotos, telefone, endereço, pedido Shopify. Contar e reportar a partir da tela, nunca do banco.
5. Pedido que está no banco como NOVEDAD mas não aparece na tela não tem mais "Solucionar" nem chat de novedad. Só entra se for caso de indenização (parado há meses): aí montar o texto para o Savin mandar pelo suporte da Dropi ou pelo contato da transportadora.

## 1. Detalhes dos pedidos (MCP Dropi / Chegou Operações, operação `drop`)

Chamar `mapa_dos_dados` uma vez. Filtro base: `pais='chile' AND dados->'shop'->>'name'='Tienda Tuya' AND sumiu_da_dropi_em IS NULL`, mais `order_id IN (...)` com os pedidos da tela (passo 0).

Detalhe por pedido: `order_id`, `phone`, `shipping_company`, `dados->>'shipping_guide'`, `dados->>'shop_order_number'` (Shopify = "#3" + número), cidade, `dados->>'dir'` e os últimos movimentos de `dados->'servientrega_movements'` (nom_mov, created_at, image_evidence):
```sql
SELECT p.order_id, p.phone, p.dados->>'dir' dir, p.city,
 (SELECT string_agg(left(m->>'created_at',16)||' '||(m->>'nom_mov')||CASE WHEN m->>'image_evidence' IS NOT NULL THEN ' [F]' ELSE '' END, ' > ' ORDER BY m->>'created_at')
  FROM (SELECT m FROM jsonb_array_elements(p.dados->'servientrega_movements') m ORDER BY m->>'created_at' DESC LIMIT 4) x) movs
FROM metricas_dropi_dropipedido p WHERE p.pais='chile' AND p.order_id IN (...)
```
Endereço e observações do pedido Shopify: `JOIN vendas_shopify_vendashopify v ON v.shopify_order_id=(d.dados->>'shop_order_id')::bigint` (`endereco_entrega`, `etiquetas`, `observacao`). A `observacao` mostra quando a Talkyria não ligou (ex.: "SIN SALDO", "SIN AGENTE ACTIVO").

## 2. Cruzar com a Talkyria (Claude in Chrome, numa aba nova; a aba da Dropi fica aberta)

**Aba em segundo plano:** o Chrome desacelera muito os `setTimeout` de abas que não estão visíveis. Um script com várias esperas internas trava depois de poucos itens (em 06/10 parou no 7º de 92). Não colocar espera dentro do script. Fazer um passo por chamada de `javascript_tool` e esperar entre os passos com `computer wait` dentro de um `browser_batch` (ex.: buscar → wait 3 → abrir → wait 2 → ler).

### 2a. Soluções combinadas e não aplicadas

1. Em `https://app.talkyria.com/novedades`, ler os cards do topo e o **Saldo** na barra lateral (`document.body.innerText.match(/Saldo\s*\$[\d.,]+/)`). A lista dessa tela não tem todos os pedidos em novedade na Dropi, então não usar como fonte principal.
2. Fonte principal: `https://app.talkyria.com/llamadas`, período **"7 dias"**, filtro **Resultado = Confirmado** (abrir o botão "Resultado" e marcar o checkbox do label "Confirmado"). Percorrer as páginas (20 por página; clicar no botão com o número da próxima página via JS, `wait 2`, ler) e guardar o nº de cada linha marcada "Dropi" com a data da ligação. As linhas Dropi ficam no começo (são as mais recentes), e as páginas antigas têm só confirmações Shopify.
3. Cruzar com a lista da tela da Dropi (passo 0). Os que coincidem são candidatos.
4. Para cada candidato, ler o resumo: colocar o nº na busca (`wait 3`), clicar no botão de título "Transcripcion" da linha (`wait 2`) e ler `row.nextElementSibling` a partir de "Resumen de la conversación". Ler em pedaços curtos, de 2 a 4 pedidos por chamada, e trocar sequências longas de dígitos por "N" (`.replace(/\d{7,}/g,'N')`): textos com telefone fazem a ferramenta bloquear a saída.
5. Classificar cada resumo:
   - **Solução de novedad** ("resolver una novedad", cliente aceitou receber ou reprogramar, deu endereço, referência ou horário): vai para o passo 5 com o que foi combinado.
   - **Confirmação do pedido original** ("confirmar un pedido", "será despachado en 3 a 7 días"): não é solução de novedad, ignorar.
   - **Aviso de entrega** ("ya se encuentra en camino") em que o cliente confirma que está disponível: conta como solução (reofertar no mesmo endereço).
   - **Não aplicar e avisar o Savin**: cliente diz que o produto é diferente do anunciado, que já recebeu o produto, ou que vai retirar na agência.

### 2b. Disparar ligação de novedad (quando o Savin pedir para resolver)

- Pedidos que precisam falar com o cliente (recusa com foto válida, endereço sem dado novo, problema de cobrança, cliente que não atendeu): ligar de novo pela Talkyria **mesmo que já tenham tentativas anteriores**.
- Antes de disparar, conferir o saldo. Cada pedido pode gerar várias tentativas (cerca de $0,05 a $0,40 por ligação atendida). Se o saldo não cobrir o lote com folga, avisar o Savin antes: saldo zerado também para as ligações de confirmação dos pedidos novos.
- Como disparar: na tela `/novedades`, cada pedido tem o botão de título **"Gestionar esta novedad con una llamada"** (texto "Llamar"). Ele abre o diálogo "Gestionar novedad #..." com o agente ("Cada pedido con su agente asignado"); clicar **"Llamar ahora"**. Achar o botão do pedido subindo pelos `parentElement` até o bloco que contém um único `#nnnnnnn`.
- Conferir em `/llamadas` (primeiras linhas) que as ligações começaram.
- O que não aparece na tela de novedades da Talkyria não dá para disparar: listar com o telefone para o Igor ligar.
- Os pedidos Blue "EN ESPERA EN OFICINA" não aparecem para o agente de agência (Oficina) da Talkyria. Avisar o Savin para tratar com o suporte da Talkyria.

### 2c. Alertas de qualidade da Talkyria (anotar na mesma passada)

- a IA falando o nome genérico da Dropi (ex.: "J - AMPOLLETA CAMARA SEGURIDAD CON APP") em vez do nome oficial da Shopify;
- a IA prometendo guia ou mensagem por WhatsApp;
- a IA marcando data errada ou já passada (ex.: "lunes 30 de septiembre" numa ligação de outubro);
- a IA dizendo outro nome de loja (ex.: "tienda klk") em vez de "Tienda Chile";
- tentativas acima do limite (6/5, 10/5);
- saldo baixo;
- cliente que recusou dizendo que o produto é diferente do da loja (ex.: perfumes "chineses" em vez de árabes, câmera sem painel solar). Isso é problema de produto ou fornecedor e reenviar não resolve.

## 3. Auditar as fotos (Claude in Chrome)

- Fotos Starken: `https://restservices.starken.cl/apiprd/starkenservices/rest/ImageListenerDevolucion?codigoOrdenFlete={guia}&secEvento={n}&hri=...`. A Blue Express normalmente não tem foto.
- O proxy da nuvem bloqueia starken.cl: abrir uma foto na aba do usuário (mesma origem) e rodar `fetch` em lote via javascript_tool, gravando em `window.__ev` e lendo depois.
- Ler o EXIF de cada JPEG: DateTimeOriginal (0x0132), modelo (0x0110), ponteiro GPS (0x8825). Hoje o bloco GPS vem vazio, então não há geolocalização. Dizer isso ao Savin em vez de inventar localização.
- Calcular um hash simples dos bytes para achar a mesma foto reaproveitada em pedidos diferentes.

Incoerências a procurar:
1. Tentativa repetida sem foto nova (dois eventos com o mesmo `secEvento`).
2. Hora do EXIF muito diferente da hora do evento.
3. Evento fora do horário de entrega (ex.: recusa registrada às 20:10, 21:34 ou 01:10). É motivo suficiente para reofertar direto.
4. Foto que não prova presença no endereço: só a etiqueta, foto de longe ou da estrada, foto de outro número de casa.
5. "RECHAZADO POR CLIENTE" na 1ª tentativa em massa no mesmo dia, em muitas cidades: pedir contestação à Starken.
6. Blue "EN ESPERA EN OFICINA" com COBRO REALIZADO / DINERO RENDIDO POR FINANZAS: o cliente pagou e o status está travado. Cobrar da Dropi como entregue.
7. Pedidos parados há meses: pedir indenização.
8. "RECHAZADO POR CLIENTE" em que a Talkyria mostra que o cliente quer receber: a recusa é falsa.

Ver as fotos com screenshot pequeno (scale 0.4), em lotes de 4 a 6.

## 4. Classificar e propor solução

| Grupo | Ação |
|---|---|
| Solução combinada na Talkyria e não aplicada | Prioridade 1: Solucionar na Dropi com o que foi combinado |
| Recusa sem prova ou fora do horário | Solucionar na Dropi (volver a ofrecer) citando o horário ou a falta de prova no texto |
| Recusa com foto válida | Ligar pela Talkyria (2b); se o cliente confirmar, Solucionar |
| No se ubica / dirección incorrecta / inubicable | Se o endereço já tem referência boa, reofertar com endereço completo + telefone + "llamar al cliente al llegar"; se falta dado, ligar antes |
| Cambio de domicilio | Ligar para pegar o endereço novo antes de solucionar |
| Problema cobro (Blue) | Ver os movimentos; se o cliente quis pagar, reofertar; senão, ligar antes |
| Produto diferente do anunciado | Não reofertar; avisar o Savin (fornecedor ou produto) |
| En espera en oficina | Avisar o cliente para retirar (agente Oficina ou Igor) |
| Cobro realizado travado | Reclamar na Dropi/carteira |
| Parado há meses ou perdido | Montar o texto de indenização (guia, pedido, valor, desde quando) para o Savin enviar |

## 5. Aplicar as soluções na Dropi (Claude in Chrome)

**Uma aba por pedido, em paralelo.** Criar uma aba para cada pedido do lote, abrir `https://app.dropi.cl/dashboard/novelties` em todas e trabalhar nelas ao mesmo tempo, passo a passo: todas buscam, depois todas clicam Solucionar, e assim por diante, com `computer wait` entre as rodadas. Quando um pedido der "Éxito", fechar a aba dele. Manter a aba original do Savin aberta.

Passos em cada aba, sempre por `javascript_tool` (clique e digitação por coordenada falham em aba de fundo):
1. Marcar o rádio **ORDEN ID** (`[...document.querySelectorAll('input[type=radio]')].find(r=>/ORDEN/.test(r.parentElement.innerText)).click()`).
2. No campo `input[placeholder="Buscar..."]`: definir o valor, disparar `input` e depois `keyup`/`keydown` Enter. Esperar uns 8 a 10 segundos e conferir a linha. Se aparecer "No hay resultados", repetir a busca uma vez; se continuar vazio, o pedido saiu da lista: avisar e seguir.
3. Clicar **Solucionar** e esperar 8 a 10 segundos (aparece "Buscando..." antes do formulário).
4. Clicar **Sí** (volver a ofrecer) e esperar uns 3 segundos. Nunca clicar **NO**: isso devolve o pedido ao remetente.
5. Preencher o formulário, que muda conforme a transportadora. Para cada campo, definir o valor e disparar `input`, `change` e `blur`:
   - **Starken:** select **Solución** = "VOLVER A OFRECER" (valor "Sacar a Reparto"), **Cambiar dirección** = endereço completo numa linha (rua, número, comuna + referência ou horário combinado) e **Número de teléfono**.
   - **Blue:** 6 campos de texto, nesta ordem: Datos adicionales a la dirección, Solución (texto), Calle, Numero (só número), Comuna e Region.
   - **O telefone é obrigatório** na Starken: sem ele, o "Guardar solución" não faz nada e não mostra erro. Pegar em `metricas_dropi_dropipedido.phone`.
6. Clicar **GUARDAR SOLUCION**. O botão fica desabilitado enquanto envia (10 a 30 segundos). Não clicar de novo: passar para a próxima aba e voltar depois.
7. Sucesso = "Éxito — Novedades reportadas con éxito" e o formulário fecha. Aí fechar a aba.

Se um passo falhar duas vezes no mesmo pedido, parar e avisar o Savin com o pedido e o passo que travou (não ficar em loop).

No final, entregar de uma vez a lista completa: o que foi solucionado, as ligações disparadas, o que ficou de fora e por quê, e o que o Savin precisa fazer manualmente (recarga de saldo, pedidos para o Igor ligar, chamados na Dropi ou Talkyria, texto de indenização).

## Regras

- Solucionar, mandar mensagem à transportadora ou disparar ligação é ação em nome do Savin. Se ele já pediu "resolva" ou "resolva todas", executar direto. Se a auditoria foi só de leitura, mostrar a lista e pedir ok antes, por lote.
- Avisar antes se o gasto na Talkyria puder zerar o saldo.
- Não inventar números; citar o período e as contagens, sempre a partir da tela da Dropi.
- Na Dropi, a lupa abre o detalhe do pedido (histórico de movimentos com o link "Ver Evidencia"); o ícone ao lado abre o chat com Transportadora/Proveedor (só existe para pedidos que estão na tela de Novedades).