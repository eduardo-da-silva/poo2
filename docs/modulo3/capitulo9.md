# Capítulo 9 — Strategy: desconto como objeto

!!! info "Situação da Empresa"

    A solução do capítulo anterior está no ar e funcionando: três tipos de desconto, um `if/elif` em `Pedido`. Só que, na mesma reunião em que aprovou a solução, o gerente já perguntou: "e quando eu quiser um quarto tipo de desconto? Vocês vão precisar mexer no sistema toda vez?"

    A resposta certa é não. E é isso que vamos resolver agora.

Vamos transformar cada regra de desconto em um **objeto**, seguindo um contrato comum. O nome desse padrão é **Strategy**: várias formas de resolver o mesmo problema, intercambiáveis, sem que quem usa precise saber qual delas está em ação.

---

## Modelando o contrato

Toda estratégia de desconto faz a mesma coisa: recebe um total e devolve um novo total, já com desconto aplicado. Isso é o suficiente para virar uma interface:

```python title="ecommerce/estrategia_desconto.py" linenums="1"
from abc import ABC, abstractmethod


class EstrategiaDesconto(ABC):

    @abstractmethod
    def calcular(self, total: float) -> float:
        ...


class SemDesconto(EstrategiaDesconto):

    def calcular(self, total: float) -> float:
        return total


class DescontoPercentual(EstrategiaDesconto):

    def __init__(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self._percentual = percentual

    def calcular(self, total: float) -> float:
        return total - (total * self._percentual / 100)
```

`EstrategiaDesconto` é a interface: uma classe abstrata (`ABC`) com um método (`calcular`) marcado como `@abstractmethod`. Ela não pode ser instanciada sozinha — só serve como contrato. `SemDesconto` e `DescontoPercentual` são implementações concretas desse contrato.

Repare que `DescontoPercentual` já resolve os três casos do capítulo anterior: `DescontoPercentual(15)` é o desconto VIP, `DescontoPercentual(10)` é o desconto de cliente frequente, `DescontoPercentual(20)` é o desconto de aniversário. Não precisamos de três classes — precisamos de uma classe reutilizável e de instâncias diferentes.

---

## Pedido aceita uma estratégia

`Pedido` não precisa mais saber os detalhes de cada desconto — só precisa saber que existe algo capaz de calcular um:

```python title="ecommerce/pedido.py" linenums="1" hl_lines="1 7-11"
from ecommerce.estrategia_desconto import EstrategiaDesconto

# ... outros imports ...

class Pedido:

    def calcular_total(self, estrategia_desconto: EstrategiaDesconto | None = None) -> float:
        total = sum(item.calcular_subtotal() for item in self._itens)
        if estrategia_desconto is None:
            return total
        return estrategia_desconto.calcular(total)

    # ... demais métodos ...
```

O `if/elif` sumiu. No lugar dele, uma pergunta simples: "existe uma estratégia? Se sim, pergunte a ela." `calcular_total()` continua funcionando sem argumento nenhum — todo o código que já chamava `pedido.calcular_total()` (inclusive `confirmar_pagamento`) continua funcionando exatamente como antes.

```python
pedido.calcular_total()                        # sem desconto, como sempre
pedido.calcular_total(DescontoPercentual(15))   # cliente VIP
pedido.calcular_total(SemDesconto())            # equivalente a não passar nada
```

---

!!! info "🏗️ Decisão de Projeto — por que a estratégia é um parâmetro, e não um atributo?"

    Poderíamos ter feito `pedido.estrategia_desconto = DescontoPercentual(15)` e deixado `calcular_total()` sem parâmetro nenhum, lendo esse atributo internamente.

    Optamos por passar a estratégia como **parâmetro do método** porque:

    1. O desconto depende de *quem está comprando agora*, não é uma propriedade permanente do pedido.
    2. Um parâmetro deixa explícito, no ponto de chamada, qual desconto está sendo aplicado — não é preciso ler o histórico do objeto para saber.
    3. Evita um pedido "esquecer" de limpar a estratégia antiga antes de calcular um novo total.

    Isso não é definitivo. No próximo capítulo, quando um `Cupom` puder ser aplicado a um pedido e precisar ser lembrado até o pagamento ser confirmado, essa decisão vai ser revisitada.

---

## Open/Closed: o que ganhamos

