# Capítulo 12 — Formas de pagamento e o problema da criação

!!! info "Situação da Empresa"

    O Módulo 3 fechou com o valor do pedido sob controle: desconto por tipo de cliente, cupom e frete, tudo sem `if/elif` espalhado. O gerente aprovou e, na mesma conversa, trouxe a próxima demanda.

    "Só aceitar um jeito de pagar está nos custando venda. Quero Pix, quero boleto, quero cartão de crédito parcelado." Três formas de pagamento — e cada uma funciona de um jeito diferente.

Hoje o pagamento do nosso sistema é uma coisa só. `Pedido.confirmar_pagamento()` cria um `Pagamento`, chama `confirmar()` e pronto. Não existe "tipo" de pagamento porque só existe um tipo.

O que o gerente está pedindo não é mudar o cálculo do valor — isso já está resolvido. É mudar **qual objeto de pagamento é criado**. Um Pix compensa na hora. Um boleto tem linha digitável e vencimento, e pode ser recusado se pagar depois do prazo. Um cartão tem bandeira e número de parcelas. São três classes diferentes, com dados diferentes e regras de confirmação diferentes.

E aí aparece uma pergunta nova, que o curso ainda não enfrentou: **quem decide qual dessas classes instanciar?**

---

## O pagamento que já temos

Desde o Módulo 2, `Pagamento` é uma classe concreta única, e `Pedido` a cria diretamente:

```python title="ecommerce/pedido.py"
def confirmar_pagamento(self) -> None:
    self._transicionar(StatusPedido.PAGO)
    self._pagamento = Pagamento(self, self.calcular_total())
    self._pagamento.confirmar()
```

Funciona enquanto existe um jeito só de pagar. No momento em que existem três, `Pedido` precisa escolher.

---

## Uma primeira tentativa

O caminho mais direto é perguntar, dentro de `confirmar_pagamento`, qual forma o cliente escolheu:

```python title="ecommerce/pedido.py" linenums="1" hl_lines="3-14"
def confirmar_pagamento(self, forma: str, **dados) -> None:
    self._transicionar(StatusPedido.PAGO)
    valor = self.calcular_total()
    if forma == "pix":
        pagamento = PagamentoPix(self, valor, chave=dados["chave"])
    elif forma == "boleto":
        pagamento = PagamentoBoleto(
            self, valor, linha_digitavel=dados["linha_digitavel"], vencimento=dados["vencimento"]
        )
    elif forma == "cartao":
        pagamento = PagamentoCartao(
            self, valor, bandeira=dados["bandeira"], parcelas=dados["parcelas"]
        )
    else:
        raise ValueError(f"Forma desconhecida: {forma}")
    self._pagamento = pagamento
    self._pagamento.confirmar()
```

Os testes passam. O gerente fica feliz. Mas olhe para o que `Pedido` acabou de aprender.

!!! warning "⚠️ Erro comum — misturar "gerenciar o pedido" com "saber construir cada pagamento""

    `Pedido` deveria cuidar dos itens, do estado e do valor. Depois desse `if/elif`, ele também conhece:

    - que existe uma classe `PagamentoPix` e que ela precisa de uma `chave`;
    - que `PagamentoBoleto` precisa de `linha_digitavel` e `vencimento`;
    - que `PagamentoCartao` precisa de `bandeira` e `parcelas`.

    Cada forma de pagamento nova — PayPal, cripto, vale-presente — é mais um `elif` dentro de `Pedido`, mais um construtor que `Pedido` precisa conhecer, mais um teste de `Pedido` para escrever. A classe que representa "uma compra confirmada" vira o lugar que sabe montar **todos os meios de pagamento que a empresa já teve**.

    Não é um erro de sintaxe. É uma responsabilidade no lugar errado — o mesmo diagnóstico do Capítulo 8, agora sobre criação em vez de cálculo.

---

!!! tip "🧠 Pense antes de continuar"

    No Módulo 3, quando o `if/elif` era de **cálculo** (qual desconto aplicar), a saída foi transformar cada regra em um objeto — Strategy.

    Agora o `if/elif` é de **construção** (qual objeto criar). Strategy não resolve isso: o problema não é "como calcular", é "o que instanciar". Que peça do sistema deveria ter a responsabilidade de, dada uma forma de pagamento, devolver o objeto de pagamento certo, já montado?

