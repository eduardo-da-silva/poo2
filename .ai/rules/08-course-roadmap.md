# rules/08-course-roadmap.md

# Roadmap do Curso

## Objetivo

Este documento descreve a evolução completa do curso, aula a aula.

Ele serve como guia para a produção do material didático.

Antes de escrever qualquer capítulo, este documento deve ser consultado.

Cada aula representa um incremento do software.

Nenhuma funcionalidade deve surgir antes do momento previsto.

Nenhum conceito deve ser antecipado sem justificativa pedagógica.

---

# Estrutura de cada aula

Toda aula deve responder às seguintes perguntas.

## Objetivo

O que o aluno deverá aprender?

---

## Evolução do E-Commerce

Qual parte do sistema será construída?

---

## Projeto Financeiro

Como o aluno aplicará o mesmo conceito?

---

## Conceitos de POO

Quais conceitos serão reforçados?

---

## Discussões

Quais perguntas deverão ser feitas ao aluno?

---

## Código

Quais classes serão criadas ou modificadas?

---

## Diagramas

Quais diagramas deverão aparecer?

---

## Exercícios

Quais atividades serão propostas?

---

## Gancho

Como preparar a próxima aula?

---

# MÓDULO 1

## Aula 1
### O primeiro contato com o domínio

### Objetivo

Apresentar o curso.

Apresentar o projeto.

Mostrar que Orientação a Objetos é modelagem.

Não ensinar sintaxe.

---

### E-Commerce

Apresentação do domínio.

Produto.

Categoria.

Primeira modelagem.

Sem persistência.

Sem interface.

---

### Projeto Financeiro

Apresentar o domínio.

Conta.

Categoria.

Lançamento.

Nenhum código ainda.

---

### Conceitos

Modelagem.

Objeto.

Classe.

Responsabilidade.

Linguagem ubíqua.

---

### Discussões

O que realmente é um Produto?

Produto conhece Cliente?

Categoria calcula preço?

Quem deveria conhecer quem?

---

### Diagramas

Primeiro diagrama de classes.

Produto

Categoria

Relacionamento.

---

### Código

Classe Produto.

Classe Categoria.

Relacionamento entre ambas.

---

### Exercícios

Criar novas categorias.

Adicionar novos produtos.

Modelar atributos.

---

### Gancho

Agora temos produtos.

Mas ninguém pode comprá-los.

Como um cliente escolhe produtos?

---

# Aula 2

### Objetivo

Introduzir Cliente.

Mostrar colaboração entre objetos.

---

### E-Commerce

Cliente.

Primeira associação.

---

### Projeto Financeiro

Cadastro de contas.

---

### Conceitos

Relacionamentos.

Associações.

Responsabilidades.

---

### Discussões

Cliente deve conhecer Produto?

Produto deve conhecer Cliente?

---

### Código

Cliente.

Relacionamentos.

---

### Gancho

Cliente existe.

Agora ele precisa comprar.

---

# Aula 3

### Objetivo

Criar Carrinho.

Introduzir composição.

---

### E-Commerce

Carrinho.

Cliente possui Carrinho.

---

### Projeto Financeiro

Carteira.

Conta principal.

---

### Conceitos

Composição.

Responsabilidade.

Alta coesão.

---

### Discussões

Carrinho deve guardar Produtos?

Ou outra abstração?

---

### Código

Carrinho.

Adicionar produto.

Remover produto.

---

### Diagramas

Cliente

↓

Carrinho

---

### Gancho

Agora surge um problema.

Como controlar quantidades?

---

# Aula 4

### Objetivo

Criar ItemCarrinho.

Mostrar quando um relacionamento vira objeto.

---

### Conceitos

Composição.

Objetos ricos.

Modelagem.

---

### Discussões

Por que não guardar apenas Produto?

Onde fica a quantidade?

---

### Código

ItemCarrinho.

Subtotal.

Carrinho refatorado.

---

### Exercícios

Adicionar alteração de quantidade.

---

### Gancho

Nosso Carrinho funciona.

Mas quem calcula o total?

---

# Aula 5

### Objetivo

Refatorar Carrinho.

Distribuir responsabilidades.

---

### Conceitos

Coesão.

Acoplamento.

Objetos ricos.

---

### Discussões

Quem calcula subtotal?

