# Módulo 4 — Criando Objetos

# O sistema calcula bem, mas ainda cria mal

O Módulo 3 acabou com o valor do pedido sob controle: desconto por tipo de cliente, cupom e frete, tudo sem `if/elif` empilhado. O gerente aprovou — e, como sempre, já quer mais.

Aceitar só um jeito de pagar está custando venda: ele quer Pix, boleto e cartão. Pedido pago precisa sair para entrega, e agora existe mais de uma origem de despacho, cada uma com seu meio de envio. E o cliente reclama que só descobre o andamento do pedido se entrar no site — quer ser avisado, por e-mail ou por SMS.

Três demandas, um problema em comum: em todas elas, alguma parte do sistema precisa decidir **qual objeto instanciar**. Resolver isso com condicionais espalhadas acopla quem cria a todas as classes concretas — o mesmo tipo de dor do Módulo 3, agora na criação em vez do cálculo.

Neste módulo aprendemos a isolar a criação de objetos em peças dedicadas — **factories** — e, ao final, a parar de espalhar a montagem das dependências pelo código, com **Injeção de Dependências**.

## O que você aprenderá

- **Simple Factory** — concentrar num único lugar a decisão de qual classe instanciar
- **Factory Method** — quando quem cria já é uma família de classes, cada uma decide o que criar
- Reconhecer **qual factory** um problema pede — e quando não aplicar nenhuma
- **Injeção de Dependências** — receber colaboradores prontos em vez de criá-los
- **Raiz de composição** — um único lugar que monta o grafo de objetos do sistema

## O que existe hoje

- ✔ Fluxo de compra completo, com desconto, cupom e frete
- ✔ `Pagamento` como classe concreta única, criada dentro de `Pedido`
- ❌ Mais de uma forma de pagamento
- ❌ Entrega como entidade (só existe cálculo de frete)
- ❌ Notificações ao cliente
- ❌ Um lugar único que monta as dependências do sistema

## Estrutura do módulo

1. **Capítulo 12 — Formas de pagamento e o problema da criação** — o gerente pede Pix, boleto e cartão. `Pagamento` vira abstração, e uma **Simple Factory** tira de `Pedido` o conhecimento das formas concretas.
2. **Capítulo 13 — Meios de entrega: Factory Method** — cada origem de despacho usa um meio de entrega diferente. Como a decisão depende de *quem cria*, a Simple Factory não basta: entra o **Factory Method**.
3. **Capítulo 14 — Notificações** — o problema de criar o objeto certo aparece pela terceira vez. Reconhecemos a forma dele e reaproveitamos a Simple Factory — sem inventar hierarquia.
4. **Capítulo 15 — Quem entrega as dependências?** — três factories espalhadas pelo código. Um único lugar passa a montar o grafo de objetos, e cada peça **recebe** o que precisa: **Injeção de Dependências**.

Ao final há um [checkpoint de entrega](entrega.md) do Projeto Financeiro, cobrindo os Capítulos 12 a 15.

---

Prepare-se para ver o mesmo problema — "qual objeto criar?" — pedir três soluções diferentes, e para perceber que escolher o padrão certo é tão importante quanto conhecê-lo.
