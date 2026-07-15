# Capítulo 5 — Do carrinho ao pedido

!!! info "Situação da Empresa"

    Nossa loja virtual já está funcionando. Clientes se cadastram, montam carrinhos, calculam totais. Mas o gerente percebeu um problema grave: ninguém consegue finalizar uma compra. Os carrinhos são montados, mas não viram pedidos. A empresa está perdendo vendas porque o sistema não registra a conclusão da compra.

    Maria, uma cliente real, ligou para o suporte: "Adicionei produtos ao carrinho, mas não encontro o botão de finalizar. Como compro?". Nosso primeiro objetivo neste módulo é responder a essa pergunta.

No Módulo 1, construímos um sistema que representa bem o domínio: produtos, categorias, clientes, carrinhos. Mas carrinho é temporário. Ele existe enquanto o cliente está comprando. No momento em que a compra é concluída, precisamos de um registro permanente: o **pedido**.

Essa é a primeira lição do módulo: **o software evolui porque o negócio evolui**. Quando começamos, a empresa só precisava organizar o catálogo. Agora precisa vender. Amanhã precisará controlar pagamentos, estoque, fretes. Cada fase do negócio exige uma expansão do modelo.

---

## O que está faltando?

Antes de escrever código, vamos responder a perguntas fundamentais.

??? question "O que um pedido precisa saber? Liste as informações que um pedido deve conter."

Um pedido representa uma compra concretizada. Ele precisa:
- saber **quem** comprou (cliente)
- saber **o que** foi comprado (itens, com produto, quantidade e preço)
- saber **quando** foi criado
- saber **quanto** custou (total)
- saber **em que situação** está (criado, pago, enviado etc.)

Algumas dessas informações já existem no Carrinho. Mas carrinho e pedido têm responsabilidades diferentes. O carrinho é um rascunho temporário. O pedido é um documento definitivo.

---

## Criando o Pedido

Vamos começar implementando a classe `Pedido`. Neste primeiro momento, ela será simples: guarda itens e calcula o total.

```python title="ecommerce/pedido.py"
from ecommerce.item_pedido import ItemPedido


class Pedido:

    def __init__(self) -> None:
        self._itens: list[ItemPedido] = []
        self._status = "criado"

    @property
    def itens(self) -> list[ItemPedido]:
        return list(self._itens)

    @property
    def status(self) -> str:
        return self._status

    def adicionar_item(self, produto: "Produto", quantidade: int) -> None:
        if self._status != "criado":
            raise ValueError("Não é possível adicionar itens a um pedido já finalizado")
        preco_no_momento = produto.preco
        self._itens.append(ItemPedido(produto, quantidade, preco_no_momento))

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self._itens)

    def quantidade_itens(self) -> int:
        return len(self._itens)
```

Note que Pedido guarda uma **cópia** dos dados no bloco `if __name__`, mas a proteção real está no `@property` e no método `adicionar_item`. Se o status não for `"criado"`, o pedido rejeita novos itens. Isso é uma primeira forma de **encapsulamento**: o objeto controla quem mexe em seus dados.

!!! tip "🧠 Pense antes de continuar"

    Note que `self._status` começa como uma string simples. Em breve isso vai mudar. Conforme o pedido evolui, nossa implementação também evolui. É assim que software real funciona: primeiro resolvemos o problema imediato, depois refinamos.

---

## Criando o ItemPedido

ItemPedido se parece com ItemCarrinho. Mas tem uma diferença sutil e importante.

??? question "ItemPedido e ItemCarrinho são iguais? Se não, quais as diferenças?"

Eles guardam informações parecidas (produto, quantidade, preço). Mas representam conceitos diferentes:

- **ItemCarrinho**: representa uma *intenção* de compra. O cliente ainda pode remover, alterar quantidade, desistir.
- **ItemPedido**: representa uma *compra realizada*. Depois de criado, não pode mais ser alterado.

Por isso ItemPedido utiliza `@property` sem setter — seus atributos são definidos no construtor e não mudam mais.

```python title="ecommerce/item_pedido.py"
class ItemPedido:

    def __init__(self, produto: "Produto", quantidade: int, preco_no_momento: float) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if preco_no_momento <= 0:
            raise ValueError("Preco deve ser positivo")
        self._produto = produto
        self._quantidade = quantidade
        self._preco_no_momento = preco_no_momento

    @property
    def produto(self) -> "Produto":
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def preco_no_momento(self) -> float:
        return self._preco_no_momento

    def calcular_subtotal(self) -> float:
        return self._preco_no_momento * self._quantidade
```

⚠️ **Erro comum neste ponto** — Tentar usar a mesma classe ItemCarrinho dentro do Pedido. As classes são estruturalmente semelhantes, mas têm responsabilidades diferentes. ItemCarrinho pode ter métodos como `alterar_quantidade`. ItemPedido nunca deve permitir isso. Criar uma nova classe é a decisão correta, mesmo que o código pareça repetitivo.

---

## Evoluindo o Cliente

Agora que Pedido existe, o Cliente precisa conhecer seus pedidos.

```python title="ecommerce/cliente.py" hl_lines="5-6 9-11 16-17"
class Cliente:

    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email
        self.carrinho: "Carrinho | None" = None
        self._pedidos: list["Pedido"] = []

    @property
    def pedidos(self) -> list["Pedido"]:
        return list(self._pedidos)

    def possui_carrinho(self) -> bool:
        return self.carrinho is not None

    def adicionar_pedido(self, pedido: "Pedido") -> None:
        self._pedidos.append(pedido)
```