---

!!! important "💡 Conceito — Factory"

    Uma *factory* (fábrica) é uma peça cuja única responsabilidade é **criar objetos**. Quem precisa de um objeto pede à factory e recebe pronto, sem conhecer a classe concreta nem seu construtor.

    A forma mais simples é a **Simple Factory**: uma classe (ou função) com um método que recebe algum identificador — aqui, a forma de pagamento — e concentra num único lugar a decisão de qual classe instanciar. Não é um dos padrões do catálogo clássico (GoF); é o primeiro passo, e resolve a maior parte da dor com o mínimo de estrutura.

---

## Modelando as formas de pagamento

Antes da factory, precisamos das classes que ela vai criar. `Pagamento` deixa de ser concreta e vira o **contrato** comum:

```python title="ecommerce/pagamento.py" linenums="1"
from abc import ABC, abstractmethod
from datetime import date

from ecommerce.situacao_pagamento import SituacaoPagamento


class Pagamento(ABC):

    def __init__(self, pedido: "Pedido", valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        self._pedido = pedido
        self._valor = valor
        self._data = date.today()
        self._situacao = SituacaoPagamento.PENDENTE

    @property
    def situacao(self) -> SituacaoPagamento:
        return self._situacao

    @property
    def confirmado(self) -> bool:
        return self._situacao == SituacaoPagamento.CONFIRMADO

    def confirmar(self) -> None:
        if self._situacao == SituacaoPagamento.CONFIRMADO:
            raise ValueError("Pagamento ja foi confirmado")
        self._situacao = self._processar()

    @abstractmethod
    def _processar(self) -> SituacaoPagamento:
        ...
```

Duas decisões aqui merecem explicação.

Primeiro, `SituacaoPagamento` é um **enum** (`PENDENTE`, `CONFIRMADO`, `RECUSADO`), não um booleano `_confirmado`. Um boleto pode ser *recusado* por vencimento — são três estados possíveis, não dois. A regra vale desde o Módulo 2: estado do domínio se representa com enum, não com flags.

Segundo, `confirmar()` não é abstrato. Ele contém a parte **comum** a todas as formas — a checagem de "já confirmado" — e delega a parte que **varia** para `_processar()`, que cada forma implementa do seu jeito. Assim nenhuma subclasse repete o guard.

```python title="ecommerce/pagamento.py" linenums="1"
class PagamentoPix(Pagamento):

    def __init__(self, pedido: "Pedido", valor: float, chave: str) -> None:
        super().__init__(pedido, valor)
        self._chave = chave

    def _processar(self) -> SituacaoPagamento:
        # A compensacao do Pix e imediata: nada mais precisa acontecer.
        return SituacaoPagamento.CONFIRMADO


class PagamentoBoleto(Pagamento):

    def __init__(self, pedido, valor, linha_digitavel: str, vencimento: date) -> None:
        super().__init__(pedido, valor)
        self._linha_digitavel = linha_digitavel
        self._vencimento = vencimento

    def _processar(self) -> SituacaoPagamento:
        if date.today() > self._vencimento:
            return SituacaoPagamento.RECUSADO
        return SituacaoPagamento.CONFIRMADO


class PagamentoCartao(Pagamento):

    def __init__(self, pedido, valor, bandeira: str, parcelas: int = 1) -> None:
        super().__init__(pedido, valor)
        if parcelas < 1:
            raise ValueError("Numero de parcelas deve ser no minimo 1")
        self._bandeira = bandeira
        self._parcelas = parcelas

    def valor_parcela(self) -> float:
        return self._valor / self._parcelas

    def _processar(self) -> SituacaoPagamento:
        return SituacaoPagamento.CONFIRMADO
```

Cada forma carrega só os dados que fazem sentido para ela, e confirma do seu jeito. `PagamentoCartao` ainda ganhou um comportamento próprio — `valor_parcela()` — que não existiria numa classe genérica.

---

## A factory

Agora a peça que concentra a decisão de criação:

```python title="ecommerce/criador_pagamento.py" linenums="1"
from datetime import date, timedelta

from ecommerce.forma_pagamento import FormaPagamento
from ecommerce.pagamento import PagamentoBoleto, PagamentoCartao, PagamentoPix

CHAVE_PIX_DA_LOJA = "loja@ecommerce.com"


class CriadorPagamento:

    def criar(self, forma: FormaPagamento, pedido, valor: float, **dados) -> "Pagamento":
        if forma == FormaPagamento.PIX:
            return PagamentoPix(pedido, valor, chave=dados.get("chave", CHAVE_PIX_DA_LOJA))
        if forma == FormaPagamento.BOLETO:
            return PagamentoBoleto(
                pedido, valor,
                linha_digitavel=dados.get("linha_digitavel", "..."),
                vencimento=dados.get("vencimento", date.today() + timedelta(days=3)),
            )
        if forma == FormaPagamento.CARTAO_CREDITO:
            return PagamentoCartao(
                pedido, valor,
                bandeira=dados.get("bandeira", "VISA"),
                parcelas=dados.get("parcelas", 1),
            )
        raise ValueError(f"Forma de pagamento desconhecida: {forma}")
```

`FormaPagamento` é um enum (`PIX`, `BOLETO`, `CARTAO_CREDITO`) — o identificador que a factory usa para decidir. O `if/elif` **não sumiu**: ele foi para o lugar certo. A diferença é que agora existe **um único ponto** no sistema que conhece os construtores concretos, e esse ponto tem uma responsabilidade só: criar pagamento.

!!! warning "⚠️ Erro comum — a factory que faz mais do que criar"

    É tentador fazer a factory já chamar `pagamento.confirmar()` antes de devolver, "para adiantar". Não faça. A responsabilidade da factory termina quando o objeto está montado. Confirmar o pagamento é decisão de quem pediu — o `Pedido`. Uma factory que cria *e* executa regra de negócio volta a misturar responsabilidades, só que agora numa classe nova.

---

## Pedido delega para a factory

```python title="ecommerce/pedido.py" linenums="1" hl_lines="4 9-11"
class Pedido:

    def __init__(self) -> None:
        # ... outros atributos ...
        self._criador_pagamento = CriadorPagamento()

    def confirmar_pagamento(
        self, forma: FormaPagamento = FormaPagamento.PIX, **dados
    ) -> None:
        self._transicionar(StatusPedido.PAGO)
        self._pagamento = self._criador_pagamento.criar(
            forma, self, self.calcular_total(), **dados
        )
        self._pagamento.confirmar()
```

`Pedido` voltou a não conhecer nenhuma classe concreta de pagamento. Ele conhece a factory e a abstração `Pagamento`, nada mais. Adicionar "PayPal" amanhã é: criar `PagamentoPayPal`, adicionar um caso na factory, e escrever os testes da factory. Nenhuma linha de `Pedido` muda.

```python
pedido.confirmar_pagamento()                                  # Pix (padrão)
pedido.confirmar_pagamento(FormaPagamento.BOLETO)
pedido.confirmar_pagamento(FormaPagamento.CARTAO_CREDITO, bandeira="MASTERCARD", parcelas=3)
```

!!! info "🏗️ Decisão de Projeto — por que `Pedido` ainda cria a própria factory?"

    Repare em `self._criador_pagamento = CriadorPagamento()` dentro do `__init__`. `Pedido` não conhece mais as classes de pagamento, mas ainda instancia a factory por conta própria.

    Para este capítulo, tudo bem: o ganho principal — tirar o conhecimento das formas concretas de dentro do `Pedido` — já foi obtido. Mas isso ainda é um acoplamento: `Pedido` decide, sozinho, qual `CriadorPagamento` usar, e um teste de `Pedido` não tem como trocar a factory por uma versão de mentira. Guarde essa observação. Ela vai voltar no Capítulo 15.

---

## Testes

