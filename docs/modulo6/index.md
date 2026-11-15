# Módulo 6 — Eventos

# O sistema sabe fazer. Falta saber quem precisa saber.

O Módulo 5 deixou o E-Commerce organizado: o domínio não conhece o banco, a aplicação não conhece o e-mail, e uma regra, verificada por testes, diz quem pode depender de quem. O gerente aprovou, e voltou com um pedido simples: "quando o pedido for pago, tire do estoque".

A resposta honesta era uma linha a mais dentro de `PagarPedido`. E depois outra, para a auditoria, e outra, para o financeiro. O caso de uso que existia para **pagar um pedido** passava a conhecer todo mundo que tem interesse em um pagamento, e a lista só cresce.

Neste módulo o sistema aprende a **anunciar o que aconteceu** sem saber quem vai reagir, e a **ser observado** sem que isso entre no código de cada operação. É o último módulo do curso, e fecha com a entrega final do Projeto Financeiro.

## O que você aprenderá

- **Observer** — um objeto avisa os interessados sem conhecer as classes concretas deles
- **Eventos de domínio** — o acontecimento deixa de ser uma chamada de método e vira um objeto, um fato com nome no passado
- **Barramento de eventos** — quem publica não conhece quem assina, e quem assina não conhece quem publicou
- **Decorator** — acrescentar log e medição de tempo em volta de uma operação, sem editá-la
- **Comando × evento** — a intenção e o fato: dois lados do mesmo acontecimento
- **Reações que falham** — o que acontece quando um manipulador lança um erro, e por que fato e reações não são atômicos
- **O quadro dos padrões** — o que cada padrão do curso resolveu, e quais ficam de fora

## O que existe hoje

- ✔ Domínio, aplicação e infraestrutura separados, com regra de dependência verificada por testes
- ✔ Repositórios em memória e em SQLite, trocados na raiz de composição
- ❌ O estoque nunca diminui quando um pedido é pago
- ❌ Cada reação nova a um pagamento exige abrir o caso de uso
- ❌ Nenhum registro do que o sistema faz, nem do tempo que leva

## Estrutura do módulo

1. **Capítulo 20 — Quem precisa saber?** — a baixa de estoque expõe o problema de um caso de uso que conhece todo mundo. O **Observer** inverte o fluxo: quem se importa se inscreve.
2. **Capítulo 21 — Fatos, não ordens** — "o pedido foi pago" vira um **evento**, e um **barramento** passa a levá-lo a quem assina. Uma auditoria completa entra sem abrir nenhum caso de uso.
3. **Capítulo 22 — Embrulhando comportamento** — **log** e **medição de tempo** entram em volta dos casos de uso com o **Decorator**. O capítulo também separa comando e evento.
4. **Capítulo 23 — Quando a reação falha** — duas pessoas compram a última unidade. O que fazer quando uma reação falha, e um olhar sobre todos os padrões do curso.

Ao final há a [entrega final](entrega.md) do Projeto Financeiro, cobrindo do Capítulo 1 ao 23.

!!! tip "Código do módulo"

    O código de cada capítulo está em `code/modulo6/capituloNN/`, cumulativo: cada pasta começa de onde a anterior terminou, e o Capítulo 20 parte do código do Capítulo 19. Para rodar os testes de um capítulo, entre na pasta e execute `pytest`.

---

Prepare-se para ver um caso de uso encolher em vez de crescer a cada exigência nova, e para entender por que quem faz uma coisa não deveria precisar saber quem se importa com ela.