Quem calcula total?

Quem conhece preço?

---

### Código

Refatoração completa.

---

### Gancho

Agora podemos finalizar uma compra.

---

# Aula 6

### Objetivo

Criar Pedido.

---

### Conceitos

Estado.

Responsabilidade.

Transição.

---

### Código

Pedido.

ItemPedido.

---

### Gancho

Pedido criado.

Mas ainda não existe pagamento.

---

# Aula 7

Pagamento.

Estados.

Primeira enumeração.

---

# Aula 8

Cupons.

Primeira implementação simples.

Sem Strategy.

---

# Aula 9

Problemas da implementação.

Condicionais crescendo.

Preparação para Strategy.

---

# Aula 10

Strategy.

Refatoração.

Primeiro padrão.

---

# MÓDULO 2

A partir deste ponto o roadmap continua exatamente no mesmo formato.

Cada aula deverá possuir:

Objetivos.

Conceitos.

Discussões.

Código.

Diagramas.

Exercícios.

Projeto Financeiro.

Gancho.

---

# MÓDULO 4 — Criando Objetos

## Aula 12
### Formas de pagamento e o problema da criação (Simple Factory)

### Objetivo

Mostrar que decidir *qual objeto instanciar* é uma responsabilidade.

Espalhar essa decisão acopla quem cria a todos os tipos concretos.

Introduzir Simple Factory como a solução mínima.

---

### E-Commerce

`Pagamento` deixa de ser classe concreta única e vira abstração.

`PagamentoPix`, `PagamentoBoleto`, `PagamentoCartao`.

`FormaPagamento` (enum), `SituacaoPagamento` (enum, substitui a flag `_confirmado`).

`CriadorPagamento` isola a criação.

`Pedido.confirmar_pagamento(forma, **dados)` delega ao criador.

---

### Projeto Financeiro

Leitores de arquivo de extrato (CSV, OFX, JSON) e um `CriadorLeitor`.

---

### Conceitos

Criação como responsabilidade.

Acoplamento a construtores concretos.

Simple Factory.

Enum para estado.

---

### Discussões

Quem deveria saber montar um `Pagamento`?

O que muda quando aparece uma forma nova?

A regra de confirmação pertence ao `Pedido` ou ao pagamento?

---

### Diagramas

Class diagram: `Pagamento` (ABC) + implementações + `CriadorPagamento`.

Sequence: `Pedido → CriadorPagamento → PagamentoPix`.

---

### Exercícios

Adicionar uma nova forma de pagamento sem editar `Pedido`.

Projeto Financeiro: interface `Leitor` + duas implementações + factory.

---

### Gancho

E quando a regra de qual objeto criar depender de contexto que a factory central
não deveria conhecer? Ela vira um `if/elif` gigante de novo.

---

## Aula 13
### Meios de entrega (Factory Method)

### Objetivo

Mostrar o limite da Simple Factory (centralização).

Introduzir Factory Method: cada subclasse decide qual produto criar.

Diferenciar meio de entrega (objeto de remessa) de cálculo de frete (Módulo 3).

---

### E-Commerce

`Entrega` (ABC): código de rastreio, prazo estimado.

`EntregaCorreios`, `EntregaTransportadora`.

`Expedidor` (ABC) com factory method `criar_entrega` + `despachar`.

`ExpedidorLojaCentral`, `ExpedidorCentroRegional`.

---

### Projeto Financeiro

Exportadores de relatório (`ExportadorRelatorio` + factory method): PDF, CSV, HTML.

---

### Conceitos

Factory Method.

Método-molde que usa o factory method.

Simple Factory × Factory Method.

---

### Discussões

`EstrategiaFrete` calcula custo; `Entrega` é criada no despacho. São a mesma coisa?

A escolha do meio de entrega depende de quê?

---

### Diagramas

Class diagram: `Expedidor` + subclasses; `Entrega` + implementações.

Tabela Simple Factory × Factory Method.

---

### Exercícios

Adicionar uma nova origem de despacho por extensão, sem editar as existentes.

Projeto Financeiro: `ExportadorRelatorio` com factory method e duas implementações.

---

### Gancho

Pagamento e entrega variados. Quando o pedido muda de estado, o cliente precisa
ser avisado — por e-mail, por SMS. Quem cria o notificador certo?

