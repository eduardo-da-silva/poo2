# Capítulo 13 — Meios de entrega: Factory Method

!!! info "Situação da Empresa"

    Pagamento resolvido, com espaço para novas formas sem dor. O gerente já está na próxima etapa do fluxo: "pedido pago é pedido que precisa sair para entrega. Hoje a gente só usa os Correios. Mas abrimos um centro de distribuição no Sul, e de lá sai por uma transportadora parceira, que é mais barata na região."

    Ou seja: o mesmo pedido pode ser despachado de lugares diferentes, e cada lugar usa um meio de entrega diferente.

Cada meio de entrega produz um objeto com informações próprias: um **código de rastreio** e um **prazo estimado**. Os Correios têm PAC e SEDEX, com prazos diferentes. A transportadora parceira tem o nome dela e um prazo próprio. Precisamos criar o objeto de entrega certo no momento do despacho.

Parece o problema do capítulo anterior. Mas tem uma diferença que muda a solução.

---

!!! note "🔍 Análise — isto não é `EstrategiaFrete` de novo?"

    No Capítulo 11 criamos `EstrategiaFrete`, que calcula **quanto custa** o frete: `FreteFixo`, `FreteGratisAcimaDe`. Agora estamos falando de **meio de entrega**. São a mesma coisa?

    | | `EstrategiaFrete` (Cap. 11) | `Entrega` / meio de entrega (agora) |
    |---|---|---|
    | Responde | Quanto o cliente paga de frete | Como o pedido chega até o cliente |
    | Quando entra | No cálculo do valor final, antes de fechar | No despacho, depois do pagamento |
    | Produz | Um número (custo) | Um objeto com rastreio e prazo |
    | Vive | Só durante o cálculo | Fica guardado no pedido |

    São dois conceitos diferentes que por acaso aparecem perto um do outro. `EstrategiaFrete` continua existindo e fazendo o que sempre fez. `Entrega` é território novo.

---

## Por que a Simple Factory não basta aqui

No capítulo anterior, `CriadorPagamento` funcionou porque a decisão cabia num `match` por enum: recebeu `FormaPagamento.PIX`, devolveu `PagamentoPix`. Um único ponto decide, e está resolvido.

Tente aplicar a mesma ideia à entrega:

```python
class CriadorEntrega:
    def criar(self, origem: str, pedido) -> Entrega:
        if origem == "loja_central":
            return EntregaCorreios(pedido, gerar_codigo(), modalidade="SEDEX")
        elif origem == "centro_sul":
            return EntregaTransportadora(pedido, gerar_codigo(), transportadora="Transportadora Sul")
        elif origem == "marketplace":
            ...  # regra do parceiro
```

Repare no que esse `CriadorEntrega` precisa saber: a regra de cada origem de despacho. Que a loja central usa SEDEX. Que o centro Sul usa a Transportadora Sul. Quando abrir um segundo centro regional, ou entrar um parceiro de marketplace com regra própria, é esse `if/elif` que cresce — e ele mistura, num lugar só, o conhecimento de *todas as origens de despacho da empresa*.

A diferença em relação ao pagamento: lá, a variação era **um dado** (a forma que o cliente escolheu). Aqui, a variação é **quem está despachando** — e cada origem de despacho é, ela mesma, uma parte do sistema com comportamento próprio.

---

!!! important "💡 Conceito — Factory Method"

    Quando *quem cria* já é uma família de classes com comportamento próprio, a decisão de qual objeto instanciar pode morar **dentro de cada uma dessas classes**, em vez de num `if/elif` central.

    O **Factory Method** é isto: uma classe base define um método de criação abstrato (`criar_entrega`) e usa esse método no seu fluxo, sem saber qual classe concreta vai voltar. Cada subclasse implementa o método do seu jeito. Adicionar uma nova variante é criar uma nova subclasse — não editar código existente.

---

## Modelando a entrega

Primeiro o produto que vai ser criado. `Entrega` é o contrato; o que varia é o prazo:

