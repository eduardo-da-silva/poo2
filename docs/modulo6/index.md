# Módulo 6 — Eventos

# O sistema sabe fazer. Falta saber quem precisa saber.

O Módulo 5 deixou o E-Commerce organizado: o domínio não conhece o banco, a aplicação não conhece o e-mail, e uma regra, verificada por testes, diz quem pode depender de quem. O gerente aprovou, e voltou com um pedido simples: "quando o pedido for pago, tire do estoque".

A resposta honesta era uma linha a mais dentro de `PagarPedido`. E depois outra, para a auditoria, e outra, para o financeiro. O caso de uso que existia para **pagar um pedido** passava a conhecer todo mundo que tem interesse em um pagamento, e a lista só cresce.

Neste módulo o sistema aprende a **anunciar o que aconteceu** sem saber quem vai reagir. Depois ganha uma **porta de entrada**, para que alguém finalmente o use, e enfrenta o primeiro cenário em que uma reação falha. É o último módulo do curso, e fecha com a entrega final do Projeto Financeiro.

## O que você aprenderá

- **Observer** — um objeto avisa os interessados sem conhecer as classes concretas deles
- **Eventos de domínio** — o acontecimento deixa de ser uma chamada de método e vira um objeto, um fato com nome no passado
- **Barramento de eventos** — quem publica não conhece quem assina, e quem assina não conhece quem publicou
- **Comando × evento** — a intenção e o fato: dois lados do mesmo acontecimento
- **Pontos de entrada** — um cenário com dados fixos e um menu de terminal, e como a mesma ideia serviria a uma API REST, uma GUI ou uma TUI
- **Reações que falham** — o que acontece quando um manipulador lança um erro, e por que fato e reações não são atômicos
- **Bônus: catálogo de padrões** — Decorator, State, Adapter, Composite, Chain of Responsibility, Command e Builder: o que cada um resolveria no seu projeto

## O que existe hoje

- ✔ Domínio, aplicação e infraestrutura separados, com regra de dependência verificada por testes
- ✔ Repositórios em memória e em SQLite, trocados na raiz de composição
- ❌ O estoque nunca diminui quando um pedido é pago
- ❌ Cada reação nova a um pagamento exige abrir o caso de uso
- ❌ Nenhuma forma de **usar** o sistema fora dos testes

## Estrutura do módulo

1. **Capítulo 20 — Quem precisa saber?** — a baixa de estoque expõe o problema de um caso de uso que conhece todo mundo. O **Observer** inverte o fluxo: quem se importa se inscreve.
2. **Capítulo 21 — Fatos, não ordens** — "o pedido foi pago" vira um **evento**, e um **barramento** passa a levá-lo a quem assina. Uma auditoria completa entra sem abrir nenhum caso de uso.
3. **Capítulo 22 — Colocando o sistema para rodar** — a **porta de entrada**: um cenário fixo e um menu de terminal, mais um esboço de REST. O capítulo também deixa claro que persistimos só uma parte dos dados, e trata o primeiro cenário em que uma reação falha.
4. **Capítulo 23 — Bônus: padrões que ficaram de fora** — um catálogo de padrões para você pesquisar. Na entrega final, você escolhe um e o implementa no seu projeto.

Ao final há a [entrega final](entrega.md) do Projeto Financeiro, com persistência, uma interface, eventos e o padrão do bônus.

!!! tip "Código do módulo"

    O código de cada capítulo está em `code/modulo6/capituloNN/`, cumulativo: cada pasta começa de onde a anterior terminou, e o Capítulo 20 parte do código do Capítulo 19. Para rodar os testes de um capítulo, entre na pasta e execute `pytest`. O Capítulo 22 tem também um programa: na pasta do capítulo, `python main.py` roda os cenários e `python main.py menu` abre o menu de terminal.

---

Prepare-se para ver um caso de uso encolher em vez de crescer a cada exigência nova, e para finalmente ver o sistema funcionando de fora para dentro.
