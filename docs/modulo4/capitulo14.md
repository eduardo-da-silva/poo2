# Capítulo 14 — Notificações

!!! info "Situação da Empresa"

    Pedido pago, pedido despachado. Só que o cliente não fica sabendo de nada disso a menos que entre no site e vá conferir. O suporte está recebendo mensagens do tipo "meu pedido sumiu" quando na verdade ele já está a caminho.

    "Avisa o cliente", pediu o gerente. "Quando o pagamento confirmar, e quando o pedido sair para entrega. Alguns preferem e-mail, outros preferem SMS."

Precisamos, em dois momentos do fluxo, montar uma mensagem e enviá-la pelo canal que o cliente escolheu. E-mail e SMS enviam de formas diferentes — e o SMS ainda tem limite de caracteres.

Você já viu esse filme duas vezes neste módulo. Vale reconhecer o padrão antes de escrever qualquer coisa.

---

!!! note "🔍 Análise — de qual factory este problema precisa?"

    - **Formas de pagamento** (Cap. 12): a escolha era um dado que o cliente passa na hora (`FormaPagamento`). Decisão simples, centralizável → **Simple Factory**.
    - **Meios de entrega** (Cap. 13): a escolha dependia de *quem despacha*, e cada origem tinha comportamento próprio → **Factory Method**.
    - **Canal de notificação** (agora): a escolha é uma preferência do cliente — um dado, `EMAIL` ou `SMS`. `NotificacaoEmail` e `NotificacaoSMS` não têm um "fluxo" próprio como o `Expedidor` tinha; elas só sabem enviar.

    A forma do problema é a mesma do Capítulo 12. A solução também é: uma **Simple Factory**. Reconhecer isso poupa a gente de inventar uma hierarquia de subclasses que não se paga.

---

## Modelando a notificação

O contrato é mínimo: dado um destinatário e uma mensagem, enviar.

```python title="ecommerce/notificacao.py" linenums="1"
from abc import ABC, abstractmethod


class Notificacao(ABC):

    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        ...


class NotificacaoEmail(Notificacao):

    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[E-MAIL -> {destinatario}] {mensagem}")


class NotificacaoSMS(Notificacao):

    # SMS tem limite de caracteres; mensagens longas sao cortadas.
    LIMITE = 160

    def enviar(self, destinatario: str, mensagem: str) -> None:
        texto = mensagem[: self.LIMITE]
        print(f"[SMS -> {destinatario}] {texto}")
```

O `print` faz o papel de "enviar de verdade". Num sistema real, `NotificacaoEmail` falaria com um servidor SMTP e `NotificacaoSMS` com uma API de mensagens — mas isso é infraestrutura, não muda a modelagem. O que importa aqui é que cada canal cumpre o mesmo contrato do seu jeito (o SMS ainda corta a mensagem no limite).

---

## A factory

Idêntica em forma à `CriadorPagamento` do Capítulo 12:

```python title="ecommerce/criador_notificacao.py" linenums="1"
from ecommerce.canal_notificacao import CanalNotificacao
from ecommerce.notificacao import Notificacao, NotificacaoEmail, NotificacaoSMS


class CriadorNotificacao:

    def criar(self, canal: CanalNotificacao) -> Notificacao:
        if canal == CanalNotificacao.EMAIL:
            return NotificacaoEmail()
        if canal == CanalNotificacao.SMS:
            return NotificacaoSMS()
        raise ValueError(f"Canal de notificacao desconhecido: {canal}")
```

`CanalNotificacao` é um enum (`EMAIL`, `SMS`). Adicionar "push" no futuro é: criar `NotificacaoPush`, adicionar um caso aqui, escrever os testes da factory. Nada mais no sistema muda.

!!! info "🏗️ Decisão de Projeto — por que não Factory Method, já que "funcionou" com entrega?"

    Poderíamos criar `NotificadorEmail(Notificador)` e `NotificadorSMS(Notificador)`, cada um com um factory method. Seria mais código para o mesmo resultado.

    Factory Method vale a pena quando *quem cria* já é uma família de classes com fluxo próprio — foi o caso do `Expedidor`, que tinha `despachar()`. Aqui não existe esse fluxo: a escolha do canal é um dado simples (`canal_preferido` do cliente), e a criação cabe num `match`. Usar Factory Method aqui seria aplicar um padrão porque "deu certo da última vez", não porque o problema pede. Escolher o padrão certo é parte do trabalho.