```python title="ecommerce/entrega.py" linenums="1"
from abc import ABC, abstractmethod


class Entrega(ABC):

    def __init__(self, pedido: "Pedido", codigo_rastreio: str) -> None:
        self._pedido = pedido
        self._codigo_rastreio = codigo_rastreio

    @property
    def codigo_rastreio(self) -> str:
        return self._codigo_rastreio

    @abstractmethod
    def prazo_estimado(self) -> int:
        """Numero de dias uteis previstos ate a entrega."""
        ...

    def etiqueta(self) -> str:
        return (
            f"{type(self).__name__} | rastreio {self._codigo_rastreio} "
            f"| prazo {self.prazo_estimado()} dias uteis"
        )


class EntregaCorreios(Entrega):

    def __init__(self, pedido, codigo_rastreio: str, modalidade: str = "PAC") -> None:
        super().__init__(pedido, codigo_rastreio)
        self._modalidade = modalidade

    def prazo_estimado(self) -> int:
        return 3 if self._modalidade == "SEDEX" else 8


class EntregaTransportadora(Entrega):

    def __init__(self, pedido, codigo_rastreio: str, transportadora: str) -> None:
        super().__init__(pedido, codigo_rastreio)
        self._transportadora = transportadora

    def prazo_estimado(self) -> int:
        return 5
```

`etiqueta()` fica na base porque é igual para todo mundo — muda só o `prazo_estimado()`, que cada subclasse responde do seu jeito. Mesma ideia do `confirmar()` de `Pagamento` no capítulo anterior.

---

## O Expedidor e o factory method

```python title="ecommerce/expedidor.py" linenums="1"
from abc import ABC, abstractmethod

from ecommerce.entrega import Entrega, EntregaCorreios, EntregaTransportadora


class Expedidor(ABC):

    def despachar(self, pedido: "Pedido") -> Entrega:
        # Fluxo comum a toda expedicao. So a criacao da entrega varia.
        entrega = self.criar_entrega(pedido)
        pedido.registrar_entrega(entrega)
        pedido.enviar()
        return entrega

    @abstractmethod
    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        ...


class ExpedidorLojaCentral(Expedidor):

    def __init__(self) -> None:
        self._despachos = 0

    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        self._despachos += 1
        codigo = f"BR{self._despachos:06d}SE"
        return EntregaCorreios(pedido, codigo, modalidade="SEDEX")


class ExpedidorCentroRegional(Expedidor):

    def __init__(self, transportadora: str = "Transportadora Sul") -> None:
        self._transportadora = transportadora
        self._despachos = 0

    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        self._despachos += 1
        codigo = f"TR{self._despachos:06d}"
        return EntregaTransportadora(pedido, codigo, transportadora=self._transportadora)
```

`despachar()` é o método-molde: ele descreve o que **sempre** acontece num despacho — cria a entrega, registra no pedido, muda o estado — sem saber qual `Entrega` concreta está sendo criada. Essa parte é o `criar_entrega()`, e cada `Expedidor` a implementa do seu jeito.

Não existe `if/elif` de origem em lugar nenhum. Um terceiro centro de distribuição amanhã é uma classe nova, `ExpedidorNordeste(Expedidor)`, com seu próprio `criar_entrega`. `despachar` não muda. `Pedido` não muda.

!!! info "🏗️ Decisão de Projeto — quem chama quem: `pedido.enviar(expedidor)` ou `expedidor.despachar(pedido)`?"

    Duas opções pareciam razoáveis:

    1. `Pedido.enviar(expedidor)` — o pedido recebe um expedidor e se manda despachar.
    2. `Expedidor.despachar(pedido)` — o expedidor conduz o processo e avisa o pedido.

    Escolhemos a segunda. O despacho é uma operação **da logística**, não do pedido: envolve gerar código de rastreio, escolher modalidade, e no futuro falar com a API da transportadora. Colocar isso dentro de `Pedido.enviar()` traria de volta para a entidade um monte de conhecimento de infraestrutura. `Pedido` só precisa saber guardar a entrega que recebeu (`registrar_entrega`) e mudar de estado (`enviar`) — as duas coisas continuam sendo dele.

    `Pedido.enviar()` continua existindo e funcionando sozinho, para os testes e fluxos que não precisam de um expedidor de verdade.

---

## Pedido guarda a entrega

```python title="ecommerce/pedido.py" linenums="1" hl_lines="6 11-14"
class Pedido:

    def __init__(self) -> None:
        # ... outros atributos ...
        self._entrega: Entrega | None = None

    @property
    def entrega(self) -> Entrega | None:
        return self._entrega

    def registrar_entrega(self, entrega: Entrega) -> None:
        if self._status != StatusPedido.PAGO:
            raise ValueError("So e possivel registrar entrega de um pedido pago")
        self._entrega = entrega
```

`registrar_entrega` valida a única invariante que interessa ao pedido: não existe entrega antes do pagamento.

---

## Simple Factory ou Factory Method?

| | Simple Factory (Cap. 12) | Factory Method (Cap. 13) |
|---|---|---|
| Onde a decisão mora | Num método de uma classe dedicada | Espalhada, uma decisão por subclasse |
| O que varia | Um dado (enum, string) | O tipo de quem cria |
| Adicionar variante | Mais um caso no `if/elif` da factory | Uma subclasse nova |
| Custo | Baixo — uma classe | Uma hierarquia de classes |
| Bom quando | A escolha é simples e centralizável | Quem cria já é uma família com comportamento próprio |

