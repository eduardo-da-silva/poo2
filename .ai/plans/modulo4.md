# Plano de Escrita — Módulo 4: Criando Objetos

> Documento de planejamento para a produção do Módulo 4 do material.
> Consultar junto com `.ai/rules/` (especialmente `07-curriculum.md`, `08-course-roadmap.md`,
> `05-domain.md`, `06-code-style.md`, `02-course-structure.md`, `11-review-checklist.md`).
> Este documento descreve **o que** escrever e **em que ordem**. Não substitui as regras de estilo.

---

## 1. Visão geral do módulo

**Título:** Módulo 4 — Criando Objetos
**Capítulos:** 12 a 15 (o Módulo 3 terminou no Capítulo 11)
**Padrões introduzidos:** Simple Factory, Factory Method, Dependency Injection
**Entrega:** sim — `docs/modulo4/entrega.md` (checkpoint formativo avaliado, nos moldes de M2 e M3)

### Arco narrativo

O fluxo de compra está completo (M2) e flexível (M3: descontos, cupons, frete). A dor deste
módulo **não** é "qual algoritmo escolher" — isso foi Strategy. É **qual objeto construir, e
quem constrói**. A empresa passou a ter variedade em coisas que precisam ser *instanciadas*:

- várias **formas de pagamento** (Pix, boleto, cartão), cada uma com dados e confirmação próprios;
- vários **meios de entrega** (Correios PAC/SEDEX, transportadora parceira), cada um com rastreio
  e prazo próprios;
- **notificações** ao cliente por canal (e-mail, SMS) quando o pedido muda de estado.

Cada `if/elif` de criação acopla quem chama (`Pedido`, serviços) a todos os construtores
concretos. O módulo mostra como isolar a criação (Factory) e, ao final, como inverter a
montagem das dependências (DI), devolvendo ao `Pedido` uma responsabilidade única.

### Estado do sistema no início do módulo (fim do Cap. 11)

- ✔ Fluxo completo: carrinho → pedido → pagamento → envio → entrega
- ✔ `EstrategiaDesconto` / `SemDesconto` / `DescontoPercentual`
- ✔ `Cupom` com validade + regra de desconto
- ✔ `EstrategiaFrete` / `FreteFixo` / `FreteGratisAcimaDe`
- ✔ `Pedido.calcular_valor_final` combina desconto e frete
- ✔ `Pagamento` é **classe concreta única**, instanciada dentro de `Pedido.confirmar_pagamento()`
- ❌ Só existe uma forma de pagamento
- ❌ Entrega não é entidade (só existe cálculo de frete)
- ❌ Não existem notificações
- ❌ Objetos criam seus próprios colaboradores (sem inversão)

### Estado do sistema ao final do módulo (fim do Cap. 15)

- ✔ `Pagamento` é abstração; `PagamentoPix` / `PagamentoBoleto` / `PagamentoCartao`
- ✔ `CriadorPagamento` (Simple Factory) isola a criação da forma de pagamento
- ✔ `Entrega` é abstração; `EntregaCorreios` / `EntregaTransportadora`
- ✔ `Expedidor` (Factory Method) — `ExpedidorLojaCentral` / `ExpedidorCentroRegional`
- ✔ `Notificacao` é abstração; `NotificacaoEmail` / `NotificacaoSMS`; `CriadorNotificacao`
- ✔ `Pedido` (ou serviço de aplicação) recebe seus colaboradores por injeção
- ✔ Raiz de composição no script de exemplo monta o grafo de objetos
- ❌ Ainda tudo em memória, sem persistência (→ Módulo 5)
- ❌ Notificação ainda é chamada direta, sem eventos (→ Módulo 6)

---

## 2. Capítulo 12 — Formas de pagamento e o problema da criação (Simple Factory)

**Objetivo pedagógico:** mostrar que decidir *qual objeto instanciar* é uma responsabilidade,
e que espalhar essa decisão acopla quem cria a todos os tipos concretos. Introduzir Simple
Factory como a solução mínima.

**Conceitos:** criação como responsabilidade; acoplamento a construtores concretos; Simple
Factory; enum para estado (reforço de `06-code-style`); interface/`ABC` (reforço do M3).

