# Capítulo 15 — Quem entrega as dependências?

!!! info "Situação da Empresa"

    Três capítulos, três factories, um serviço de notificação. Cada peça funciona. Mas quem tenta usar o sistema de ponta a ponta esbarra sempre na mesma dificuldade: antes de conseguir pagar um pedido, é preciso montar um monte de objeto na mão, e cada um mora num canto diferente do código.

    A pessoa que entrou nova no time perguntou: "onde eu configuro tudo isso de uma vez?" A resposta hoje é: em lugar nenhum. Está espalhado.

Vamos olhar o que o `Pedido` e o fluxo de compra acumularam ao longo do módulo — e resolver de vez a forma como as peças se encontram.

---

## O problema, concretamente

`Pedido.__init__` tem esta linha, desde o Capítulo 12:

```python
self._criador_pagamento = CriadorPagamento()
```

`Pedido` não conhece mais as classes de pagamento — a factory cuida disso. Mas ele **cria a própria factory**. Isso tem três consequências:

1. **Acoplamento escondido.** `Pedido` decide, sozinho, que a factory é a `CriadorPagamento` padrão. Se amanhã existir uma `CriadorPagamentoComAntifraude`, trocar exige editar `Pedido`.
2. **Teste difícil.** Um teste de `Pedido` não tem como colocar uma factory de mentira no lugar. Todo teste de pagamento roda a factory real.
3. **Montagem espalhada.** O `CriadorNotificacao`, o `ServicoNotificacaoPedido` e o `Expedidor` são montados por quem chama o fluxo, cada um numa linha solta. Não existe um lugar que descreva "é assim que o sistema se conecta".

```python
# Como o fluxo completo parece hoje, do lado de quem chama:
pedido = maria.finalizar_compra()

servico_notificacao = ServicoNotificacaoPedido(CriadorNotificacao())

pedido.confirmar_pagamento()                 # usa a factory que o Pedido criou sozinho
servico_notificacao.pedido_pago(pedido, maria)

ExpedidorLojaCentral().despachar(pedido)
servico_notificacao.pedido_enviado(pedido, maria)
```

Quatro objetos montados, em três lugares, e é fácil esquecer de chamar a notificação depois de uma transição.

---

!!! important "💡 Conceito — Injeção de Dependências"

    Um objeto tem uma **dependência** quando precisa de outro objeto para fazer seu trabalho. Existem duas formas de obter essa dependência:

    - **criar** — `self._criador = CriadorPagamento()`. O objeto fica preso à classe concreta.
    - **receber** — a dependência chega pronta, de fora. O objeto só declara que precisa dela.

    Receber é **Injeção de Dependências**. Você já fez isso no curso sem o nome: `Pedido.calcular_total(estrategia_desconto)` recebe a estratégia por parâmetro em vez de criar uma. `ServicoNotificacaoPedido(criador_notificacao)`, no capítulo anterior, recebe a factory pelo construtor. Agora vamos aplicar a ideia ao resto.

    O objeto que recebe fica mais simples (não sabe montar nada) e mais testável (dá para passar um dublê). O preço é que **alguém** precisa montar tudo — e esse alguém é a **raiz de composição**.

---

## Formas de injeção

| Forma | Como | Quando usar |
|---|---|---|
| Por construtor | `def __init__(self, criador): self._criador = criador` | Padrão. A dependência é obrigatória e não muda durante a vida do objeto. |
| Por método | `def calcular_total(self, estrategia): ...` | A dependência muda a cada chamada (como o desconto, que depende de quem compra). |
| Por atributo (setter) | `pedido.criador = ...` depois de criado | Evitar. O objeto pode existir num estado incompleto, sem a dependência. |

O curso já usa as duas primeiras. A terceira aparece aqui só para você reconhecer e evitar.

---

## Tirando a factory de dentro do Pedido

`Pedido` deixa de criar a `CriadorPagamento`. Ele passa a **receber** uma no momento de confirmar o pagamento — injeção por método, igual ao que `calcular_total` já fazia com a estratégia de desconto:

```python title="ecommerce/pedido.py" linenums="1" hl_lines="1 3"
def confirmar_pagamento(
    self,
    criador_pagamento: CriadorPagamento,
    forma: FormaPagamento = FormaPagamento.PIX,
    **dados,
) -> None:
    self._transicionar(StatusPedido.PAGO)
    self._pagamento = criador_pagamento.criar(forma, self, self.calcular_total(), **dados)
    self._pagamento.confirmar()
```