```python title="tests/test_criador_pagamento.py" linenums="1"
class TestCriadorPagamento:

    def setup_method(self) -> None:
        self.pedido = Pedido()
        self.pedido.adicionar_item(self.notebook, 1)
        self.criador = CriadorPagamento()

    def test_cria_pagamento_pix(self) -> None:
        pagamento = self.criador.criar(FormaPagamento.PIX, self.pedido, 3500.0)
        assert isinstance(pagamento, PagamentoPix)

    def test_cria_pagamento_cartao_com_parcelas(self) -> None:
        pagamento = self.criador.criar(
            FormaPagamento.CARTAO_CREDITO, self.pedido, 3600.0, parcelas=3
        )
        assert isinstance(pagamento, PagamentoCartao)
        assert pagamento.parcelas == 3

    def test_forma_desconhecida_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            self.criador.criar("pix", self.pedido, 3500.0)
```

```python title="tests/test_pagamento.py" linenums="1"
def test_pagamento_e_abstrato(self) -> None:
    with pytest.raises(TypeError):
        Pagamento(self.pedido, 3500.0)

def test_boleto_vencido_e_recusado(self) -> None:
    pag = PagamentoBoleto(
        self.pedido, 3500.0, linha_digitavel="123",
        vencimento=date.today() - timedelta(days=1),
    )
    pag.confirmar()
    assert pag.situacao == SituacaoPagamento.RECUSADO
```

```bash
$ pytest tests/
```

??? tip "99 testes passando"

    Onze testes novos: as três formas de pagamento isoladas (incluindo o boleto vencido e o parcelamento do cartão), a factory devolvendo a classe certa para cada `FormaPagamento`, o erro para forma desconhecida, e a integração com `Pedido.confirmar_pagamento`. Os testes que chamavam `confirmar_pagamento()` sem argumento continuam passando — Pix é o padrão.

---

## 🧩 Aplicando ao Projeto Financeiro

No seu sistema financeiro, os extratos chegam em formatos diferentes: um banco exporta **CSV**, outro exporta **OFX**, um terceiro só oferece **JSON** pela API. Cada formato precisa de um leitor próprio, que sabe interpretar aquela estrutura.

Se você for decidir o leitor com um `if extensao == ".csv": ... elif ...` dentro da classe que processa o extrato, cai exatamente no problema deste capítulo.

Não implemente a solução completa ainda. Modele a interface `Leitor` (um método que recebe um caminho de arquivo e devolve uma lista de lançamentos) e pelo menos duas implementações. Depois responda: quem, no seu projeto, deveria ter a responsabilidade de escolher o leitor certo a partir do arquivo?

---

## 📌 Resumo

- Decidir **qual objeto instanciar** é uma responsabilidade — e espalhar essa decisão com `if/elif` acopla quem cria a todas as classes concretas e seus construtores
- **Factory** é uma peça cuja única função é criar objetos; a **Simple Factory** concentra num método a decisão de qual classe instanciar
- `Pagamento` virou uma abstração; `PagamentoPix`, `PagamentoBoleto` e `PagamentoCartao` são as implementações, cada uma com seus dados e sua regra de confirmação
- `SituacaoPagamento` (enum) substituiu a flag booleana — um boleto pode ser recusado, não só confirmado
- `confirmar()` na classe base é um método-molde: guarda o comum, delega o que varia para `_processar()`
- A factory isola o `if/elif` num único ponto; `Pedido` volta a não conhecer nenhuma forma concreta

## O que mudou no sistema

- ✔ `Pagamento` é abstrato; `PagamentoPix` / `PagamentoBoleto` / `PagamentoCartao` existem
- ✔ `FormaPagamento` e `SituacaoPagamento` (enums) existem
- ✔ `CriadorPagamento` concentra a criação; `Pedido.confirmar_pagamento` aceita a forma
- ❌ `Pedido` ainda instancia a própria `CriadorPagamento`
- ❌ Meios de entrega e notificações ainda não existem

## O que vem a seguir

A factory resolveu a criação do pagamento porque a decisão cabe num `match` simples por enum. Mas nem toda escolha de criação é assim. No próximo capítulo, o pedido pago precisa ser **despachado** — e qual meio de entrega usar não depende de um enum, depende de *quem* está despachando. Uma factory central não vai dar conta: vamos precisar de **Factory Method**.
