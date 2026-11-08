# Módulo 5 — Organização do Sistema

# O sistema funciona, mas não sabe onde guardar as coisas

O Módulo 4 deixou o E-Commerce criando bem os seus objetos e montando suas dependências num único lugar. O gerente aprovou — e voltou com uma pergunta simples: "o pedido de ontem, onde ele está?"

A resposta era incômoda. Pedidos, produtos, tudo vive na memória do programa e desaparece quando ele termina. E, ao olhar o código com os olhos de quem acabou de chegar ao time, outra coisa ficou evidente: regras de negócio, coordenação do fluxo e detalhes técnicos moram na mesma pasta, lado a lado, sem nada que diga qual é qual.

Neste módulo o sistema aprende a **lembrar** — e, mais importante, aprende a separar *o que ele é* de *onde e como ele guarda e entrega as coisas*.

## O que você aprenderá

- **Repository** — uma coleção de objetos de domínio que esconde onde eles são guardados
- **Persistência com SQLite** — guardar de verdade, com o módulo `sqlite3` da biblioteca padrão, e entender o que um **ORM** mudaria
- **Casos de uso** — uma classe para cada intenção de quem usa o sistema
- **Camadas** — domínio, aplicação e infraestrutura, e a regra de quem pode conhecer quem
- **Inversão de Dependências** — a abstração pertence a quem a usa; os detalhes se adaptam a ela
- **Testes de arquitetura** — verificar a regra de dependência automaticamente

## O que existe hoje

- ✔ Fluxo de compra completo, com desconto, cupom, frete, pagamento, entrega e notificação
- ✔ Factories e Injeção de Dependências, com raiz de composição
- ❌ Qualquer forma de guardar os dados além da memória
- ❌ Separação entre regra de negócio, coordenação e infraestrutura
- ❌ Uma regra, verificada, sobre quem pode depender de quem

## Estrutura do módulo

1. **Capítulo 16 — O sistema precisa lembrar** — pedidos e produtos ganham identidade, e um **repositório** passa a ser o único que sabe onde eles ficam. A primeira implementação é em memória.
2. **Capítulo 17 — Guardando de verdade** — o mesmo contrato ganha uma implementação em **SQLite**. O serviço não muda. O capítulo também mostra onde um **ORM** entraria e por que trocar seria barato.
3. **Capítulo 18 — Casos de uso e camadas** — o código se organiza em **domínio**, **aplicação** e **infraestrutura**; o `ServicoPedido` se divide em **casos de uso**. Um teste de arquitetura aponta uma violação que fica registrada como dívida.
4. **Capítulo 19 — Quem depende de quem?** — a dívida é paga com **Inversão de Dependências**, e a arquitetura inteira passa a ser vigiada por testes.

Ao final há um [checkpoint de entrega](entrega.md) do Projeto Financeiro, cobrindo os Capítulos 16 a 19.

!!! tip "Código do módulo"

    O código de cada capítulo está em `code/modulo5/capituloNN/`, cumulativo: cada pasta começa de onde a anterior terminou. Para rodar os testes de um capítulo, entre na pasta e execute `pytest`.

---

Prepare-se para ver um mesmo contrato ser cumprido por duas tecnologias diferentes, sem que o resto do sistema perceba — e para entender por que essa é a característica de um sistema que consegue envelhecer bem.