O `__init__` de `Pedido` perde a linha `self._criador_pagamento = CriadorPagamento()`. `Pedido` não instancia mais nada além dos próprios `ItemPedido`.

!!! warning "⚠️ Erro comum — o `default` que instancia um concreto"

    Uma "injeção" pela metade é comum:

    ```python
    def confirmar_pagamento(self, criador_pagamento: CriadorPagamento | None = None, ...):
        criador_pagamento = criador_pagamento or CriadorPagamento()  # <-- acoplamento de volta
    ```

    Com esse `or CriadorPagamento()`, quem não passa nada continua preso à classe concreta — e todo teste que "esquece" de injetar está, silenciosamente, usando a implementação real. Ou a dependência é injetada de verdade, ou o `default` traz o acoplamento de volta pela porta dos fundos.

---

## Um lugar para o fluxo morar: `ServicoPedido`

A coordenação — pagar e então notificar, despachar e então notificar — não é responsabilidade de `Pedido` (uma entidade não deveria orquestrar envio de e-mail) nem de quem chama o fluxo (que teria que lembrar a ordem toda vez). Ela ganha uma classe, que **recebe** seus três colaboradores:

```python title="ecommerce/servico_pedido.py" linenums="1"
class ServicoPedido:

    def __init__(
        self,
        criador_pagamento: CriadorPagamento,
        expedidor: Expedidor,
        servico_notificacao: ServicoNotificacaoPedido,
    ) -> None:
        self._criador_pagamento = criador_pagamento
        self._expedidor = expedidor
        self._servico_notificacao = servico_notificacao

    def pagar(self, pedido, cliente, forma: FormaPagamento = FormaPagamento.PIX, **dados) -> None:
        pedido.confirmar_pagamento(self._criador_pagamento, forma, **dados)
        self._servico_notificacao.pedido_pago(pedido, cliente)

    def despachar(self, pedido, cliente) -> Entrega:
        entrega = self._expedidor.despachar(pedido)
        self._servico_notificacao.pedido_enviado(pedido, cliente)
        return entrega
```

`ServicoPedido` não cria nenhum dos três — todos chegam pelo construtor. A notificação, que no Capítulo 14 era chamada "por quem conduz o fluxo", agora tem endereço fixo: logo depois da transição correspondente, dentro do serviço.

!!! info "🏗️ Decisão de Projeto — isto mora no `Pedido` ou num serviço?"

    `pagar` e `despachar` poderiam ser métodos de `Pedido`. Escolhemos um serviço à parte porque essas operações **coordenam vários objetos** (factory, expedidor, notificação) e envolvem infraestrutura (mensagens, no futuro transportadoras). `Pedido` continua guardando só o que é dele: itens, estado, pagamento, entrega, cupom.

    Essa separação entre "a entidade" e "o serviço que coordena a entidade" é o primeiro passo para a ideia de **camadas**, que é o assunto do Módulo 5. Por enquanto, basta perceber que nem todo comportamento cabe dentro da entidade.

---

## A raiz de composição

Existe agora **um** lugar que sabe como o sistema se conecta — o ponto de entrada da aplicação (aqui, o `if __name__ == "__main__"`; num sistema web, seria a inicialização do servidor):

```python title="ecommerce/servico_pedido.py" linenums="1"
if __name__ == "__main__":
    # Raiz de composicao: um unico lugar monta o grafo de objetos.
    servico_pedido = ServicoPedido(
        criador_pagamento=CriadorPagamento(),
        expedidor=ExpedidorLojaCentral(),
        servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacao()),
    )

    # ... monta o pedido da Maria ...

    servico_pedido.pagar(pedido, maria)
    servico_pedido.despachar(pedido, maria)
    pedido.entregar()
```

O fluxo de quem chama caiu para três linhas, e a ordem certa está garantida pelo serviço. Trocar `ExpedidorLojaCentral` por `ExpedidorCentroRegional`, ou a factory de pagamento por uma com antifraude, é mudar **uma linha na raiz de composição** — nada mais no sistema muda.

---

## O ganho aparece no teste

