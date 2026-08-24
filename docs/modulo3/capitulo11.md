# Capítulo 11 — Frete

!!! info "Situação da Empresa"

    Desconto e cupom resolvidos. Só que agora é o cliente quem reclama: "eu não sei quanto vou pagar de frete até chegar na última tela da compra. Isso me faz desistir." O gerente concorda — quer que o frete apareça já no resumo do pedido, e que compras acima de um certo valor tenham frete grátis.

Frete é um problema diferente de desconto — não reduz o valor dos produtos, soma um custo por cima. Mas repare na forma da pergunta que o gerente fez: "depende de quanto o cliente está comprando". É a mesma forma do problema que já resolvemos duas vezes neste módulo.

---

!!! note "🔍 Análise — é o mesmo problema de novo?"

    Antes de escrever qualquer código, vale comparar:

    - **Desconto por tipo de cliente**: várias formas de calcular um valor a partir do total, escolhidas em tempo de execução.
    - **Cupom**: idem, com uma camada extra de validade.
    - **Frete**: fixo, ou grátis a partir de um valor mínimo, ou (no futuro) por peso, por região, por transportadora.

    As três coisas têm o mesmo formato: uma regra de cálculo que varia, plugada em um ponto fixo do fluxo de compra. Isso é exatamente o que `EstrategiaDesconto` resolveu para desconto. Não existe motivo para inventar uma solução diferente para frete — vamos aplicar o mesmo padrão.

---

## Modelando o frete

```python title="ecommerce/estrategia_frete.py" linenums="1"
from abc import ABC, abstractmethod


class EstrategiaFrete(ABC):

    @abstractmethod
    def calcular(self, total_pedido: float) -> float:
        ...


class FreteFixo(EstrategiaFrete):

    def __init__(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("Valor do frete nao pode ser negativo")
        self._valor = valor

    def calcular(self, total_pedido: float) -> float:
        return self._valor


class FreteGratisAcimaDe(EstrategiaFrete):

    def __init__(self, valor_minimo: float, valor_frete: float) -> None:
        self._valor_minimo = valor_minimo
        self._valor_frete = valor_frete

    def calcular(self, total_pedido: float) -> float:
        if total_pedido >= self._valor_minimo:
            return 0.0
        return self._valor_frete
```

`EstrategiaFrete` é uma interface nova — não a mesma `EstrategiaDesconto` reaproveitada. Desconto e frete respondem perguntas diferentes (um reduz o total, o outro soma um custo), então merecem contratos diferentes, mesmo seguindo a mesma ideia estrutural. Reaproveitar por reaproveitar, quando os conceitos não são o mesmo conceito, é tão problemático quanto duplicar código à toa.

---

## Juntando desconto e frete no fechamento do pedido

```python title="ecommerce/pedido.py" linenums="1" hl_lines="1 7-15"
from ecommerce.estrategia_frete import EstrategiaFrete

# ... outros imports ...

class Pedido:

    def calcular_valor_final(
        self,
        estrategia_desconto: EstrategiaDesconto | None = None,
        estrategia_frete: EstrategiaFrete | None = None,
    ) -> float:
        total = self.calcular_total(estrategia_desconto)
        if estrategia_frete is None:
            return total
        return total + estrategia_frete.calcular(total)

    # ... demais métodos ...
```

`calcular_valor_final` combina duas estratégias independentes — desconto e frete — sem que uma precise saber da existência da outra. `calcular_total` continua exatamente como estava, então nada que já dependia dele (como `confirmar_pagamento`) precisou mudar.

```python
pedido.calcular_valor_final()
# só os produtos, sem desconto nem frete

pedido.calcular_valor_final(estrategia_frete=FreteFixo(25.0))
# produtos + frete fixo

pedido.calcular_valor_final(
    estrategia_desconto=DescontoPercentual(10),
    estrategia_frete=FreteGratisAcimaDe(valor_minimo=1000.0, valor_frete=40.0),
)
# produtos com 10% de desconto, frete grátis se o total já descontado passar de R$ 1000
```

---

## Testes