---

## Cliente conhece seu canal preferido

```python title="ecommerce/cliente.py" linenums="1" hl_lines="7-8 15-18"
from ecommerce.canal_notificacao import CanalNotificacao


class Cliente:

    def __init__(self, nome, email, telefone: str = "",
                 canal_preferido: CanalNotificacao = CanalNotificacao.EMAIL) -> None:
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.canal_preferido = canal_preferido
        # ... carrinho, pedidos ...

    @property
    def contato(self) -> str:
        if self.canal_preferido == CanalNotificacao.SMS:
            return self.telefone
        return self.email
```

`contato` devolve o endereço certo para o canal preferido — quem for enviar a notificação não precisa saber se é e-mail ou telefone. A preferência é do cliente, então mora no `Cliente`.

---

## O serviço que monta e dispara

Montar a mensagem de "pagamento confirmado" ou "pedido enviado" não é responsabilidade de `Pedido` (ele não deveria saber redigir texto para cliente) nem de `Notificacao` (ela só sabe enviar). É uma responsabilidade nova, e ganha uma classe:

```python title="ecommerce/servico_notificacao_pedido.py" linenums="1"
from ecommerce.criador_notificacao import CriadorNotificacao


class ServicoNotificacaoPedido:

    def __init__(self, criador_notificacao: CriadorNotificacao) -> None:
        self._criador_notificacao = criador_notificacao

    def pedido_pago(self, pedido: "Pedido", cliente: "Cliente") -> None:
        mensagem = (
            f"Ola, {cliente.nome}. O pagamento do seu pedido foi confirmado. "
            f"Total: R$ {pedido.calcular_total():.2f}."
        )
        self._notificar(cliente, mensagem)

    def pedido_enviado(self, pedido: "Pedido", cliente: "Cliente") -> None:
        rastreio = pedido.entrega.codigo_rastreio if pedido.entrega is not None else "-"
        mensagem = (
            f"Ola, {cliente.nome}. Seu pedido foi enviado. "
            f"Codigo de rastreio: {rastreio}."
        )
        self._notificar(cliente, mensagem)

    def _notificar(self, cliente: "Cliente", mensagem: str) -> None:
        notificacao = self._criador_notificacao.criar(cliente.canal_preferido)
        notificacao.enviar(cliente.contato, mensagem)
```

Repare no `__init__`: o serviço **recebe** o `CriadorNotificacao`, não o cria. Isso já é injeção de dependência — a mesma ideia que o Capítulo 15 vai levar a sério para o resto do sistema. Aqui ela aparece de graça, e o benefício fica óbvio nos testes.

Como o serviço é usado, por enquanto, é o código que conduz o fluxo quem chama:

```python
servico = ServicoNotificacaoPedido(CriadorNotificacao())

pedido.confirmar_pagamento()
servico.pedido_pago(pedido, cliente)

ExpedidorLojaCentral().despachar(pedido)
servico.pedido_enviado(pedido, cliente)
```

!!! warning "⚠️ Erro comum — fazer `Pedido` disparar a notificação"

    A tentação é colocar `self._servico_notificacao.pedido_pago(...)` dentro de `Pedido.confirmar_pagamento()`. Aí `Pedido` passaria a conhecer o serviço de notificação, o criador, o canal... e a mudança de estado ficaria amarrada ao envio de mensagem (um erro no SMS quebraria o pagamento).

    Por enquanto, quem chama a transição também chama a notificação, logo em seguida, de forma explícita. É repetitivo e fácil de esquecer — e é exatamente esse desconforto que o **Módulo 6** vai resolver, com eventos. Por ora, o foco é só um: qual objeto de notificação é criado, e por quem.

---

!!! tip "🧠 Pense antes de continuar"

    Este é o terceiro `CriadorX` do módulo. `Pedido` cria `CriadorPagamento` no seu `__init__`. Quem conduz o fluxo cria `CriadorNotificacao` e monta o `ServicoNotificacaoPedido`. O `Expedidor` é instanciado à parte.

    São peças espalhadas, cada uma montada num canto. Se você fosse escrever um teste do fluxo completo, quantos objetos precisaria construir na mão antes de começar? E se quisesse trocar um deles por uma versão de mentira?