---

## Aula 14
### Notificações (Factory reaproveitada, sem eventos ainda)

### Objetivo

Reconhecer que a forma do problema se repete e reaproveitar Simple Factory.

Praticar a escolha do padrão certo para o problema certo.

Não antecipar Observer/eventos (Módulo 6).

---

### E-Commerce

`Notificacao` (ABC): `enviar(destinatario, mensagem)`.

`NotificacaoEmail`, `NotificacaoSMS`.

`CanalNotificacao` (enum), `CriadorNotificacao`.

`Cliente.canal_preferido`.

`ServicoNotificacaoPedido` chamado após as transições de estado do pedido.

---

### Projeto Financeiro

Importadores por origem/banco e um `CriadorImportador`.

---

### Conceitos

Reaproveitamento de um padrão já conhecido.

Simple Factory × Factory Method revisitados.

Separação entre criar o notificador e disparar a notificação.

---

### Discussões

Por que Simple Factory de novo, e não Factory Method?

Onde mora a decisão de *quando* notificar?

---

### Diagramas

Class diagram: `Notificacao` + implementações + `CriadorNotificacao`.

Sequence: transição do pedido → `ServicoNotificacaoPedido` → `NotificacaoEmail`.

---

### Exercícios

Adicionar um novo canal (push) sem editar quem dispara a notificação.

Projeto Financeiro: `CriadorImportador` por origem.

---

### Gancho

Três factories, três pontos onde `Pedido` e serviços fazem `new` dos próprios
colaboradores. `Pedido` sabe demais sobre como montar suas dependências.

---

## Aula 15
### Quem entrega as dependências? (Dependency Injection)

### Objetivo

Mostrar que criar os próprios colaboradores é acoplamento.

Declarar dependências e recebê-las prontas (DI) torna o objeto simples e testável.

Fechar o módulo com uma refatoração ampla.

---

### E-Commerce

`Pedido` (ou um serviço de aplicação `ServicoPedido`/`Checkout`) recebe no
construtor: `CriadorPagamento`, `Expedidor`, `ServicoNotificacaoPedido`.

Raiz de composição no script de exemplo monta o grafo de objetos.

Tipos de injeção: construtor, método, setter.

---

### Projeto Financeiro

Raiz de composição do sistema financeiro: leitores, importadores e exportadores
injetados num serviço.

---

### Conceitos

Inversão de Controle.

Injeção de Dependências.

Raiz de composição.

DI manual × contêiner.

---

### Discussões

Isso mora no `Pedido` (entidade) ou num serviço? (prenúncio de camadas do Módulo 5)

O `default=` que instancia um concreto é injeção de verdade?

---

### Diagramas

Grafo de dependências do `Pedido` antes × depois.

Sequence da raiz de composição montando tudo.

---

### Exercícios

Testar o `Pedido`/serviço com dublês de todos os colaboradores.

Projeto Financeiro: montar a raiz de composição.

---

### Gancho

Muitos objetos montados numa raiz, tudo em memória, aplicação misturada no
domínio. O Módulo 5 separa domínio de infraestrutura: camadas, repositórios,
persistência.

---

# MÓDULO 5 — Organização do Sistema

Detalhamento completo em `.ai/plans/modulo5.md`.

## Aula 16 — O sistema precisa lembrar (Repository)

Identidade (`id`) em `Produto` e `Pedido`. `RepositorioProduto` / `RepositorioPedido` (contrato) e implementações em memória. `ServicoPedido` passa a operar por `pedido_id`. Projeto Financeiro: repositório de lançamentos. Gancho: reiniciar o programa apaga tudo.

## Aula 17 — Guardando de verdade (SQLite)

Segunda implementação do mesmo contrato com `sqlite3`; `Pedido.reconstituir`; suíte de contrato rodando nas duas implementações; seção sobre ORM (o que mudaria). Pagamento, entrega e cupom ficam fora da persistência (dívida visível). Gancho: tudo na mesma pasta.

## Aula 18 — Casos de uso e camadas

`dominio/`, `aplicacao/`, `infraestrutura/`; `ServicoPedido` vira `CadastrarProduto`, `FinalizarCompra`, `PagarPedido`, `DespacharPedido`; `composicao.py`; teste de arquitetura com uma violação conhecida (`xfail`). Gancho: como a aplicação envia notificação sem conhecer a infraestrutura?

