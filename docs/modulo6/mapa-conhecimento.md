# Mapa de Conhecimento — Módulo 6

> **Do sistema organizado ao sistema que reage**

No Módulo 5, a pergunta era **quem pode conhecer quem**. No Módulo 6 ela ganha uma versão mais fina: **quem *causa* um acontecimento precisa conhecer quem *reage* a ele?** A resposta, ao longo dos quatro capítulos, foi que não.

## O que foi acrescentado

### Observer e eventos

- **Observer** — um objeto (o sujeito) mantém uma lista de observadores e os avisa quando algo acontece. O sujeito conhece apenas o contrato do observador.
- **Evento de domínio** — um objeto imutável que representa algo que **já aconteceu**, com nome no passado (`PedidoPago`). Carrega o que os interessados precisam saber.
- **Barramento de eventos (publish/subscribe)** — um intermediário entre quem publica e quem assina. Guarda as assinaturas e entrega cada evento a quem se inscreveu no seu tipo.
- **Manipulador (*handler*)** — quem reage a um evento. Em Python, uma função ou um objeto com `__call__`.

    ```
    PagarPedido
        ↓ publica PedidoPago
    BarramentoEventos  (porta, na aplicação)
        ↑ implementado por
    BarramentoEmMemoria  (adaptador, na infraestrutura)
        ↓ entrega a
    notificar · dar baixa no estoque · registrar auditoria
    ```

### Pontos de entrada

- **Ponto de entrada (adaptador de entrada)** — o código que fica entre o mundo de fora (teclado, tela, rede) e os casos de uso. É o oposto dos adaptadores de saída (banco, e-mail): é quem **chama** o sistema.
- **Quarta camada (`entrada/`)** — importa domínio, aplicação e a raiz de composição, nunca a infraestrutura; ninguém importa a entrada.
- **A interface é um detalhe** — terminal, REST, GUI ou TUI podem ser trocados sem mexer no centro do sistema.
- **A fronteira traduz exceções** — o que o caso de uso lança vira mensagem, ou status HTTP, na linguagem do meio.
- **Consulta também é caso de uso** — `ListarProdutos`, `ConsultarPedido`.
- **Entradas injetadas** — o menu recebe `entrada` e `saida` de fora, e o teste passa uma sessão roteirizada.

### Comando e evento

| | Comando | Evento |
|---|---|---|
| Expressa | Uma intenção | Um fato |
| Nome | Imperativo (`PagarPedido`) | Passado (`PedidoPago`) |
| Destino | Um só | Zero, um ou vários |
| Pode ser recusado | Sim | Não |

### Falhas e consistência

- **Postura diante da falha** — propagar (a reação faz parte da operação), isolar e registrar (o fato já é verdade) ou repetir/compensar (precisa acontecer de qualquer jeito).
- **Consistência eventual** — por um tempo, as partes do sistema não concordam, e dependem de algo para voltarem a concordar.
- **Idempotência** — repetir o tratamento de um evento não pode ter efeito duplicado.
- **Atomicidade** — o que precisa acontecer junto, ou nada, pertence à mesma transação, e não a um evento.

### Persistência parcial

O sistema persiste **apenas uma parte** dos dados (`Produto`, `Pedido`, `ItemPedido`). Um sistema real persistiria tudo, e com muitas classes um **ORM** começa a compensar, como mais um adaptador do mesmo contrato.

### SOLID

O módulo reforça dois princípios:

- **SRP**: `PagarPedido` voltou a ter uma só razão para mudar, pagar.
- **OCP**: acrescentar uma reação é **estender** o sistema pela montagem, sem editar o que já funciona.

### Bônus: o catálogo de padrões

Decorator, State, Adapter, Composite, Chain of Responsibility, Command com handler e Builder ficaram de fora do caminho principal por falta de uma dor que os pedisse. O Capítulo 23 os apresenta como um mapa de pesquisa, e a entrega final pede que o aluno escolha um. Em Python, muitos se reduzem a funções, listas e argumentos nomeados; o Singleton é um alerta, e a raiz de composição entrega o que ele prometia.

## O mapa acumulado

```mermaid
graph TD
    DOM[Domínio] --> OBJ[Objetos]
    OBJ --> RESP[Responsabilidades]
    RESP --> AC[Acoplamento]
    AC --> DIP[Inversão de Dependências]
    DIP --> CAM[Camadas]
    DIP --> REPO[Repository]
    CAM --> UC[Casos de uso]
    UC --> OBS[Observer]
    OBS --> EVT[Eventos de domínio]
    EVT --> BAR[Barramento de eventos]
    DIP --> BAR
    UC --> ENT[Pontos de entrada]
    BAR --> FAL[Falhas em reações]
    FAL --> EVE[Consistência eventual]
    EVT --> CMD[Comando × evento]
```

## A pergunta central do módulo

> **Quem faz precisa conhecer quem reage?**

A resposta final do módulo é:

```text
Quem faz anuncia o que aconteceu, no passado.

                 ↓

Quem se importa assina, e é ligado numa montagem única.

                 ↓

O que precisa acontecer em volta (log, tempo) embrulha a operação,
sem entrar nela.
```

## Onde chegamos

```text
Módulo 1
Modelar conceitos e responsabilidades
        ↓
Módulo 2
Proteger estado e coordenar comportamentos
        ↓
Módulo 3
Isolar variações de comportamento
        ↓
Módulo 4
Isolar criação e montagem de dependências
        ↓
Módulo 5
Isolar o domínio dos detalhes técnicos
        ↓
Módulo 6
Isolar quem faz de quem reage
```

O sistema agora tem uma estrutura que diz o que é cada coisa, uma regra verificada sobre quem depende de quem, um mecanismo para crescer **por adição** (reações entram pela montagem, sem abrir o que já existe) e uma porta pela qual alguém pode usá-lo. É o encerramento do percurso do curso, e o ponto de partida para a [entrega final](entrega.md).