---

## Testes

O serviço é testado com dublês — uma `Notificacao` espiã e um `CriadorNotificacao` falso, injetado no lugar do real:

```python title="tests/test_servico_notificacao_pedido.py" linenums="1"
class NotificacaoEspia(Notificacao):
    def __init__(self) -> None:
        self.enviadas: list[tuple[str, str]] = []

    def enviar(self, destinatario: str, mensagem: str) -> None:
        self.enviadas.append((destinatario, mensagem))


class CriadorNotificacaoFake:
    def __init__(self, notificacao: Notificacao) -> None:
        self._notificacao = notificacao
        self.canais_pedidos: list[CanalNotificacao] = []

    def criar(self, canal: CanalNotificacao) -> Notificacao:
        self.canais_pedidos.append(canal)
        return self._notificacao


def test_usa_o_canal_preferido_do_cliente(self) -> None:
    cliente = Cliente("João", "joao@email.com", telefone="+55 47 90000-0000",
                      canal_preferido=CanalNotificacao.SMS)
    self.servico.pedido_pago(self._pedido_pago(), cliente)
    assert self.criador_fake.canais_pedidos == [CanalNotificacao.SMS]
    assert self.espia.enviadas[0][0] == "+55 47 90000-0000"
```

```bash
$ pytest tests/
```

??? tip "120 testes passando"

    Onze testes novos: `NotificacaoEmail`/`NotificacaoSMS` isoladas (incluindo o corte do SMS no limite), a factory devolvendo a classe certa por canal, o erro para canal desconhecido, o `contato` do cliente seguindo a preferência, e o `ServicoNotificacaoPedido` montando a mensagem certa e usando o canal preferido — tudo com dublês, sem enviar nada de verdade.

---

## 🧩 Aplicando ao Projeto Financeiro

No seu sistema financeiro, os extratos vêm de bancos diferentes, e cada banco formata o arquivo do seu jeito — mesmo quando todos são "CSV". Você precisa de um **importador** por origem: `ImportadorBancoX`, `ImportadorBancoY`.

A escolha do importador é um dado (o banco de origem, que você identifica pelo cabeçalho do arquivo ou por uma configuração). Isso é o cenário da Simple Factory: crie um `CriadorImportador` que, dado o identificador do banco, devolve o importador certo.

Compare com o que você fez no Capítulo 13 para os exportadores de relatório (Factory Method). Documente: por que importador é Simple Factory e exportador é Factory Method — ou por que, no seu caso, os dois são iguais?

---

## 📌 Resumo

- O problema de "criar o objeto certo" apareceu pela terceira vez — e reconhecer a **forma** do problema diz qual factory usar
- Canal de notificação é uma preferência simples do cliente (um dado) → **Simple Factory**, como no pagamento; não Factory Method
- `Notificacao` (abstrata), `NotificacaoEmail`, `NotificacaoSMS`; `CriadorNotificacao` decide por `CanalNotificacao`
- Montar a mensagem é uma responsabilidade própria: `ServicoNotificacaoPedido`, que **recebe** o criador em vez de instanciá-lo — injeção de dependência, aparecendo naturalmente
- A notificação é disparada por chamada direta após a transição; eventos (Módulo 6) resolvem esse acoplamento depois
- Escolher o padrão certo para o problema é tão importante quanto conhecer o padrão

## O que mudou no sistema

- ✔ `Notificacao` (abstrata), `NotificacaoEmail`, `NotificacaoSMS` existem
- ✔ `CanalNotificacao` (enum) e `CriadorNotificacao` existem
- ✔ `Cliente` conhece seu `canal_preferido` e expõe `contato`
- ✔ `ServicoNotificacaoPedido` monta e dispara as mensagens de pagamento e envio
- ❌ Quem conduz o fluxo ainda monta todas as peças na mão
- ❌ `Pedido` ainda instancia sua própria `CriadorPagamento`

## O que vem a seguir

Temos três factories e um punhado de serviços — e cada um é montado num canto diferente do código. `Pedido` cria o seu criador de pagamento sozinho; o resto é montado por quem chama o fluxo. No próximo capítulo vamos parar de espalhar essa montagem: um único lugar monta o grafo de objetos, e cada peça **recebe** o que precisa em vez de criar. É o fecho do módulo — **Injeção de Dependências**.