### Situação da empresa

Todo pedido hoje é pago de um jeito só: `Pedido.confirmar_pagamento()` faz `Pagamento(self,
valor)` e chama `confirmar()`. A empresa passou a aceitar **Pix**, **boleto** e **cartão de
crédito**. Cada forma tem dados próprios (chave Pix; linha digitável e vencimento do boleto;
bandeira e parcelas do cartão) e confirma de maneira diferente.

### Problema

Onde nasce o objeto de pagamento certo? Se `Pedido` (ou a tela de checkout) fizer
`if forma == "pix": ... elif forma == "boleto": ...`, `Pedido` passa a conhecer todas as
formas e seus construtores. Cada forma nova obriga a editar `Pedido`.

### Discussão (perguntas socráticas)

- Quem deveria saber montar um `Pagamento`? O `Pedido`? O `Cliente`? Uma peça dedicada?
- O que muda quando aparecer "PayPal"? Quantos lugares eu edito?
- A regra "como confirmar um Pix" pertence ao `Pedido` ou ao próprio pagamento?

### Modelagem

- `FormaPagamento` (enum): `PIX`, `BOLETO`, `CARTAO_CREDITO`.
- `SituacaoPagamento` (enum): `PENDENTE`, `CONFIRMADO`, `RECUSADO` — substitui o
  `_confirmado: bool` atual (regra do curso: estado é enum, não flag booleana).
- `Pagamento` deixa de ser classe concreta única → vira `ABC` com contrato:
  `confirmar()`, `valor`, `situacao`.
- Implementações: `PagamentoPix`, `PagamentoBoleto`, `PagamentoCartao` — cada uma com seus
  atributos específicos e sua regra de `confirmar()`.
- `CriadorPagamento` (Simple Factory): `criar(forma: FormaPagamento, pedido, valor, **dados)
  -> Pagamento`. Concentra o `match`/dict de decisão num único lugar.

Diagramas:
- Class diagram: `Pagamento` (ABC) + 3 implementações + `CriadorPagamento`.
- Sequence diagram: `Pedido → CriadorPagamento.criar → PagamentoPix`.

### Implementação (incremental)

1. Extrair `SituacaoPagamento` e ajustar o `Pagamento` atual para usá-lo (refatoração pequena,
   sem mudar comportamento).
2. Transformar `Pagamento` em `ABC`; criar `PagamentoPix` primeiro (caso mais simples).
3. Mostrar o `if/elif` ingênuo dentro de `Pedido.confirmar_pagamento(forma, **dados)` —
   sentir a dor.
4. Extrair `CriadorPagamento`; `Pedido.confirmar_pagamento` passa a delegar. `Pedido` passa a
   depender só de `Pagamento` (abstração) e `CriadorPagamento`.
5. Adicionar `PagamentoBoleto` e `PagamentoCartao` — mostrar que só a factory muda.

### ⚠️ Erro comum

- Factory que devolve `dict`/tupla em vez de objetos polimórficos.
- Factory que, além de criar, **confirma** o pagamento (mistura criação com regra de negócio).
- Factory como método estático dentro de `Pedido` (não resolveu o acoplamento, só mudou de lugar).

### 🏗️ Decisão de projeto

Simple Factory não é um padrão GoF "oficial" — é uma função/classe que isola a criação.
Por que começar por ela: resolve a maior parte da dor com o mínimo de estrutura. Registrar
quando ela começa a incomodar (gancho do Cap. 13).

### 🧩 Aplicando ao Projeto Financeiro

Leitores de arquivo de extrato: CSV, OFX, JSON. Um `CriadorLeitor` que decide qual leitor
instanciar pela extensão/tipo do arquivo. O aluno modela a interface `Leitor` e ≥2
implementações.

### Testes

- Cada `Pagamento*` isolado (atributos, `confirmar()`, transições de `SituacaoPagamento`).
- `CriadorPagamento` retorna o tipo certo para cada `FormaPagamento`.
- Forma desconhecida → `ValueError` (ou `FormaPagamentoInvalidaError`).
- Atualizar `test_pagamento.py` herdado do M3.

### Resumo + gancho