A lista de pedidos é privada (`_pedidos`) e exposta via `@property` que retorna uma cópia. Isso impede que código externo manipule a lista diretamente — outro exemplo de encapsulamento.

---

## Finalizando o carrinho

O Carrinho precisa de um método que transforme seus itens em um Pedido.

```python title="ecommerce/carrinho.py" hl_lines="16-22"
from ecommerce.item_carrinho import ItemCarrinho
from ecommerce.pedido import Pedido


class Carrinho:

    def __init__(self) -> None:
        self.itens: list[ItemCarrinho] = []

    def adicionar_item(self, produto: "Produto", quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover_item(self, produto: "Produto") -> None:
        self.itens = [i for i in self.itens if i.produto is not produto]

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self.itens)

    def quantidade_itens(self) -> int:
        return len(self.itens)

    def finalizar(self) -> Pedido:
        if not self.itens:
            raise ValueError("Carrinho vazio")
        pedido = Pedido()
        for item in self.itens:
            pedido.adicionar_item(item.produto, item.quantidade)
        return pedido
```

🏗️ **Decisão de Projeto** — Por que o método `finalizar` está no Carrinho e não no Cliente?

Essa é uma decisão importante. Poderíamos ter colocado a lógica no Cliente (`cliente.finalizar_compra()`), no Pedido (`Pedido.a_partir_de(carrinho)`) ou em uma função separada (`criar_pedido(carrinho, cliente)`).

Optamos por colocar no Carrinho porque:

1. O Carrinho conhece seus itens — ele tem as informações necessárias.
2. A responsabilidade "transformar-se em pedido" é do próprio carrinho.
3. Mais adiante, no Capítulo 7, o Cliente orquestrará o fluxo completo usando esse método.

No entanto, isso não é definitivo. Conforme o fluxo de compra ficar mais complexo, talvez essa responsabilidade mude de lugar. Evolução do software é assim: decisões de hoje podem ser repensadas amanhã.

---

## Testes

Vamos criar os testes para verificar se tudo funciona.

```python title="tests/test_item_pedido.py"
import pytest
from ecommerce.categoria import Categoria
from ecommerce.item_pedido import ItemPedido
from ecommerce.produto import Produto


class TestItemPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)

    def test_criar_item_pedido(self) -> None:
        item = ItemPedido(self.notebook, 2, self.notebook.preco)
        assert item.produto == self.notebook
        assert item.quantidade == 2
        assert item.preco_no_momento == 3500.0

    def test_calcular_subtotal(self) -> None:
        item = ItemPedido(self.notebook, 3, self.notebook.preco)
        assert item.calcular_subtotal() == 10500.0

    def test_quantidade_invalida(self) -> None:
        with pytest.raises(ValueError):
            ItemPedido(self.notebook, 0, self.notebook.preco)
```

```python title="tests/test_pedido.py"
import pytest
from ecommerce.categoria import Categoria
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_criar_pedido_vazio(self) -> None:
        pedido = Pedido()
        assert pedido.quantidade_itens() == 0
        assert pedido.calcular_total() == 0.0
        assert pedido.status == "criado"

    def test_adicionar_item(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        assert pedido.quantidade_itens() == 1

    def test_calcular_total(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        pedido.adicionar_item(self.mouse, 3)
        total_esperado = (2 * 3500.0) + (3 * 150.0)
        assert pedido.calcular_total() == total_esperado

    def test_nao_adicionar_apos_finalizado(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido._status = "pago"
        with pytest.raises(ValueError):
            pedido.adicionar_item(self.mouse, 1)
```

```bash
$ pytest tests/
```

??? tip "Testes passando"

    Todas as classes do módulo anterior continuam funcionando. Os novos testes garantem que Pedido e ItemPedido se comportam corretamente.

---

## 🧩 Aplicando ao Projeto Financeiro

No mundo financeiro, lançamentos contábeis são como itens de carrinho: eles existem em estado aberto até que sejam "fechados" em um período.

A tarefa para você: crie uma classe `Fechamento` no seu projeto financeiro. Ela deve receber uma lista de lançamentos e consolidá-los em um resumo do período. Assim como `Carrinho.finalizar()` transforma itens em um pedido, seu `Fechamento` deve transformar lançamentos abertos em um registro consolidado.

Não implementamos a solução. Você precisa decidir:
- Que informações o `Fechamento` deve guardar?
- Os lançamentos originais devem ser copiados ou referenciados?
- O que acontece se não houver lançamentos no período?

---

## 📌 Resumo

- O software evolui porque o negócio evolui — novas necessidades geram novas classes
- **Pedido** representa uma compra concretizada, diferente do Carrinho (rascunho temporário)
- **ItemPedido** é estruturalmente similar a ItemCarrinho, mas tem responsabilidades diferentes (imutável, representa compra realizada)
- **Encapsulamento** começa a aparecer: atributos privados, properties sem setter, validação de estado
- **Método `finalizar`** transforma Carrinho em Pedido, mantendo a responsabilidade onde os dados estão

## O que mudou no sistema

- ✔ Carrinho agora pode ser finalizado
- ✔ Pedido existe como classe
- ✔ ItemPedido existe como classe
- ✔ Cliente conhece seus pedidos
- ❌ Estados ainda são strings simples (vamos melhorar)
- ❌ Pagamento ainda não existe
- ❌ Fluxo completo não está integrado

## O que vem a seguir

Agora temos pedidos. Mas eles só têm um estado: "criado". O gerente quer saber: qual pedido já foi pago? Qual foi enviado? Qual foi cancelado?

No próximo capítulo, vamos dar vida ao ciclo de vida do pedido.