`Pedido` está **fechado para modificação** — não precisamos mais editar `calcular_total` para adicionar um novo tipo de desconto — e **aberto para extensão** — um novo desconto é uma nova classe (ou uma nova instância de `DescontoPercentual`) em algum outro lugar do código.

Se amanhã a empresa criar um desconto progressivo (quanto mais itens, maior o desconto), isso vira uma nova classe:

```python
class DescontoProgressivo(EstrategiaDesconto):

    def __init__(self, quantidade_itens: int) -> None:
        self._quantidade_itens = quantidade_itens

    def calcular(self, total: float) -> float:
        if self._quantidade_itens >= 10:
            return total * 0.80
        if self._quantidade_itens >= 5:
            return total * 0.90
        return total
```

Nenhuma linha de `Pedido` precisa mudar para isso funcionar. Esse é o ganho prático de uma interface: o código que já existe e já foi testado permanece intocado.

---

## Testes

```python title="tests/test_estrategia_desconto.py" linenums="1"
import pytest
from ecommerce.estrategia_desconto import DescontoPercentual, SemDesconto


class TestSemDesconto:

    def test_nao_altera_o_total(self) -> None:
        estrategia = SemDesconto()
        assert estrategia.calcular(1000.0) == 1000.0


class TestDescontoPercentual:

    def test_calcula_desconto_de_dez_por_cento(self) -> None:
        estrategia = DescontoPercentual(10)
        assert estrategia.calcular(1000.0) == 900.0

    def test_calcula_desconto_de_cem_por_cento(self) -> None:
        estrategia = DescontoPercentual(100)
        assert estrategia.calcular(1000.0) == 0.0

    def test_percentual_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            DescontoPercentual(-1)

    def test_percentual_acima_de_cem_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            DescontoPercentual(101)
```

```python title="tests/test_pedido.py" linenums="1"
def test_calcular_total_sem_estrategia(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total() == 3500.0

def test_calcular_total_com_estrategia_sem_desconto(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total(SemDesconto()) == 3500.0

def test_calcular_total_com_desconto_percentual(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_total(DescontoPercentual(15)) == 3500.0 * 0.85
```

```bash
$ pytest tests/
```

??? tip "73 testes passando"

    Os testes do `if/elif` do capítulo anterior foram substituídos pelos testes de `EstrategiaDesconto`. O comportamento observável não mudou — os mesmos três descontos continuam funcionando — só a forma como o código chega até eles.

---

## 🧩 Aplicando ao Projeto Financeiro

No capítulo anterior você identificou onde, no seu projeto, o cálculo de rendimento cresce como uma cadeia de condicionais. Agora é a hora de aplicar a mesma ideia.

Crie uma interface (`EstrategiaRendimento` ou nome equivalente) com um método que calcule o valor rendido a partir de um valor aplicado. Implemente pelo menos duas estratégias concretas — poupança e CDB pré-fixado são um bom ponto de partida. Decida: onde essa estratégia vai ser usada? Uma `Aplicacao` guarda a estratégia como atributo, ou ela é passada como parâmetro na hora de calcular o rendimento?

---

## 📌 Resumo

- **Strategy** transforma cada regra de negócio intercambiável em uma classe própria, todas cumprindo o mesmo contrato
- `EstrategiaDesconto` é uma interface (`ABC` + `@abstractmethod`); `SemDesconto` e `DescontoPercentual` são implementações concretas
- `Pedido.calcular_total` recebe a estratégia como parâmetro — o pedido não precisa mais conhecer os detalhes de cada tipo de desconto
- **Open/Closed**: um novo desconto é código novo, não uma edição em código que já funciona

## O que mudou no sistema

- ✔ `EstrategiaDesconto`, `SemDesconto` e `DescontoPercentual` existem
- ✔ `Pedido.calcular_total` aceita uma estratégia opcional
- ✔ Adicionar um novo tipo de desconto não exige mais editar `Pedido`
- ❌ Cupons ainda não existem
- ❌ Frete ainda não existe

## O que vem a seguir

Descontos por tipo de cliente resolvidos. Mas o gerente já está de volta: agora ele quer lançar **cupons** — códigos que o cliente digita na hora de fechar a compra. No próximo capítulo, vamos ver `Cupom` usar exatamente a mesma interface que acabamos de criar.
