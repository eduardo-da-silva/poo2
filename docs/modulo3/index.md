# Módulo 3 — Estratégias

# O sistema funciona, mas não é flexível

O Módulo 2 foi concluído. O fluxo de compra está completo: carrinho vira pedido, pedido é pago, enviado, entregue. O gerente está satisfeito com o que já existe — e, como sempre, já quer mais.

Desconto para clientes VIP. Desconto de aniversário. Cupons promocionais com validade. Frete grátis acima de um certo valor. Cada pedido novo, se resolvido com um `if/elif`, torna o sistema mais difícil de manter — e mais fácil de quebrar.

Neste módulo, vamos aprender a resolver "várias formas de fazer a mesma coisa" sem empilhar condicionais. É o primeiro padrão de projeto do curso: **Strategy**.

## O que você aprenderá

- **Interfaces** — contratos que várias classes podem cumprir
- **Polimorfismo de verdade** — código que trata objetos diferentes da mesma forma
- **Strategy** — o primeiro padrão de projeto do curso
- **Open/Closed** — estender comportamento sem editar código que já funciona
- Quando reaproveitar uma interface existente e quando criar uma nova

## O que existe hoje

- ✔ Fluxo de compra completo (carrinho → pedido → pagamento → envio → entrega)
- ✔ `Produto.aplicar_desconto` — desconto único e permanente
- ❌ Desconto diferente por tipo de cliente
- ❌ Cupons promocionais
- ❌ Cálculo de frete

## Estrutura do módulo

1. **Capítulo 8 — O problema dos descontos** — o gerente pede descontos diferentes por tipo de cliente. Resolvemos com uma cadeia de condicionais, e sentimos na pele por que isso não escala.
2. **Capítulo 9 — Strategy: desconto como objeto** — cada regra de desconto vira uma classe. `Pedido` para de conhecer os detalhes de cada uma.
3. **Capítulo 10 — Cupom** — uma entidade nova reaproveita a mesma interface de desconto, agora com validade.
4. **Capítulo 11 — Frete** — o mesmo padrão resolve um problema diferente, fechando o módulo com desconto e frete combinados no valor final do pedido.

---

Prepare-se para ver o mesmo padrão resolver três problemas diferentes — e para perceber quando *não* reaproveitar uma interface é a decisão certa.