Resumo: criação isolada numa peça só; `Pedido` voltou a não conhecer formas concretas.
Gancho: e quando a *regra de qual objeto criar* depender de contexto que a factory central
não deveria conhecer (a transportadora varia por origem de despacho, por contrato)? Uma
factory central vira um `if/elif` gigante de novo.

---

## 3. Capítulo 13 — Meios de entrega (Factory Method)

**Objetivo pedagógico:** mostrar o limite da Simple Factory (centralização) e introduzir
Factory Method — cada subclasse decide qual produto criar, mantendo aberto para extensão via
herança.

**Conceitos:** Factory Method; método-molde (template) que usa o factory method; Simple
Factory × Factory Method (quando usar cada um); herança usada com parcimônia.

### Situação da empresa

Pedido pago precisa ser **despachado**. A empresa trabalha com Correios (PAC e SEDEX) e uma
transportadora parceira para regiões específicas. Cada meio gera **código de rastreio** e
**prazo estimado** de formas diferentes.

### ⚠️ Ponto de confusão a tratar de frente

`EstrategiaFrete` (Cap. 11) calcula **quanto custa** o frete. O meio de entrega deste capítulo
cria um objeto `Entrega` que representa a **remessa** (rastreio + prazo + etiqueta), quando o
pedido é despachado. São conceitos distintos. Incluir uma seção `🔍 Análise` comparando os dois
lado a lado, com tabela.

### Problema com a Simple Factory

A escolha do meio de entrega não é um `match` simples por enum: depende de **quem está
despachando**. A loja principal usa Correios; um centro de distribuição regional usa a
transportadora parceira; no futuro, marketplace com regras próprias. Colocar tudo num
`CriadorEntrega` central obriga esse criador a conhecer as regras de cada origem.

### Modelagem

- `Entrega` (ABC): `codigo_rastreio`, `prazo_estimado()`, `etiqueta()` (opcional).
- Implementações: `EntregaCorreios` (PAC/SEDEX por parâmetro **ou** duas classes — discutir a
  escolha), `EntregaTransportadora`.
- `Expedidor` (ABC):
  - factory method abstrato `criar_entrega(pedido) -> Entrega`;
  - método concreto `despachar(pedido)` que chama `criar_entrega` e muda o estado do pedido
    (template method — reaproveita o fluxo, varia só a criação).
- Subclasses: `ExpedidorLojaCentral`, `ExpedidorCentroRegional` — cada uma implementa
  `criar_entrega`.

Diagramas:
- Class diagram: `Expedidor` (ABC) + subclasses; `Entrega` (ABC) + implementações.
- Tabela comparativa Simple Factory × Factory Method.

### Implementação (incremental)

1. Modelar `Entrega` e uma implementação (`EntregaCorreios`).
2. Criar `Expedidor` com `despachar` + `criar_entrega` abstrato; `ExpedidorLojaCentral`.
3. Integrar ao `Pedido`: decidir se `Pedido.enviar()` recebe um `Expedidor` ou se o
   `Expedidor.despachar(pedido)` chama `pedido.enviar()`. Registrar a decisão (prenúncio de DI
   no Cap. 15 e de camadas no M5).
4. Adicionar `ExpedidorCentroRegional` + `EntregaTransportadora` — mostrar extensão sem editar
   o que já existe.

### 🏗️ Decisão de projeto

Simple Factory: um lugar decide, fácil, mas centraliza o conhecimento. Factory Method: cada
subclasse decide o seu, aberto a extensão por herança, ao custo de uma hierarquia. Não trocar
Simple Factory por Factory Method quando a variação é só um parâmetro.

### ⚠️ Erro comum

- Criar hierarquia de `Expedidor` só para variar um parâmetro (bastava Simple Factory).
- Herança profunda de expedidores.
- `Entrega` anêmica (só dados), com o cálculo de prazo/rastreio vazando para o `Expedidor`.

### 🧩 Aplicando ao Projeto Financeiro

Exportadores de relatório: `ExportadorRelatorio` (ABC) com factory method `criar_documento()`;
subclasses `ExportadorPDF`, `ExportadorCSV`, `ExportadorHTML`.

