# Capítulo 10 — Cupom

!!! info "Situação da Empresa"

    Descontos por tipo de cliente estão resolvidos — e resolvidos de um jeito que aceita novos tipos sem dor. O gerente gostou tanto que voltou com outra ideia: "quero lançar cupons promocionais. O cliente digita um código na hora de fechar a compra e ganha um desconto. E cada cupom tem uma validade — depois de um tempo, ele para de funcionar."

Um cupom parece, à primeira vista, só mais um tipo de desconto. Mas ele carrega algo que os descontos por tipo de cliente não tinham: um **código**, uma **validade**, e a possibilidade de **se tornar inválido**. Isso é informação suficiente pra virar uma entidade própria — não apenas mais uma estratégia.

---

## Modelando o Cupom

Um cupom guarda um código, uma data de validade e a regra de desconto que ele aplica. Ele não recalcula descontos do zero — reaproveita a mesma interface `EstrategiaDesconto` do capítulo anterior:

```python title="ecommerce/cupom.py" linenums="1"
from datetime import date

from ecommerce.estrategia_desconto import EstrategiaDesconto


class Cupom:

    def __init__(self, codigo: str, validade: date, estrategia_desconto: EstrategiaDesconto) -> None:
        self._codigo = codigo
        self._validade = validade
        self._estrategia_desconto = estrategia_desconto

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def validade(self) -> date:
        return self._validade

    def esta_valido(self, hoje: date | None = None) -> bool:
        hoje = hoje if hoje is not None else date.today()
        return hoje <= self._validade

    def calcular_desconto(self, total: float) -> float:
        if not self.esta_valido():
            raise ValueError(f"Cupom {self._codigo} esta expirado")
        return self._estrategia_desconto.calcular(total)
```

`Cupom` não reimplementa o cálculo de desconto — ele delega para uma `EstrategiaDesconto` que já conhecemos. Isso é composição, o mesmo princípio que já apareceu com `Carrinho` e `ItemCarrinho`: `Cupom` sabe *quando* pode aplicar um desconto (checando a validade), a estratégia sabe *como* calcular esse desconto.

!!! warning "⚠️ Erro comum — colocar a lógica de cupom dentro de Produto"

    Pode parecer natural perguntar "o produto tem cupom aplicado?" e guardar essa informação em `Produto`. Não faça isso.

    `Produto` representa um item do catálogo — ele existe independentemente de qualquer compra. `Cupom` só faz sentido no contexto de uma compra específica, de um cliente específico, em um momento específico. Se `Produto` soubesse sobre cupons, um desconto aplicado numa compra vazaria para todas as outras — exatamente o problema que já vimos com `aplicar_desconto` no Capítulo 8.

    Quem usa o cupom é o `Pedido`, não o `Produto`.

---

## Pedido aplica o cupom

```python title="ecommerce/pedido.py" linenums="1" hl_lines="1 9 13-15 19-22 26-27"
from ecommerce.cupom import Cupom

# ... outros imports ...

class Pedido:

    def __init__(self) -> None:
        # ... outros atributos ...
        self._cupom: Cupom | None = None

    # ... outras properties ...

    @property
    def cupom(self) -> Cupom | None:
        return self._cupom

    # ... adicionar_item ...

    def aplicar_cupom(self, cupom: Cupom) -> None:
        if not cupom.esta_valido():
            raise ValueError(f"Cupom {cupom.codigo} esta expirado")
        self._cupom = cupom

    def calcular_total(self, estrategia_desconto: EstrategiaDesconto | None = None) -> float:
        total = sum(item.calcular_subtotal() for item in self._itens)
        if self._cupom is not None:
            return self._cupom.calcular_desconto(total)
        if estrategia_desconto is None:
            return total
        return estrategia_desconto.calcular(total)

    # ... demais métodos ...
```

`confirmar_pagamento` não precisou mudar: ele já chama `self.calcular_total()`, e agora `calcular_total` sabe verificar sozinho se existe um cupom aplicado.

---

!!! info "🏗️ Decisão de Projeto — por que o cupom vira um atributo, se a estratégia de desconto era um parâmetro?"

    No Capítulo 9, decidimos que a estratégia de desconto seria passada como parâmetro, não guardada no pedido — porque o desconto por tipo de cliente é recalculado a cada consulta, sem estado persistente.

    Um cupom é diferente: uma vez aplicado, ele precisa **permanecer** aplicado até o pedido ser pago — inclusive porque `confirmar_pagamento` chama `calcular_total()` internamente, sem receber parâmetro nenhum. Se o cupom fosse só um parâmetro, precisaríamos passá-lo de novo em cada chamada, e correríamos o risco de esquecer — cobrando o cliente sem o desconto que ele já viu na tela.

    Por isso `_cupom` é um atributo: ele representa uma decisão já tomada sobre *este* pedido, não um cálculo pontual. `aplicar_cupom` valida a validade uma vez, no momento da aplicação — se o cupom expirar entre a aplicação e o pagamento, o desconto já garantido continua valendo.

