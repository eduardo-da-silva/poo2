# Capítulo 8 — O problema dos descontos

!!! info "Situação da Empresa"

    O Módulo 2 terminou com o fluxo de compra completo: carrinho vira pedido, pedido é pago, enviado, entregue. O gerente adorou. E, como sempre, apareceu com uma ideia nova.

    "Quero premiar quem compra com a gente com frequência. E dar um desconto especial de aniversário. E, já que estamos nisso, os clientes VIP também merecem um tratamento diferenciado." Três pedidos em uma frase só — e nenhum deles é sobre alterar o preço do produto para sempre.

Precisamos diferenciar o desconto por **tipo de cliente**, sem tocar no preço do `Produto`. Isso já é uma pista importante: o desconto não é uma propriedade do produto, é uma regra que se aplica **no momento da compra**.

---

## O desconto que já temos

Desde o Módulo 1, `Produto` sabe aplicar um desconto:

```python
def aplicar_desconto(self, percentual: float) -> None:
    if not 0 <= percentual <= 100:
        raise ValueError("Percentual deve estar entre 0 e 100")
    self.preco -= self.preco * (percentual / 100)
```

Esse método resolve um problema diferente do que o gerente está pedindo agora: ele muda o preço do produto **permanentemente**, para todo mundo, para sempre. Serve para uma liquidação, uma reprecificação. Não serve para "o cliente Maria, hoje, nesta compra, tem 15% de desconto porque é VIP" — se usássemos `aplicar_desconto` para isso, o próximo cliente comum pagaria o preço já descontado.

O desconto por tipo de cliente precisa acontecer em outro lugar: no momento em que o **pedido** é fechado, não no produto.

---

## Uma primeira tentativa

O jeito mais direto de resolver isso é perguntar, na hora de calcular o total, que tipo de cliente está comprando:

```python title="ecommerce/pedido.py" linenums="1" hl_lines="8-16"
class Pedido:

    # ... outros métodos ...

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self._itens)

    def calcular_total_com_desconto(self, tipo_cliente: str) -> float:
        total = self.calcular_total()
        if tipo_cliente == "vip":
            total -= total * 0.15
        elif tipo_cliente == "frequente":
            total -= total * 0.10
        elif tipo_cliente == "aniversario":
            total -= total * 0.20
        return total

    # ... demais métodos ...
```

Funciona. Os testes passam. O gerente fica feliz.

!!! warning "⚠️ Erro comum — condicionais que só crescem"

    `calcular_total_com_desconto` parece uma solução razoável — e para três tipos de desconto, talvez seja. O problema não está no código de hoje, está no que ele vira amanhã.

    Cada novo tipo de desconto significa um novo `elif` dentro de `Pedido`. Cada `elif` precisa ser testado. Se dois tipos de desconto puderem se combinar (um cliente VIP que também faz aniversário hoje, por exemplo), a lógica de combinação também entra nessa mesma cadeia. `Pedido` — que deveria só saber gerenciar itens e estado — vira o lugar que conhece **todas as regras de negócio de desconto que a empresa já teve**.

    Isso não é um erro de sintaxe. É um sinal de que a responsabilidade está no lugar errado.

---

!!! tip "🧠 Pense antes de continuar"

    O gerente já mencionou três tipos de desconto. Nada impede que amanhã ele peça um quarto (desconto de primeira compra), um quinto (cupom de indicação), ou que dois descontos precisem se combinar.

    Cada vez que isso acontecer, alguém vai precisar abrir `pedido.py`, entender a cadeia de `if/elif` inteira, e inserir mais um caso no meio dela — torcendo para não quebrar os anteriores. Existe uma forma de adicionar um novo tipo de desconto **sem editar o código que já existe e já funciona**?

---

!!! important "💡 Conceito — Interface"

    Uma interface é um contrato: ela diz **o que** um objeto sabe fazer, sem dizer **como** ele faz. Em Python, isso normalmente vira uma classe base com um método que toda subclasse é obrigada a implementar.

    Se existisse uma interface "calcula um desconto a partir de um total", cada tipo de desconto (VIP, frequente, aniversário, e todos os que ainda não existem) poderia ser uma classe própria que cumpre esse contrato. `Pedido` não precisaria mais saber que "vip" significa 15% — ele só precisaria saber que recebeu algo capaz de calcular um desconto, e perguntar a esse algo qual é o valor.

Isso é o caminho que vamos seguir no próximo capítulo. Por enquanto, guarde a pergunta: **e se cada regra de desconto fosse um objeto, em vez de uma linha dentro de um `if`?**

---

## Testes

```python title="tests/test_pedido.py" linenums="1"
def test_desconto_cliente_vip(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total_com_desconto("vip") == 3500.0 * 0.85

def test_desconto_cliente_frequente(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total_com_desconto("frequente") == 3500.0 * 0.90

def test_desconto_aniversario(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total_com_desconto("aniversario") == 3500.0 * 0.80

def test_sem_desconto_cliente_comum(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total_com_desconto("comum") == 3500.0
```

```bash
$ pytest tests/
```

??? tip "69 testes passando"

    Os quatro novos testes cobrem os três tipos de desconto e o caso sem desconto. Todos os testes dos módulos anteriores continuam passando — não mexemos em nada que já existia, só adicionamos um método novo.

---

## 🧩 Aplicando ao Projeto Financeiro

No seu sistema financeiro, pense em **tipos de rendimento**: poupança rende um percentual fixo ao mês, um CDB pré-fixado rende uma taxa combinada no momento da aplicação, um CDB pós-fixado rende conforme um índice que muda todo mês.

Se você fosse calcular o rendimento de uma aplicação hoje, com um método só, você cairia na mesma armadilha deste capítulo: um `if tipo == "poupanca": ... elif tipo == "cdb_pre": ...` que só cresce.

Não implemente a solução ainda. Apenas responda: no seu projeto, onde essa lógica de cálculo de rendimento está hoje? O que aconteceria se você precisasse adicionar um quarto tipo de investimento?

---

## 📌 Resumo

- **Desconto por tipo de cliente** é uma regra que se aplica no momento da compra, diferente de `Produto.aplicar_desconto` (que muda o preço para sempre)
- A solução mais direta — uma cadeia de `if/elif` dentro de `Pedido` — funciona, mas concentra em uma única classe todas as regras de desconto que a empresa já teve
- **Interface** é um contrato que várias implementações podem cumprir, sem que quem usa o contrato precise saber qual implementação está por trás
- Ainda não resolvemos o problema — só entendemos exatamente qual é o problema

## O que mudou no sistema

- ✔ `Pedido.calcular_total_com_desconto` existe e funciona para três tipos de cliente
- ❌ Adicionar um novo tipo de desconto ainda exige editar `Pedido`
- ❌ Não é possível combinar dois descontos
- ❌ Cupons e frete ainda não existem

## O que vem a seguir

No próximo capítulo, vamos transformar cada regra de desconto em um objeto — e dar nome ao padrão que torna isso possível: **Strategy**.
