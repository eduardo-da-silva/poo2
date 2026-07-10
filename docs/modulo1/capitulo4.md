# Capítulo 4 — Mão na massa: implementando as classes

Nos capítulos anteriores modelamos o domínio do E-Commerce. Descobrimos entidades, definimos relacionamentos e discutimos responsabilidades. Agora chegou a hora de transformar esse modelo em código.

Neste tutorial você criará todo o projeto do zero — desde o ambiente virtual até os testes automatizados.

---

## Passo 1 — Preparando o ambiente

Crie a estrutura de diretórios do projeto:

```bash
mkdir -p ecommerce tests
```

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale o pytest:

```bash
pip install pytest
```

Crie o arquivo de dependências:

### `requirements.txt`

```text linenums="1"
pytest==8.*
```

Crie o arquivo para ignorar arquivos temporários:

### `.gitignore`

```text linenums="1"
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

---

## Passo 2 — O pacote `ecommerce`

Crie o arquivo que torna a pasta `ecommerce` um pacote Python:

### `ecommerce/__init__.py`

```python linenums="1"
```

Vazio mesmo. Sua função é apenas marcar o diretório como um pacote.

---

## Passo 3 — Categoria

Vamos começar pela classe mais simples.

### `ecommerce/categoria.py`

```python linenums="1"
class Categoria:

    def __init__(self, nome: str) -> None:
        self.nome = nome
```

Não há segredos aqui. Uma categoria possui apenas um nome. Futuramente ela poderá ganhar novos atributos (descrição, departamento), mas por enquanto isso é suficiente.

Teste manual:

```python
from ecommerce.categoria import Categoria

cat = Categoria("Informática")
print(cat.nome)  # Informática
```

---

## Passo 4 — Teste da Categoria

Antes de avançar, vamos criar nosso primeiro teste automatizado.

### `tests/__init__.py`

```python linenums="1"
```

Vazio, para marcar `tests` como pacote.

### `tests/test_categoria.py`

```python linenums="1"
from ecommerce.categoria import Categoria


class TestCategoria:

    def test_cria_categoria_com_nome(self) -> None:
        cat = Categoria("Informática")
        assert cat.nome == "Informática"
```

Rode os testes pela primeira vez:

```bash
pytest
```

Você deverá ver uma saída indicando que **1 teste passou**.

---

## Passo 5 — Produto

Agora uma classe com mais comportamento.

### `ecommerce/produto.py`

```python linenums="1"
from ecommerce.categoria import Categoria