Com tudo injetado, testar o fluxo não precisa mais de colaboradores reais:

```python title="tests/test_servico_pedido.py" linenums="1"
def test_colaboradores_podem_ser_trocados_sem_tocar_no_servico(self) -> None:
    class ExpedidorFake(Expedidor):
        def __init__(self) -> None:
            self.chamado = False

        def criar_entrega(self, pedido: Pedido) -> Entrega:
            self.chamado = True
            return EntregaCorreios(pedido, "FAKE-1")

    expedidor_fake = ExpedidorFake()
    servico = ServicoPedido(
        criador_pagamento=CriadorPagamento(),
        expedidor=expedidor_fake,
        servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacaoFake(self.espia)),
    )

    servico.pagar(pedido, self.cliente)
    servico.despachar(pedido, self.cliente)
    assert expedidor_fake.chamado is True
```

Nenhuma linha de `ServicoPedido` sabe que está lidando com um expedidor de mentira. Foi só passar outro objeto na construção.

```bash
$ pytest tests/
```

??? tip "123 testes passando"

    Seis testes novos para `ServicoPedido`: pagar confirma o pedido e notifica; despachar envia e notifica; um colaborador pode ser trocado por um dublê sem tocar no serviço. Os testes de `Pedido` agora passam uma `CriadorPagamento` explícita para `confirmar_pagamento` — e ficou visível, no teste, exatamente qual factory está em uso.

---

## 🧩 Aplicando ao Projeto Financeiro

Volte aos leitores (Capítulo 12), importadores (Capítulo 14) e exportadores (Capítulo 13) do seu sistema financeiro. Provavelmente, hoje, cada serviço que os usa cria os próprios: `self._criador_leitor = CriadorLeitor()`.

Faça o mesmo movimento deste capítulo:

1. Cada serviço **recebe** suas factories pelo construtor, em vez de criá-las.
2. Crie um `ServicoImportacao` (ou nome equivalente) que coordena "ler o arquivo → importar os lançamentos → gerar o relatório", recebendo os colaboradores injetados.
3. Escreva uma **raiz de composição** — uma função `montar_aplicacao()` ou o próprio `if __name__ == "__main__"` — que monta o grafo inteiro num lugar só.

Documente: o que ficou mais fácil de testar depois disso? Que colaborador você conseguiria substituir por um dublê hoje, sem editar nenhum serviço?

Quando terminar, você está pronto para o [checkpoint de entrega do módulo](entrega.md).

---

## 📌 Resumo

- Um objeto que **cria** seus colaboradores fica acoplado às classes concretas e difícil de testar; um objeto que **recebe** fica simples e substituível
- **Injeção de Dependências**: a dependência chega de fora. Por construtor (padrão), por método (quando muda a cada chamada), por setter (evitar)
- `Pedido` parou de instanciar `CriadorPagamento`; ela é injetada em `confirmar_pagamento`, como a estratégia de desconto já era em `calcular_total`
- Um `default=` que instancia um concreto anula a injeção — é acoplamento escondido
- `ServicoPedido` dá endereço fixo à coordenação (pagar+notificar, despachar+notificar) e recebe seus três colaboradores
- A **raiz de composição** é o único lugar que monta o grafo de objetos; trocar uma implementação é mudar uma linha lá

## O que mudou no sistema

- ✔ `Pedido` não instancia mais nenhuma factory; `confirmar_pagamento` recebe a `CriadorPagamento`
- ✔ `ServicoPedido` coordena pagamento, despacho e notificação com colaboradores injetados
- ✔ Existe uma raiz de composição montando o grafo num único lugar
- ✔ O fluxo completo é testável com dublês, sem colaboradores reais
- ❌ Tudo ainda vive em memória — nada é persistido
- ❌ A coordenação e o domínio ainda moram no mesmo pacote, sem separação de camadas

## O que vem a seguir

O módulo fecha aqui. O E-Commerce sabe criar seus objetos sem espalhar condicionais e sabe montar suas dependências num lugar só. Mas todo pedido, todo pagamento, toda entrega desaparece quando o programa termina — não há persistência. E o `ServicoPedido` que acabamos de criar é a ponta de um assunto maior: **separar o domínio da infraestrutura**. É o Módulo 5.

Antes disso, consolide seu Projeto Financeiro: [entregue a terceira parte](entrega.md).