### Testes

- `EntregaCorreios` / `EntregaTransportadora` isoladas.
- Cada `Expedidor` produz a `Entrega` certa.
- `despachar` muda o estado do pedido corretamente e falha se o pedido não estiver pago.

### Resumo + gancho

Resumo: quando a decisão de criação depende de contexto/variante, Factory Method distribui
essa decisão sem `if/elif`. Gancho: pagamento e entrega variados; quando o pedido muda de
estado, o cliente precisa ser avisado — por e-mail, por SMS. De novo: quem cria o notificador?

---

## 4. Capítulo 14 — Notificações (Factory reaproveitada, sem eventos ainda)

**Objetivo pedagógico:** reconhecer que a *forma do problema* se repete (como Strategy se
repetiu no M3) e reaproveitar Simple Factory. Praticar a escolha do padrão certo para o
problema certo.

**Conceitos:** reaproveitamento de um padrão já conhecido; Simple Factory × Factory Method
revisitados; separação entre "criar o notificador" e "disparar a notificação".

### ⚠️ Escopo — não antecipar o Módulo 6 (Observer / Eventos)

Aqui o `Pedido` (ou um serviço de pedido) chama a notificação **direta e explicitamente**
depois de mudar de estado. **Nada** de publish/subscribe, lista de observers ou eventos. O
foco é apenas: *como o objeto notificador certo é criado*. Incluir uma nota (`💡` ou `🔍`)
reconhecendo que essa chamada direta vai incomodar — e que o Módulo 6 resolve o acoplamento
com eventos.

### Situação da empresa

O cliente quer ser avisado quando o pedido é **pago** e quando é **enviado**. Canais:
**e-mail** e **SMS** (push no futuro). Cada canal monta a mensagem e "envia" de forma diferente.

### Modelagem

- `CanalNotificacao` (enum): `EMAIL`, `SMS`.
- `Notificacao` (ABC): `enviar(destinatario, mensagem)`.
- Implementações: `NotificacaoEmail`, `NotificacaoSMS` (o "envio" é simulado — `print`/log; o
  curso não integra serviços externos).
- `CriadorNotificacao` (Simple Factory) — reaproveita o formato do Cap. 12.
- Montagem da mensagem por estado do pedido (`pedido_pago`, `pedido_enviado`) — simples, sem
  template engine.

### Implementação (incremental)

1. Modelar `Notificacao` + `NotificacaoEmail`.
2. `CriadorNotificacao.criar(canal) -> Notificacao`.
3. `Cliente.canal_preferido: CanalNotificacao`.
4. `ServicoNotificacaoPedido` que recebe um `CriadorNotificacao` e é chamado por
   `Pedido`/`Cliente` após as transições de estado.
5. Adicionar `NotificacaoSMS`.

### 🏗️ Decisão de projeto

Por que Simple Factory de novo, e não Factory Method: a escolha do canal é **preferência do
cliente** (um dado em tempo de execução), não uma regra de subclasse. Reconhecer o padrão
certo para o problema certo é o aprendizado do capítulo.

### ⚠️ Erro comum

- `Pedido` importando `NotificacaoEmail` diretamente.
- `if canal == EMAIL: print(...)` espalhado por vários pontos.
- Serviço de notificação que também decide *quando* notificar misturado com a regra de
  transição de estado do pedido.

### 🧩 Aplicando ao Projeto Financeiro

Importadores por origem: `CriadorImportador` que decide qual importador instanciar conforme o
banco/origem do arquivo (Banco X, Banco Y), reaproveitando o formato de solução.

### Testes

- Dublês (spy/fake) de `Notificacao` para verificar que `enviar` foi chamado com a mensagem
  certa.
- `CriadorNotificacao` devolve o canal certo.
- `ServicoNotificacaoPedido` dispara a notificação nas transições esperadas.

### Resumo + gancho

Resumo: o mesmo padrão (Simple Factory) resolveu um terceiro problema; saber escolher entre
Simple Factory e Factory Method é parte do trabalho. Gancho: três factories, três pontos onde
`Pedido` e serviços fazem `new` dos próprios colaboradores. `Pedido` virou um objeto que sabe
demais sobre como montar suas dependências. Como inverter isso?