class Produto:

    def __init__(
        self, nome: str, preco: float, quantidade_estoque: int, categoria: Categoria
    ) -> None:
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria

    def esta_disponivel(self) -> bool:
        return self.quantidade_estoque > 0

    def aplicar_desconto(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.preco -= self.preco * (percentual / 100)

    def alterar_preco(self, novo_preco: float) -> None:
        if novo_preco <= 0:
            raise ValueError("Preco deve ser positivo")
        self.preco = novo_preco


if __name__ == "__main__":
    from ecommerce.categoria import Categoria

    cat = Categoria("Informática")
    p = Produto("Notebook", 3500.0, 10, cat)
    print(f"Produto: {p.nome}, Preco: {p.preco}, Disponivel: {p.esta_disponivel()}")

    p.aplicar_desconto(10)
    print(f"Com 10% de desconto: {p.preco}")

    p.alterar_preco(4000.0)
    print(f"Preco reajustado: {p.preco}")
```

Observe algumas decisões de projeto:

- **Preço é float**, não inteiro em centavos. Decisão proposital para simplificar. Em um sistema real discutiríamos `Decimal`.
- **`quantidade_estoque` está no Produto** por enquanto. Já discutimos que futuramente o estoque merecerá uma classe própria.
- **`aplicar_desconto` valida o percentual**. Um desconto de 150% não faz sentido.
- **`alterar_preco` impede preços negativos**. Essa é uma invariante do domínio.

Teste manual:

```bash
python -m ecommerce.produto
```

---

## Passo 6 — Testes do Produto

Agora vamos validar o comportamento do Produto com testes.

### `tests/test_produto.py`

```python linenums="1"
from ecommerce.categoria import Categoria
from ecommerce.produto import Produto


class TestProduto:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")

    def test_cria_produto_com_atributos(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        assert p.nome == "Notebook"
        assert p.preco == 3500.0
        assert p.quantidade_estoque == 10
        assert p.categoria is self.cat

    def test_produto_disponivel_com_estoque(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        assert p.esta_disponivel() is True

    def test_produto_indisponivel_sem_estoque(self) -> None:
        p = Produto("Notebook", 3500.0, 0, self.cat)
        assert p.esta_disponivel() is False

    def test_produto_indisponivel_com_estoque_negativo(self) -> None:
        p = Produto("Notebook", 3500.0, -1, self.cat)
        assert p.esta_disponivel() is False

    def test_aplicar_desconto_valido(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        p.aplicar_desconto(10)
        assert p.preco == 3150.0

    def test_aplicar_desconto_invalido_abaixo_de_zero(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        try:
            p.aplicar_desconto(-5)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass

    def test_aplicar_desconto_invalido_acima_de_cem(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        try:
            p.aplicar_desconto(150)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass

    def test_alterar_preco_valido(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        p.alterar_preco(4000.0)
        assert p.preco == 4000.0

    def test_alterar_preco_invalido_negativo(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        try:
            p.alterar_preco(-500)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass

    def test_alterar_preco_invalido_zero(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        try:
            p.alterar_preco(0)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass
```

Rode os testes novamente:

```bash
pytest
```

Agora você deve ver **11 testes passando** (1 da Categoria + 10 do Produto).

---

## Passo 7 — Cliente

Uma classe simples para representar quem compra.

### `ecommerce/cliente.py`

```python linenums="1"
class Cliente:

    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email
        self.carrinho: "Carrinho | None" = None

    def possui_carrinho(self) -> bool:
        return self.carrinho is not None


if __name__ == "__main__":
    c = Cliente("João", "joao@email.com")
    print(f"Cliente: {c.nome}, Email: {c.email}")
    print(f"Possui carrinho: {c.possui_carrinho()}")
```

O atributo `carrinho` usa uma **string como type hint** (`"Carrinho | None"`) porque a classe `Carrinho` ainda não foi definida. O Python entende essa sintaxe como uma referência futura.

Repare no método `possui_carrinho()`. Ele existe porque o Cliente não deveria expor seu atributo diretamente — ele responde a perguntas sobre seu estado. Objeto rico, lembra?

### `tests/test_cliente.py`

```python linenums="1"
from ecommerce.cliente import Cliente


class TestCliente:

    def test_cria_cliente_com_nome_e_email(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.nome == "João"
        assert c.email == "joao@email.com"

    def test_cliente_sem_carrinho(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.possui_carrinho() is False
```

```bash
pytest
```

**13 testes passando.**

---

## Passo 8 — ItemCarrinho

Aqui aplicamos um princípio importante: quando um relacionamento começa a ter informações próprias, ele merece virar uma classe.

### `ecommerce/item_carrinho.py`

```python linenums="1"
class ItemCarrinho:

    def __init__(self, produto: "Produto", quantidade: int) -> None:
        self.produto = produto
        self.quantidade = quantidade
        self.preco_no_momento = produto.preco

    def calcular_subtotal(self) -> float:
        return self.preco_no_momento * self.quantidade


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    item = ItemCarrinho(notebook, 2)
    print(f"Subtotal: R$ {item.calcular_subtotal():.2f}")
```

A linha `self.preco_no_momento = produto.preco` é uma decisão importante de projeto. O `ItemCarrinho` guarda uma **cópia do preço no momento em que foi criado**. Se o preço do produto mudar depois, o item do carrinho mantém o valor original. Isso evita surpresas na finalização da compra.

### `tests/test_item_carrinho.py`

```python linenums="1"
from ecommerce.categoria import Categoria
from ecommerce.produto import Produto
from ecommerce.item_carrinho import ItemCarrinho


class TestItemCarrinho:

    def setup_method(self) -> None:
        cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, cat)

    def test_cria_item_com_produto_e_quantidade(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.produto is self.notebook
        assert item.quantidade == 2

    def test_preco_no_momento_igual_preco_do_produto(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.preco_no_momento == 3500.0

    def test_preco_no_momento_congela_preco_da_criacao(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        self.notebook.alterar_preco(4000.0)
        assert item.preco_no_momento == 3500.0

    def test_calcular_subtotal(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.calcular_subtotal() == 7000.0

    def test_subtotal_com_quantidade_um(self) -> None:
        item = ItemCarrinho(self.notebook, 1)
        assert item.calcular_subtotal() == 3500.0
```

Repare no teste `test_preco_no_momento_congela_preco_da_criacao`. Ele verifica justamente a decisão de projeto que discutimos: mesmo que o preço do produto mude, o item mantém o valor original.

```bash
pytest
```

**18 testes passando.**

---

## Passo 9 — Carrinho

A classe que coordena os itens. Observe a composição: o Carrinho cria e gerencia Itens, e um Item não existe sem um Carrinho.

### `ecommerce/carrinho.py`

```python linenums="1"
from ecommerce.item_carrinho import ItemCarrinho


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


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    mouse = Produto("Mouse", 150.0, 20, cat)

    carrinho = Carrinho()
    carrinho.adicionar_item(notebook, 1)
    carrinho.adicionar_item(mouse, 2)

    print(f"Itens no carrinho: {carrinho.quantidade_itens()}")
    print(f"Total: R$ {carrinho.calcular_total():.2f}")
```

Observe que `calcular_total` delega o cálculo de cada item para o próprio `ItemCarrinho`. O Carrinho apenas soma os subtotais. Essa é a aplicação prática da pergunta "quem é responsável por isso?".

### `tests/test_carrinho.py`

```python linenums="1"
from ecommerce.categoria import Categoria
from ecommerce.produto import Produto
from ecommerce.carrinho import Carrinho


class TestCarrinho:

    def setup_method(self) -> None:
        cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, cat)
        self.mouse = Produto("Mouse", 150.0, 20, cat)

    def test_carrinho_vazio(self) -> None:
        carrinho = Carrinho()
        assert carrinho.quantidade_itens() == 0

    def test_adicionar_item_ao_carrinho(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        assert carrinho.quantidade_itens() == 1

    def test_adicionar_multiplos_itens(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        assert carrinho.quantidade_itens() == 2

    def test_remover_item_do_carrinho(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        carrinho.remover_item(self.notebook)
        assert carrinho.quantidade_itens() == 1

    def test_calcular_total_com_um_item(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 2)
        assert carrinho.calcular_total() == 7000.0

    def test_calcular_total_com_varios_itens(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 3)
        assert carrinho.calcular_total() == 3950.0

    def test_calcular_total_carrinho_vazio(self) -> None:
        carrinho = Carrinho()
        assert carrinho.calcular_total() == 0.0

    def test_adicionar_quantidade_invalida(self) -> None:
        carrinho = Carrinho()
        try:
            carrinho.adicionar_item(self.notebook, 0)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass
```

```bash
pytest
```

**26 testes passando.**

---

## Passo 10 — Rodando tudo

Para executar todos os testes:

```bash
cd code/modulo1/capitulo4
source .venv/bin/activate
pytest -v
```

A opção `-v` (verbose) exibe o nome de cada teste individualmente.

Para testar manualmente qualquer classe:

```bash
python -m ecommerce.produto
python -m ecommerce.carrinho
```

---

## Passo 11 — Exercícios

### Nível 1 — Fixação

1. Adicione um atributo `descricao: str` à classe `Produto` e crie um teste que verifique seu valor.
2. No teste `test_carrinho_vazio`, altere a asserção para que o teste falhe propositalmente. Execute `pytest` e observe a mensagem de erro.

### Nível 2 — Aplicação

3. Implemente um método `esvaziar()` na classe `Carrinho` que remove todos os itens. Crie o teste correspondente.
4. Crie um método `aumentar_preco(self, percentual: float)` em `Produto`. Diferente de `aplicar_desconto`, ele deve aumentar o preço. Qual validação faz sentido aqui?

### Nível 3 — Desafio

5. No sistema financeiro, implemente uma classe `Categoria` e uma classe `Lancamento`, onde cada lançamento possui uma categoria. Crie os testes para validar o relacionamento entre elas.

---

## Aplicando ao Projeto Financeiro

Assim como criamos `Categoria` e `Produto` no E-Commerce, crie as primeiras classes do sistema financeiro:

- `Conta` — nome, saldo
- `Categoria` — nome (gastos como "Alimentação", "Transporte")
- `Lancamento` — descrição, valor, data, categoria

Crie os arquivos, os testes e verifique se tudo passa. Use a mesma estrutura de pacote (`ecommerce/` → `financeiro/`).

---

## Resumo do que aprendemos

| Conceito | Onde aplicamos |
|----------|----------------|
| Classe simples | `Categoria` |
| Objeto rico | `Produto` com validações e métodos de negócio |
| Associação | `Produto → Categoria`, `ItemCarrinho → Produto` |
| Composição | `Carrinho *→ ItemCarrinho` |
| Delegação | `Carrinho.calcular_total` chama `ItemCarrinho.calcular_subtotal` |
| Testes automatizados | `tests/test_*.py` com pytest |
| Invariante | Preço nunca negativo, quantidade sempre positiva |

---

## O que vem a seguir

Agora temos um catálogo de produtos, clientes e um carrinho funcional. Mas o sistema ainda não permite finalizar uma compra. No próximo módulo evoluiremos o domínio para incluir pedidos, estados e regras de negócio mais complexas.
