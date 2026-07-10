# Capítulo 2 — Conhecendo o domínio

!!! info "Situação da Empresa"

    No capítulo anterior, começamos a pensar como engenheiros de software. Discutimos responsabilidades, modelagem e a importância de projetar antes de codificar. Agora é hora de conhecer a fundo o domínio do nosso E-Commerce.

    A empresa já identificou seus principais produtos, mas ainda não existe uma forma clara de atender clientes, processar pedidos ou gerenciar vendas. Antes de modelar qualquer classe, precisamos entender como uma loja virtual realmente funciona.

No capítulo anterior discutimos o que significa projetar software orientado a objetos e por que modelar o domínio é mais importante que escrever código. Agora chegou o momento de conhecer o domínio do nosso sistema.

Entretanto, **ainda não escreveremos código**. Nossa primeira tarefa será compreender o problema que estamos tentando resolver.

!!! info "Análise de domínio"

    Essa etapa recebe diversos nomes na Engenharia de Software: levantamento de requisitos, análise de domínio ou modelagem do domínio. Independentemente do nome utilizado, a ideia é a mesma: **entender o problema antes de propor uma solução**.

---

## Um erro muito comum

Imagine que alguém diga:

> "Precisamos desenvolver um sistema para uma loja virtual."

Um desenvolvedor iniciante normalmente abre a IDE e começa a criar classes:

```python
class Produto:  # Exemplo do que NÃO fazer
    pass


class Cliente:  # Criar classes sem entender o domínio
    pass


class Pedido:
    pass
```

Algumas horas depois existem dezenas de classes, centenas de linhas de código e... nenhuma certeza de que o sistema está indo na direção correta. O problema é que **criar classes não significa compreender o domínio**.

!!! warning "A pergunta certa"

    Antes de perguntar **"como implementar?"**, devemos perguntar: **"como esse negócio funciona?"** Essa mudança de perspectiva é um dos grandes diferenciais entre um programador e um engenheiro de software.

---

## O que é um domínio?

Chamamos de **domínio** o conjunto de regras, conceitos e processos relacionados ao problema que estamos tentando resolver.

No nosso caso, o domínio é o funcionamento de um comércio eletrônico.

```mermaid
flowchart LR
    subgraph Domínio do E-Commerce
        A[Produtos] --> B[Carrinho]
        C[Clientes] --> B
        B --> D[Pedidos]
        D --> E[Pagamentos]
        F[Cupons] --> B
        G[Estoque] --> A
    end
```

Um E-Commerce possui diversas regras. Por exemplo:

- Produtos possuem preço
- Produtos pertencem a categorias
- Clientes realizam compras
- Clientes adicionam produtos ao carrinho
- Pedidos são pagos
- Pedidos podem ser cancelados
- Alguns produtos podem estar sem estoque
- Cupons concedem descontos
- Formas de pagamento possuem regras diferentes

!!! tip "Regras de negócio vs. tecnologia"

    Perceba que nenhuma dessas afirmações fala sobre Python. Nenhuma delas fala sobre classes. Nenhuma delas fala sobre banco de dados. **São regras do negócio.** Essas regras continuarão existindo mesmo que o sistema seja reescrito em outra linguagem daqui a dez anos. Esse é justamente o motivo pelo qual dizemos que **o domínio deve guiar o software**, e não o contrário.

---

## Nossa primeira pergunta

Sempre que iniciamos um novo sistema, uma boa pergunta é:

> **Quais são os objetos que existem nesse domínio?**

??? question "Antes de olhar a lista, tente responder por conta própria. Que objetos você identifica no domínio de um E-Commerce?"

Pensando rapidamente, podemos listar:

- Produto
- Categoria
- Cliente
- Carrinho
- Item do Carrinho
- Pedido
- Item do Pedido
- Cupom
- Pagamento
- Estoque

Essa lista não está pronta. Provavelmente ela mudará durante o desenvolvimento. Isso é esperado. Projetar software é um processo **iterativo**.

🧠 **Pense:** o que aconteceria se começássemos a implementar assumindo que essa lista está completa e nunca mudará? Que problemas enfrentaríamos?

---

## Uma observação importante

Muitos alunos imaginam que basta transformar cada substantivo em uma classe. Infelizmente isso não funciona.

Considere a frase:

> "O cliente compra um produto utilizando um cartão de crédito."

Temos os substantivos: **Cliente**, **Produto**, **Cartão**, **Crédito**. Será que todos devem virar classes? Talvez. Talvez não. Depende do domínio.

Às vezes um conceito importante pode ser representado apenas por um atributo. Em outros casos um simples atributo evolui para uma classe inteira.

??? question "Cartão de crédito é classe ou atributo?"

    Em um sistema financeiro, `CartaoDeCredito` provavelmente seria uma classe com diversos atributos e comportamentos (limite, fatura, juros). Em um sistema simples de E-Commerce, talvez seja apenas um atributo do pagamento. **Modelagem envolve decisões, e não regras rígidas.**

---

## Vamos imaginar uma compra

João entra em uma loja virtual. Ele procura um notebook. Encontra um produto. Adiciona duas unidades ao carrinho. Depois adiciona um mouse. Aplica um cupom de desconto. Escolhe pagar com cartão de crédito. Finaliza a compra. Dias depois recebe os produtos.

```mermaid
sequenceDiagram
    actor J as João
    participant L as Loja
    participant Carrinho
    participant Estoque
    
    J->>L: Buscar notebook
    L->>J: Resultados
    J->>Carrinho: Adicionar 2x Notebook
    J->>Carrinho: Adicionar Mouse
    J->>Carrinho: Aplicar cupom DESCONTO10
    J->>L: Finalizar compra
    L->>Estoque: Reservar itens
    L->>J: Pedido confirmado
```

Agora pense: quais objetos participaram dessa história? Provavelmente você respondeu algo semelhante a:

- Cliente
- Produto
- Carrinho
- ItemCarrinho
- Cupom
- Pedido
- Pagamento

Perceba que esses objetos surgiram naturalmente da narrativa. Essa é uma excelente técnica para descobrir entidades de um domínio.

---

## 🧩 Aplicando ao Projeto Financeiro

Crie uma narrativa semelhante para o sistema financeiro. Imagine um usuário chamado "Maria" controlando suas finanças. Ela registra uma receita, categoriza um gasto, define um orçamento mensal. Que objetos surgem naturalmente dessa história? Liste-os antes de prosseguir.

---

## 📌 Resumo

- **Domínio** é o conjunto de regras e conceitos do problema que estamos resolvendo
- Antes de criar classes, precisamos compreender como o negócio funciona
- **Narrativas de compra** ajudam a descobrir entidades naturalmente
- Nem todo substantivo vira classe — modelagem envolve decisões
- As entidades identificadas até agora: Produto, Categoria, Cliente, Carrinho, ItemCarrinho, Pedido, Cupom, Pagamento e Estoque

No próximo capítulo vamos modelar as primeiras entidades do nosso sistema e entender como elas se relacionam — usando diagramas, decisões de projeto e discussões sobre responsabilidades.