---

## 5. Capítulo 15 — Quem entrega as dependências? (Dependency Injection)

**Objetivo pedagógico:** mostrar que criar os próprios colaboradores é acoplamento, e que
declarar dependências e recebê-las prontas (DI) torna o objeto simples e testável. Fechar o
módulo com uma refatoração ampla.

**Conceitos:** Inversão de Controle; Injeção de Dependências (construtor, método, setter);
raiz de composição; DI manual × contêiner.

### Situação da empresa

Olhar o `Pedido` acumulado ao final do Cap. 14: ele instancia `CriadorPagamento`, recebe (ou
cria) `Expedidor`, chama `ServicoNotificacaoPedido`... parte injetado, parte criado
internamente, inconsistente. Testar `Pedido` obriga a carregar factories reais.

### Problema

- Acoplamento a construtores concretos.
- Dificuldade de teste (não dá para trocar por dublês sem editar `Pedido`).
- Impossível trocar implementação (ex.: `CriadorPagamentoFake` em teste; notificação real ×
  fake) sem mexer no código que usa.

### Conceito

Inversão de Controle / Injeção de Dependências: o objeto **declara o que precisa** (de
preferência no construtor) e **recebe pronto** de quem o cria. Ligar com o que já foi visto:
`Pedido.calcular_total(estrategia_desconto)` já era injeção por parâmetro (method injection);
agora isso é formalizado e generalizado.

### Modelagem / refatoração

- `Pedido` **ou** um serviço de aplicação (`ServicoPedido` / `Checkout`) recebe no construtor:
  `CriadorPagamento`, `Expedidor`, `ServicoNotificacaoPedido`. Discutir explicitamente a
  escolha entre pôr isso no `Pedido` (entidade) ou num serviço — é um prenúncio das camadas
  do Módulo 5.
- **Raiz de composição:** o `if __name__ == "__main__"` do script de exemplo passa a montar o
  grafo de objetos num único lugar.
- Tipos de injeção: por construtor (padrão), por método (já usado em `calcular_total`), por
  setter (quando e por que evitar).

Diagramas:
- Grafo de dependências do `Pedido` antes × depois.
- Sequence da raiz de composição montando tudo e passando para o serviço.

### 🏗️ Decisão de projeto

DI **manual**, sem contêiner/framework — coerente com `06-code-style` (evitar frameworks;
domínio independente). Mencionar que contêineres de DI existem, mas são um detalhe de
infraestrutura.

### ⚠️ Erro comum

- "Injetar" mas manter `default=` que instancia um concreto no construtor (acoplamento
  escondido — isso já existe hoje em `calcular_total` com `estrategia_desconto=None`;
  aproveitar como exemplo).
- Service Locator disfarçado de DI (o objeto pede a dependência a um registro global).
- Injetar coisas demais — sinal de que a classe faz demais.

### 🧩 Aplicando ao Projeto Financeiro

Montar a raiz de composição do sistema financeiro: leitores + importadores + exportadores
injetados num serviço de importação/relatório. Nenhum desses serviços instancia os próprios
colaboradores.

### Testes

- `Pedido` / serviço de aplicação testável com dublês de todos os colaboradores.
- Mostrar o teste ficando **mais simples** depois da refatoração (antes × depois).

### Resumo do módulo (Cap. 15 encerra o módulo)

- Simple Factory isola *como* criar quando a decisão é central e simples.
- Factory Method distribui a decisão de criação quando ela varia por contexto/variante.
- DI isola *quem fornece* os colaboradores.
- Juntos, devolvem ao `Pedido` uma responsabilidade única.

### Gancho para o Módulo 5

Temos muitos objetos sendo montados numa raiz de composição, mas tudo ainda vive em memória e
a lógica de aplicação está misturada no domínio. O Módulo 5 separa domínio de infraestrutura:
camadas, repositórios, persistência.

---

## 6. Página de entrega — `docs/modulo4/entrega.md`

Mesmo formato de `docs/modulo2/entrega.md` e `docs/modulo3/entrega.md`. Checkpoint formativo,
avaliado, não substitui a entrega final do Módulo 7.