```python title="tests/test_estrategia_frete.py" linenums="1"
import pytest
from ecommerce.estrategia_frete import FreteFixo, FreteGratisAcimaDe


class TestFreteFixo:

    def test_calcula_valor_fixo(self) -> None:
        estrategia = FreteFixo(25.0)
        assert estrategia.calcular(100.0) == 25.0
        assert estrategia.calcular(1000.0) == 25.0

    def test_valor_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            FreteFixo(-10.0)


class TestFreteGratisAcimaDe:

    def test_frete_gratis_quando_atinge_o_minimo(self) -> None:
        estrategia = FreteGratisAcimaDe(valor_minimo=200.0, valor_frete=30.0)
        assert estrategia.calcular(200.0) == 0.0
        assert estrategia.calcular(500.0) == 0.0

    def test_cobra_frete_abaixo_do_minimo(self) -> None:
        estrategia = FreteGratisAcimaDe(valor_minimo=200.0, valor_frete=30.0)
        assert estrategia.calcular(150.0) == 30.0
```

```python title="tests/test_pedido.py" linenums="1"
def test_calcular_valor_final_sem_frete(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_valor_final() == 3500.0

def test_calcular_valor_final_com_frete_fixo(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    assert pedido.calcular_valor_final(estrategia_frete=FreteFixo(25.0)) == 3525.0

def test_calcular_valor_final_com_desconto_e_frete(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    valor_final = pedido.calcular_valor_final(
        estrategia_desconto=DescontoPercentual(10),
        estrategia_frete=FreteFixo(25.0),
    )
    assert valor_final == (3500.0 * 0.90) + 25.0

def test_calcular_valor_final_frete_gratis_acima_do_minimo(self) -> None:
    pedido = Pedido()
    pedido.adicionar_item(self.notebook, 1)
    estrategia_frete = FreteGratisAcimaDe(valor_minimo=1000.0, valor_frete=40.0)
    assert pedido.calcular_valor_final(estrategia_frete=estrategia_frete) == 3500.0
```

```bash
$ pytest tests/
```

??? tip "88 testes passando"

    Oito testes novos fecham o módulo: quatro para as estratégias de frete isoladas, quatro para a combinação de desconto e frete em `calcular_valor_final`.

---

## 🧩 Aplicando ao Projeto Financeiro

Feche o módulo aplicando o padrão pela terceira vez: **correções monetárias** (IPCA, INPC, Selic) também são regras de cálculo intercambiáveis, aplicadas sobre um valor, escolhidas em tempo de execução — exatamente a forma que você já viu com rendimento e com juros.

Modele uma interface para correção monetária e pelo menos duas implementações. Depois, dê um passo atrás: olhe para as três interfaces que você criou neste módulo (rendimento, juros, correção monetária). Elas deveriam ser três interfaces separadas, ou alguma delas é, na verdade, o mesmo conceito com nomes diferentes? Não existe resposta errada aqui — o que importa é que a decisão seja consciente.

---

## 📌 Resumo do módulo

- **Strategy** resolveu três problemas de negócio diferentes (desconto por cliente, cupom, frete) com a mesma forma estrutural: uma interface, várias implementações, escolhidas em tempo de execução
- **Interface** (`ABC` + `@abstractmethod`) é o contrato que torna isso possível — quem usa a estratégia não precisa conhecer suas implementações
- **Open/Closed**: em nenhum dos três casos precisamos editar código que já funcionava para adicionar uma nova regra
- Nem tudo que "parece parecido" deve reaproveitar a mesma interface — `EstrategiaDesconto` e `EstrategiaFrete` são conceitos diferentes, mesmo seguindo a mesma ideia estrutural
- Reaproveitar por composição (como `Cupom` reaproveitou `EstrategiaDesconto`) evita duplicar lógica sem forçar heranças artificiais

## O que mudou no sistema

- ✔ `EstrategiaDesconto`, `SemDesconto`, `DescontoPercentual` existem
- ✔ `Cupom` existe, com validade e regra de desconto
- ✔ `EstrategiaFrete`, `FreteFixo`, `FreteGratisAcimaDe` existem
- ✔ `Pedido.calcular_valor_final` combina desconto e frete
- ❌ Frete ainda não está integrado ao pagamento (`confirmar_pagamento` continua cobrando só os produtos)
- ❌ Não é possível combinar cupom com desconto por tipo de cliente no mesmo pedido
- ❌ Formas de pagamento, meios de entrega e criação de objetos em geral ainda não têm um padrão — é o que vem no Módulo 4

## O que vem a seguir

O sistema já resolve descontos, cupons e frete sem condicionais espalhados pelo código. Antes de seguir para o Módulo 4, é hora de parar de novo e consolidar: [entregue a segunda parte do seu Projeto Financeiro](entrega.md).

No Módulo 4, vamos olhar para outro tipo de problema: como criar objetos — pagamentos, entregas, notificações — sem espalhar `if/elif` também na hora de decidir *o que* instanciar.