!!! warning "⚠️ Erro comum — criar uma hierarquia só para variar um parâmetro"

    Factory Method custa uma hierarquia de classes. Se a diferença entre "loja central" e "centro regional" fosse *só* qual string passar para um construtor, isso não pagaria o custo — uma Simple Factory com um enum `OrigemDespacho` resolveria.

    Vale a pena aqui porque cada `Expedidor` tende a ganhar comportamento próprio (regras de corte de horário, integração com transportadora, prioridade de itens). Se as suas subclasses só diferem numa linha, revise: talvez você precise de uma Simple Factory, não de Factory Method.

---

## Testes

```python title="tests/test_expedidor.py" linenums="1"
class TestExpedidor:

    def _pedido_pago(self) -> Pedido:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        return pedido

    def test_loja_central_despacha_pelos_correios(self) -> None:
        entrega = ExpedidorLojaCentral().despachar(self._pedido_pago())
        assert isinstance(entrega, EntregaCorreios)
        assert entrega.modalidade == "SEDEX"

    def test_despachar_registra_entrega_e_muda_o_estado(self) -> None:
        pedido = self._pedido_pago()
        entrega = ExpedidorLojaCentral().despachar(pedido)
        assert pedido.entrega is entrega
        assert pedido.status == "enviado"

    def test_nao_despacha_pedido_nao_pago(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        with pytest.raises(ValueError):
            ExpedidorLojaCentral().despachar(pedido)
```

```bash
$ pytest tests/
```

??? tip "109 testes passando"

    Dez testes novos: as duas `Entrega` isoladas (prazos de PAC/SEDEX, dados da transportadora, formato da etiqueta), os dois `Expedidor` criando a entrega certa, o despacho registrando a entrega e mudando o estado, e a recusa de despachar um pedido não pago. O `test_fluxo_compra` agora passa por um `Expedidor` no lugar de chamar `pedido.enviar()` direto.

---

## 🧩 Aplicando ao Projeto Financeiro

No seu sistema financeiro, pense em **exportar um relatório** em formatos diferentes: PDF para imprimir, CSV para abrir na planilha, HTML para publicar.

Cada formato monta o documento de um jeito radicalmente diferente — não é só "trocar a extensão". Modele `ExportadorRelatorio` como uma classe base com um método concreto `exportar(relatorio)` que descreve o fluxo comum (cabeçalho, corpo, rodapé, salvar) e um factory method que cria o "documento" no formato certo. `ExportadorPDF`, `ExportadorCSV`, `ExportadorHTML` implementam esse método.

Decida e documente: você usou Factory Method (uma subclasse por formato) ou uma Simple Factory (um enum `FormatoRelatorio`)? O que te fez escolher?

---

## 📌 Resumo

- **Meio de entrega** (`Entrega`, com rastreio e prazo) é um conceito diferente de **cálculo de frete** (`EstrategiaFrete`, do Módulo 3), mesmo aparecendo perto no fluxo
- A Simple Factory não serve quando a decisão de criação depende de *quem cria*, não de um dado — cada origem de despacho tem comportamento próprio
- **Factory Method**: a classe base define um método de criação abstrato e o usa num fluxo-molde; cada subclasse decide o que criar
- `Expedidor.despachar()` é o método-molde; `criar_entrega()` é o factory method que varia por subclasse
- Nova origem de despacho = nova subclasse de `Expedidor`, sem editar `despachar` nem `Pedido`
- Factory Method custa uma hierarquia; não vale a pena quando as subclasses diferem só num parâmetro

## O que mudou no sistema

- ✔ `Entrega` (abstrata), `EntregaCorreios`, `EntregaTransportadora` existem
- ✔ `Expedidor` (Factory Method), `ExpedidorLojaCentral`, `ExpedidorCentroRegional` existem
- ✔ `Pedido` guarda a entrega (`registrar_entrega`, `entrega`)
- ✔ `Expedidor.despachar` conduz o despacho e transiciona o pedido
- ❌ Notificações ao cliente ainda não existem
- ❌ `Pedido` ainda instancia sua própria `CriadorPagamento`

## O que vem a seguir

O pedido é pago e despachado — mas o cliente só descobre isso se entrar no site e conferir. Ele quer ser **avisado**: por e-mail, por SMS. No próximo capítulo vamos ver o problema da criação aparecer pela terceira vez — e reconhecer qual das factories que já conhecemos ele pede.