**O que o aluno já deve ter construído no Projeto Financeiro:**

- Interface `Leitor` + ≥2 implementações (Cap. 12), criadas por uma factory.
- `CriadorImportador` decidindo o importador por origem/formato (Cap. 14).
- Interface `ExportadorRelatorio` + ≥2 implementações com factory method (Cap. 13).
- Raiz de composição que injeta leitores + importadores + exportadores num serviço (Cap. 15).
- Testes automatizados (dublês onde fizer sentido), suíte inteira passando.

**O que deve ser entregue:**

1. Código-fonte organizado como pacote `financeiro/` (mesma estrutura desde o M1).
2. Testes `pytest` cobrindo sucesso e erro, todos passando.
3. README curto respondendo, com justificativa:
   - Em cada caso (leitor, importador, exportador), você usou Simple Factory ou Factory
     Method? Por quê?
   - O que é injetado e o que é criado internamente nos seus serviços? Por quê?
   - Que formato novo você consegue adicionar hoje sem editar nenhuma classe existente?

**Prazo:** `[DATA A DEFINIR]` (link de repositório Git com acesso ao professor).

**Tabela de avaliação (0 a 10):** nos moldes do M3 — pesos como proposta, ajustáveis com o
professor. Critérios sugeridos:

| Critério | Peso | O que é avaliado |
|---|---|---|
| Factory de leitores | 1,5 | Isola a criação; extensível sem editar chamadores |
| Factory de importadores | 1,5 | Decisão de criação por origem, sem `if/elif` espalhado |
| Factory Method de exportadores | 1,5 | Cada variante decide seu produto; ≥2 formatos funcionando |
| Injeção de dependências | 2,0 | Serviços recebem colaboradores prontos; nada de `new` interno |
| Testes automatizados | 2,0 | Sucesso e erro cobertos; suíte passando; dublês onde couber |
| Decisões de projeto documentadas | 1,0 | Perguntas do README respondidas e justificadas |
| Organização e coesão do código | 0,5 | Estrutura de pacotes, nomes, responsabilidades separadas |

---

## 7. Arquivos a criar / modificar

### Novos — documentação

- `docs/modulo4/index.md` — visão geral (quadro ✔/❌, "o que você aprenderá", estrutura dos 4
  capítulos), no formato de `docs/modulo3/index.md`.
- `docs/modulo4/capitulo12.md`
- `docs/modulo4/capitulo13.md`
- `docs/modulo4/capitulo14.md`
- `docs/modulo4/capitulo15.md`
- `docs/modulo4/entrega.md`

### Novos — código (snapshot acumulativo por capítulo, padrão dos módulos anteriores)

- `code/modulo4/capitulo12/` — `ecommerce/` + `tests/` + `requirements.txt`
- `code/modulo4/capitulo13/`
- `code/modulo4/capitulo14/`
- `code/modulo4/capitulo15/`

Cada capítulo parte do snapshot do capítulo anterior (Cap. 12 parte de
`code/modulo3/capitulo11/`). Novos arquivos previstos ao longo do módulo:
`ecommerce/forma_pagamento.py`, `situacao_pagamento.py` (ou dentro de `pagamento.py`),
`pagamento.py` (refatorado para ABC + implementações), `criador_pagamento.py`,
`entrega.py`, `expedidor.py`, `notificacao.py`, `canal_notificacao.py`,
`criador_notificacao.py`, `servico_notificacao_pedido.py`, e refatorações em `pedido.py` e
`cliente.py`. Testes correspondentes em `tests/`.

### Modificar — configuração do site

- `mkdocs.yml` — nova seção no `nav`:
  ```yaml
  - Módulo 4 — Criando Objetos:
    - Visão geral do módulo: modulo4/index.md
    - Capítulo 12 — Formas de pagamento e o problema da criação: modulo4/capitulo12.md
    - "Capítulo 13 — Meios de entrega: Factory Method": modulo4/capitulo13.md
    - Capítulo 14 — Notificações: modulo4/capitulo14.md
    - Capítulo 15 — Quem entrega as dependências?: modulo4/capitulo15.md
    - Entrega da Terceira Parte do Projeto: modulo4/entrega.md
  ```