## Aula 19 — Quem depende de quem? (DIP)

Contrato `Notificacao` / `FabricaNotificacao` sobe para a aplicação; `xfail` vira teste verde; DIP × DI × raiz de composição; trocar memória/SQLite/ORM só na composição. Gancho: cada reação a um pagamento vira mais uma linha no caso de uso (Módulo 6, eventos).

---

# MÓDULO 6 — Eventos

## Aula 20 — Quem precisa saber? (Observer)

Baixa de estoque quando o pedido é pago (`Produto.dar_baixa`, `EstoqueInsuficienteError`). Observer clássico em `PagarPedido` (`ObservadorDePagamento`; observadores de notificação e estoque). Limites: lista por sujeito, observador preso ao sujeito, aviso sem nome, falha de um observador derruba os seguintes (teste que documenta a dívida). Projeto Financeiro: observador de meta estourada. Gancho: o aviso não diz o que aconteceu.

## Aula 21 — Fatos, não ordens (eventos de domínio)

`PedidoPago` e `PedidoDespachado` (imutáveis, no domínio); porta `BarramentoEventos` na aplicação e `BarramentoEmMemoria` na infraestrutura; manipuladores em `aplicacao/manipuladores/` (notificação, estoque, auditoria); `RegistroAuditoria`. A prova: uma reação nova entra só pela composição. Decisão: o caso de uso publica, depois de guardar. Gancho: log e tempo não são reações a um fato.

## Aula 22 — Colocando o sistema para rodar (pontos de entrada)

Quarta camada `entrada/` (importa domínio, aplicação e composição; nunca infraestrutura). `cenario.py` (dados fixos, `--armazenamento`, `--banco`, `--cenario`) e `menu.py` (terminal, `entrada` e `saida` injetadas, exceções traduzidas). Consultas como casos de uso (`ListarProdutos`, `ConsultarPedido`). Esboço de REST (texto, não executado) com quatro pontos de contato. Seção explícita: só uma parte dos dados é persistida; um sistema real persistiria tudo e um ORM começaria a compensar. Cenário da última unidade (Ana e Bia): falha em reação, três posturas, `BarramentoEmMemoria(ao_falhar=...)`, consistência eventual, idempotência. Gancho: padrões que ficaram de fora (bônus).

## Aula 23 — Bônus: padrões que ficaram de fora

Catálogo (sem muito código): Decorator, State, Adapter, Composite, Chain of Responsibility, Command com handler, Builder; alerta sobre o Singleton; padrões que "somem" em Python; quadro dos padrões do curso; como pesquisar. Na entrega final, o aluno escolhe um padrão do catálogo, pesquisa, implementa, testa e justifica (15% da nota, proposta). Código de referência do Decorator em `code/modulo6/bonus-decorator/`.

---

# Ordem dos padrões

Strategy.

↓

Simple Factory, Template Method e Factory Method.

↓

Facade e Dependency Injection.

↓

Repository (e Data Mapper).

↓

Observer e eventos (publish/subscribe).

↓

Pontos de entrada (adaptadores de entrada).

↓

Bônus: Decorator, State, Adapter, Composite, Chain of Responsibility, Command, Builder.

Nunca antecipar padrões.

Cada um deve resolver um problema existente.

---

# Ordem das refatorações

Duplicação.

↓

Extração de métodos.

↓

Extração de classes.

↓

Polimorfismo.

↓

Camadas.

↓

Arquitetura.

---

# Crescimento da arquitetura

Inicialmente.

Arquivos simples.

↓

Pacotes.

↓

Domínio.

↓

Aplicação.

↓

Infraestrutura.

↓

Persistência.

Nunca começar o curso com arquitetura complexa.

---

# Evolução do Projeto Financeiro

O Projeto Financeiro sempre acompanha o E-Commerce.

Ele nunca deve ficar mais de uma aula atrasado.

O aluno deve conseguir aplicar imediatamente os conceitos recém-aprendidos.

---

# Regra de ouro

Toda aula deve responder claramente:

O que o software aprendeu?

O que o aluno aprendeu?

O que faremos na próxima aula?

Se uma dessas respostas não estiver clara, a aula deverá ser reestruturada.