---

## Testes

```python title="tests/test_cupom.py" linenums="1"
from datetime import date, timedelta

import pytest
from ecommerce.cupom import Cupom
from ecommerce.estrategia_desconto import DescontoPercentual


class TestCupom:

    def setup_method(self) -> None:
        self.amanha = date.today() + timedelta(days=1)
        self.ontem = date.today() - timedelta(days=1)

    def test_cupom_valido(self) -> None:
        cupom = Cupom("BEMVINDO10", self.amanha, DescontoPercentual(10))
        assert cupom.esta_valido() is True

    def test_cupom_expirado(self) -> None:
        cupom = Cupom("PROMOANTIGA", self.ontem, DescontoPercentual(10))
        assert cupom.esta_valido() is False

    def test_calcular_desconto_cupom_valido(self) -> None:
        cupom = Cupom("BEMVINDO10", self.amanha, DescontoPercentual(10))
        assert cupom.calcular_desconto(1000.0) == 900.0

    def test_calcular_desconto_cupom_expirado_lanca_erro(self) -> None:
        cupom = Cupom("PROMOANTIGA", self.ontem, DescontoPercentual(10))
        with pytest.raises(ValueError):
            cupom.calcular_desconto(1000.0)
```

```python title="tests/test_pedido.py" linenums="1"
def test_aplicar_cupom_valido(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    cupom = Cupom("BEMVINDO10", date.today() + timedelta(days=1), DescontoPercentual(10))
    pedido.aplicar_cupom(cupom)
    assert pedido.cupom is cupom
    assert pedido.calcular_total() == 3500.0 * 0.90

def test_aplicar_cupom_expirado_lanca_erro(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    cupom = Cupom("PROMOANTIGA", date.today() - timedelta(days=1), DescontoPercentual(10))
    with pytest.raises(ValueError):
        pedido.aplicar_cupom(cupom)

def test_pagamento_reflete_desconto_do_cupom(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    cupom = Cupom("BEMVINDO10", date.today() + timedelta(days=1), DescontoPercentual(10))
    pedido.aplicar_cupom(cupom)
    pedido.confirmar_pagamento()
    assert pedido.pagamento.valor == 3500.0 * 0.90
```

```bash
$ pytest tests/
```

??? tip "80 testes passando"

    Sete testes novos: quatro para `Cupom` isoladamente, três para a integração de `Cupom` com `Pedido` — incluindo a garantia de que o pagamento reflete o desconto do cupom.

---

## 🧩 Aplicando ao Projeto Financeiro

No seu sistema financeiro, pense em **tipos de juros**: juros simples e juros compostos calculam o valor final de formas diferentes, a partir dos mesmos dados de entrada (capital, taxa, tempo).

Assim como `Cupom` reaproveitou `EstrategiaDesconto` em vez de recalcular tudo do zero, veja se sua estratégia de rendimento do capítulo anterior pode ser reaproveitada aqui — ou se juros simples/compostos merecem sua própria interface. Documente sua decisão: reaproveitar uma interface existente por semelhança real de comportamento é diferente de forçar um encaixe só para não criar uma classe nova.

---

## 📌 Resumo

- **Cupom** é uma entidade própria — tem identidade (código), validade e uma regra de desconto — não apenas mais uma estratégia
- `Cupom` reaproveita `EstrategiaDesconto` por composição, em vez de duplicar a lógica de cálculo
- `Pedido` guarda o cupom aplicado como atributo, ao contrário da estratégia de desconto por tipo de cliente (que continua sendo passada por parâmetro) — decisão justificada pela necessidade do desconto persistir até o pagamento
- `Produto` nunca conhece `Cupom` — quem aplica é o `Pedido`

## O que mudou no sistema

- ✔ `Cupom` existe, com código, validade e regra de desconto
- ✔ `Pedido.aplicar_cupom` valida a validade antes de aceitar o cupom
- ✔ O pagamento reflete o desconto do cupom aplicado
- ❌ Frete ainda não existe
- ❌ Não é possível combinar cupom com desconto por tipo de cliente

## O que vem a seguir

Desconto resolvido, cupom resolvido. Mas o cliente ainda não sabe quanto vai pagar de frete até finalizar a compra. No próximo capítulo, vamos ver a mesma ideia de Strategy resolver um problema completamente diferente — e fechar o módulo.
