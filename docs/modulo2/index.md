# Módulo 2 — Evoluindo o domínio

# O sistema está crescendo

O Módulo 1 foi concluído. Nosso e-commerce já cadastra produtos e categorias, gerencia clientes e mantém carrinhos de compra com cálculo automático de totais.

Mas o negócio não para.

Os clientes estão usando o sistema. Eles montam carrinhos. Mas descobriram que não é possível finalizar a compra. Não existe pedido. Não existe registro de venda. A empresa precisa urgentemente evoluir o domínio.

Neste módulo, vamos expandir o sistema para incluir pedidos, estados e um fluxo de compra completo. Mais importante: vamos usar essa evolução para aprofundar conceitos fundamentais de Orientação a Objetos.

## O que você aprenderá

- Que **software evolui** — o modelo de hoje não é o modelo de amanhã
- **Encapsulamento** de verdade — objetos que protegem seu próprio estado
- **Invariantes** — regras que nunca podem ser violadas
- **Colaboração entre objetos** — como classes conversam para realizar um fluxo
- **Responsabilidades** cada vez mais precisas
- Que **regras de negócio** moldam o código, e não o contrário

## O que existe hoje

- ✔ Produtos e Categorias
- ✔ Clientes
- ✔ Carrinho e Itens do Carrinho
- ✔ Cálculo de totais e subtotais
- ❌ Pedidos
- ❌ Itens do Pedido
- ❌ Estados e fluxo de compra
- ❌ Pagamento

## Estrutura do módulo

1. **Capítulo 5 — Do carrinho ao pedido** — criamos as classes `Pedido` e `ItemPedido`, e transformamos o carrinho em um pedido pela primeira vez.
2. **Capítulo 6 — O ciclo de vida do pedido** — introduzimos estados, transições e a classe `Pagamento`. O pedido ganha comportamento rico.
3. **Capítulo 7 — O fluxo completo de compra** — unimos todas as peças: carrinho vira pedido, pedido é pago, enviado e entregue. Colaboração entre objetos em ação.

---

Prepare-se. O sistema vai crescer — e sua compreensão sobre Orientação a Objetos também.