- `docs/index.md` — acrescentar entrada do Módulo 4.

### Modificar — regras do curso (`.ai/rules/`)

- `05-domain.md`:
  - `Pagamento` passa a ser abstração com implementações por `FormaPagamento`; adicionar
    `FormaPagamento` e `SituacaoPagamento` à linguagem ubíqua e à lista de entidades.
  - Adicionar `Entrega` / meio de entrega (rastreio, prazo) — distinta de `EstrategiaFrete`.
  - Adicionar `Notificacao` / `CanalNotificacao`.
  - Atualizar invariantes de `Pagamento` (situação como enum; pertence a um pedido).
  - Relacionamentos permitidos: `Pedido → Entrega`, `Pedido → Notificacao` /
    `Cliente → Notificacao` (definir qual).
- `07-curriculum.md`: acrescentar o bloco "Checkpoint de entrega" ao Módulo 4 (hoje só M2, M3
  e M7 têm), apontando `docs/modulo4/entrega.md`.
- `08-course-roadmap.md`: detalhar as Aulas 12 a 15 no mesmo formato das Aulas 1 a 10
  (Objetivo / E-Commerce / Projeto Financeiro / Conceitos / Discussões / Código / Diagramas /
  Exercícios / Gancho). Hoje o roadmap detalhado para depois da Aula 10.

---

## 8. Ordem de execução

1. **Domínio primeiro** — atualizar `.ai/rules/05-domain.md` (regra do próprio curso: o
   domínio evolui antes do código).
2. Atualizar `.ai/rules/07-curriculum.md` e `.ai/rules/08-course-roadmap.md`.
3. **Capítulo 12:** escrever `code/modulo4/capitulo12/` (código + testes, `pytest` verde) →
   depois `docs/modulo4/capitulo12.md`.
4. **Capítulo 13:** partir do snapshot do Cap. 12 → código + testes → `capitulo13.md`.
5. **Capítulo 14:** idem, a partir do Cap. 13.
6. **Capítulo 15:** idem, a partir do Cap. 14.
7. `docs/modulo4/index.md` e `docs/modulo4/entrega.md`.
8. `mkdocs.yml` + `docs/index.md`.
9. Revisão capítulo a capítulo com `.ai/rules/11-review-checklist.md`; rodar `pytest` em cada
   `code/modulo4/capituloN/`; conferir build do MkDocs.

---

## 9. Riscos e pontos de atenção

- **`EstrategiaFrete` (M3) × meio de entrega (M4):** risco de parecer retrabalho. Tratar de
  frente no Cap. 13 com seção `🔍 Análise` e tabela comparativa (cálculo de custo × objeto de
  remessa com rastreio/prazo).
- **Não antecipar Observer / Eventos (Módulo 6)** no Cap. 14: notificação é chamada direta e
  explícita; o capítulo só cuida da *criação* do notificador.
- **`Pagamento` deixa de ser classe concreta:** é uma mudança de modelagem sobre o M3.
  Apresentar como **evolução** do negócio ("a empresa passou a aceitar várias formas"), nunca
  como correção de erro. Atualizar `test_pagamento.py` herdado e qualquer teste de fluxo que
  instancie `Pagamento` diretamente.
- **`Pedido` acumulando dependências nos caps. 12–14** é dívida **intencional** — a dor que o
  Cap. 15 resolve. Os capítulos devem deixá-la visível, sem "consertar antes da hora".
- **DI sem framework:** manter injeção manual e raiz de composição no script de exemplo,
  coerente com `06-code-style`.
- **Consistência de nomenclatura:** fixar os nomes (`FormaPagamento`, `SituacaoPagamento`,
  `CriadorPagamento`, `Entrega`, `Expedidor`, `Notificacao`, `CanalNotificacao`,
  `CriadorNotificacao`, `ServicoNotificacaoPedido`) em `05-domain.md` antes de escrever os
  capítulos, e não variar depois.
- **Tamanho dos capítulos:** os do M3 têm ~200 linhas de Markdown. O Cap. 15 (refatoração
  ampla) tende a ser maior — controlar para não virar um capítulo denso demais.
