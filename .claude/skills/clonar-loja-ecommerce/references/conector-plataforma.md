# Conector direto com a plataforma

Sem conector, o código volta como texto e a pessoa cola à mão no editor de tema.
Funciona, mas cada seção custa uma ida e volta manual.

Com conector, o assistente escreve direto na loja. A diferença é real em página
com muitas seções — não é só conveniência.

## Quando vale a pena

**Vale** quando a pessoa vai construir várias seções, ou várias lojas, ou vai
iterar bastante sobre o mesmo layout.

**Não vale** na primeira loja de alguém que nunca viu uma seção funcionar. Quem
ainda não completou o ciclo manual não deve começar depurando permissão de API —
o erro fica indistinguível entre "o código está errado" e "o conector não tem
acesso".

**Regra prática:** só proponha o conector depois que a primeira seção estiver de
pé pelo caminho manual.

## O que o conector precisa poder fazer

Independente da plataforma, a autorização precisa cobrir:

| Capacidade | Para quê |
|---|---|
| Ler e escrever **tema** | Criar o rascunho e publicar alterações |
| Ler e escrever **código do tema** | Criar os arquivos de seção |
| Ler e escrever **produtos** | Criar ou ajustar o produto e suas variações |
| Ler e escrever **arquivos** | Subir imagens |
| Ler e escrever **conteúdo** | Páginas e textos fora do produto |

Faltando qualquer uma, o sintoma é o mesmo e confunde: o assistente diz que fez,
mas nada aparece na loja. **Se isso acontecer, suspeite da permissão antes de
suspeitar do código.**

## Fluxo geral de configuração

O detalhe muda por plataforma, mas a sequência é sempre esta:

1. Criar um app customizado ou credencial de desenvolvedor na plataforma
2. Habilitar as permissões da tabela acima
3. Publicar/liberar uma versão do app
4. Instalar o app na loja
5. Conectar o app ao assistente e autorizar
6. Liberar as permissões do lado do assistente, para não pedir confirmação a
   cada operação

## Verificar antes de construir

Antes de mandar qualquer coisa ser construída, peça algo trivial de leitura —
por exemplo, as informações básicas da loja.

Se os dados voltarem, a conexão está de pé. Se não voltarem, resolva isso antes,
porque todo erro seguinte vai parecer erro de código.

## Segurança

O conector recebe permissão de **escrita** na loja de produção.

- Trabalhe sempre em **tema rascunho**, nunca no publicado
- Revise o que foi criado antes de publicar
- Se a loja estiver faturando, considere testar primeiro numa loja de
  desenvolvimento

Um assistente com permissão de escrita e sem tema rascunho pode derrubar uma
loja que está vendendo.
