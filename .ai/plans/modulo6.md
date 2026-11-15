# Plano de Escrita — Módulo 6: Eventos

> Documento de planejamento do Módulo 6. Consultar junto com `.ai/rules/` e
> `.ai/plans/decisoes-pos-modulo5.md`. Descreve **o que** escrever e **em que ordem**;
> não substitui as regras de estilo. **Status (2026-11-15): escrito.** Caps. 20–23 e snapshots em `code/modulo6/` (191 / 196 / 234 testes; `bonus-decorator` 204). A estrutura final difere do plano original (ver "Estrutura final" logo abaixo); as seções "Cap. 22" e "Cap. 23" mais adiante descrevem o plano **antigo** (Decorator e falhas como capítulos) e estão superadas.

**Capítulos:** 20 a 23 (o Módulo 5 terminou no Capítulo 19)
**Conceitos:** Observer (publisher/subscriber), eventos de domínio, Decorator, Command × evento, falha em reações
**Entrega:** **entrega final** do Projeto Financeiro (`docs/modulo6/entrega.md`). Não há Módulo 7:
a entrega final migrou para cá (ver `decisoes-pos-modulo5.md`).

## Estrutura final (2026-11-15)

Decidida com o professor depois de rever o plano: o módulo **termina no `main`**, e os padrões que ficaram de fora viram um capítulo **bônus**.

| Cap. | Título | Conteúdo |
|---|---|---|
| 20 | Quem precisa saber? (Observer) | Baixa de estoque; Observer clássico; limites |
| 21 | Fatos, não ordens (eventos de domínio) | Eventos, barramento, manipuladores, auditoria; caixa comando × evento |
| 22 | Colocando o sistema para rodar | Camada `entrada/` (cenário fixo, menu de terminal), consultas como casos de uso, esboço de REST (texto), **persistência parcial e ORM**, cenário da última unidade e **falha em reações** (`ao_falhar`) |
| 23 | Bônus: padrões que ficaram de fora | Catálogo de 7 padrões (Decorator, State, Adapter, Composite, Chain, Command com handler, Builder), alerta do Singleton, padrões que "somem" em Python, quadro do curso, como pesquisar |

- O antigo capítulo de **Decorator** virou um bloco do bônus; o código testado ficou como referência opcional em `code/modulo6/bonus-decorator/` (parte de `capitulo21`, 204 testes).
- O antigo capítulo de **falhas** virou a última seção do Cap. 22.
- **Entrega final:** exige persistência em SQLite, uma interface (cenário, menu ou REST) e **um padrão do catálogo do bônus** (15% da nota, 1,5 ponto, proposta). Pesos: domínio 0,5; variações e criação 1,0; persistência e camadas 1,5; eventos 1,5; testes 1,5; interface 1,0; padrão do bônus 1,5; documento 1,0; organização 0,5. Prazo em aberto.
- **Testes verificados:** Cap. 20 = 191, Cap. 21 = 196, Cap. 22 = 234.

## Histórico: revisão de 2026-11-15 (plano antes da decisão final)


**Motivo.** O aluno nunca vê o sistema rodar de fora para dentro: há `__main__` soltos por arquivo e um demo em
`composicao.py`, mas ninguém "usa" o sistema. Um capítulo de ponto de entrada fecha Ports & Adapters (até aqui só
adaptadores de **saída**: SQLite, e-mail, barramento; faltam os de **entrada**), e dá ao Decorator e às falhas algo
visível para mostrar. Posição: **depois do Cap. 21**, antes do Decorator.

**Nova numeração** (o conteúdo dos antigos 22 e 23 não muda, só o número e o gancho):

| Cap. | Título | Origem |
|---|---|---|
| 20 | Quem precisa saber? (Observer) | já escrito |
| 21 | Fatos, não ordens (eventos de domínio) | já escrito; o "O que vem a seguir" muda (gancho: ninguém usa o sistema) |
| **22** | **Colocando o sistema para rodar (pontos de entrada)** | **novo** |
| 23 | Embrulhando comportamento (Decorator) | antigo 22 |
| 24 | Quando a reação falha | antigo 23 |

Cadeia de ganchos: 21 → "só os testes executam o sistema" → 22 → "queremos ver o que ele faz por dentro (log, tempo)" →
23 → "e se uma reação falha? rode a última unidade" → 24 → entrega final (Capítulos 1 a 24).

### Cap. 22 — Colocando o sistema para rodar (pontos de entrada)

**Situação da Empresa:** a diretoria pede uma demonstração; o time descobre que só os testes executam o sistema.

**Conceito:** *ponto de entrada* = adaptador de **entrada** (*driving adapter*): quem chama os casos de uso. A interface
(terminal, TUI, GUI, REST) é um **detalhe**, como o banco e o ORM. Quarta camada: `ecommerce/entrada/`, que importa
`dominio`, `aplicacao` e `composicao`, nunca `infraestrutura`; ninguém importa `entrada`.

**Código (snapshot `code/modulo6/capitulo22/`, parte de `capitulo21`):**

- `entrada/cenario.py` — o `main` com **dados fixos**: cadastra produtos, cria clientes, compra, paga e despacha; imprime estoque
  antes/depois, notificações e a trilha de auditoria. Função `executar_cenario(app, saida)` testável; `argparse` com
  `--armazenamento memoria|sqlite` e `--banco ARQUIVO`, mostrando a raiz de composição trocando peças sem tocar em caso de uso.
  Por padrão usa `:memory:` (rodar duas vezes com arquivo duplicaria os produtos: material para o Nível 2).
- `entrada/menu.py` — **menu de terminal** só com a biblioteca padrão (`input`/`print`), com `entrada` e `saida` **injetadas**
  (DI de novo; o teste passa uma sessão roteirizada). Opções: listar produtos, pôr no carrinho, finalizar compra, pagar, despachar,
  ver auditoria, sair. Cliente fixo (Maria), carrinho só na sessão. O menu **traduz exceções para a linguagem do meio**
  (`PedidoNaoEncontradoError`, `ValueError`, `EstoqueInsuficienteError` viram mensagens), adiantando o mapeamento exceção → HTTP.
- Dois casos de uso de **consulta** novos, para o menu não tocar em repositório: `ListarProdutos` e `ConsultarPedido`
  (leitura também é caso de uso). Entram em `Aplicacao` e na composição.
- Testes: cenário (saída esperada, memória e SQLite), menu (sessões roteirizadas, erros amigáveis, opção inválida), casos de
  uso de consulta (nas duas implementações), arquitetura (`entrada` não importa `infraestrutura`; nenhuma outra camada importa
  `entrada`). Meta aproximada: +15 sobre os 196 do Cap. 21; **confirmar rodando**.

**Seção "E se fosse REST, GUI ou TUI?" (texto, não código testado):** esboço de ~30 linhas de FastAPI (`montar_aplicacao()`
uma vez, endpoints `POST /produtos`, `GET /produtos`, `POST /pedidos`, `POST /pedidos/{id}/pagamento`, `POST /pedidos/{id}/despacho`)
e uma frase para TUI/GUI ("a tela chama os mesmos casos de uso"). Quatro pontos de contato, cada um com a lacuna do sistema atual:
(1) **quem é o cliente?** (hoje o `Cliente` não é persistido e os casos de uso recebem o objeto); (2) **serializar** `Pedido`/`Produto`
(DTO/esquemas; o domínio não vira JSON sozinho); (3) **exceção → status HTTP** (404 / 422 / 409), a mesma tradução que o menu faz;
(4) **conexão e threads** (`sqlite3` e `check_same_thread`; uma conexão por requisição). Nada em `dominio/` nem `aplicacao/` muda.
`fastapi` **não** entra em `requirements.txt` do snapshot. Um capítulo bônus com REST de verdade só existiria assumindo o custo de
persistir cliente e carrinho (ver abaixo).

**Seção "O que ainda não está persistido" (explícita, pedido do professor):** tabela do que vai e do que não vai para o SQLite.

| Persistido | Não persistido (só memória) |
|---|---|
| `Produto`, `Pedido`, `ItemPedido` | `Cliente`, `Carrinho`, `Pagamento`, `Entrega`, `Cupom`, registro de auditoria, eventos |

Dizer com clareza: **isto é um recorte didático**. Um sistema real persiste **tudo**; o menu e o cenário já mostram a lacuna
(reiniciar perde cliente, carrinho e auditoria; um pedido relido volta sem pagamento, entrega e cupom). Persistir o resto traz
mais tabelas, mapeamento de hierarquias (`Pagamento` e `Entrega` são polimórficos), `Pedido` referenciando `Cliente` e migrações.
Nesse ponto o SQL escrito à mão (um `INSERT`/`UPDATE`/`SELECT` e um mapeador por classe) vira trabalho repetitivo e propenso a
erro, e **é aí que um ORM passa a compensar** (SQLAlchemy em mapeamento imperativo, mantendo o domínio limpo, como Caps. 17 e 19
descrevem; migrações com Alembic). Critério prático: quando o número de classes/tabelas e de consultas cresce, ou quando
migrações viram rotina. O ORM continua sendo só mais um adaptador do mesmo contrato.

**Projeto Financeiro:** `cenario.py` com dados fixos e um menu de terminal; a entrega final passa a exigir um ponto de entrada.

**Exercícios:** Nível 1 — nova opção no menu (por exemplo, cancelar pedido); Nível 2 — rodar o cenário duas vezes com
`--banco loja.db` e explicar o que acontece e por quê (produtos duplicados, `Cliente` perdido); Nível 3 — implementar de
verdade o esboço REST com FastAPI e listar o que foi preciso mudar fora das camadas internas; 🚀 Desafio — uma TUI (por exemplo
Textual) ou uma janela Tk chamando os mesmos casos de uso.

**Tarefas de renumeração (só ao escrever):**

- Mover `code/modulo6/capitulo23` → `capitulo24` e depois `capitulo22` → `capitulo23`; criar o novo `capitulo22` a partir de `capitulo21`.
  O novo Cap. 23 (Decorator) passa a partir do snapshot 22 e embrulha também `ListarProdutos`/`ConsultarPedido`. O Cap. 24 acrescenta ao `cenario.py`
  o cenário da última unidade (Ana e Bia).
- `docs/modulo6/capitulo22.md` → `capitulo23.md`, `capitulo23.md` → `capitulo24.md`; corrigir referências internas ("Capítulo 22/23", "Caps. 1 a 23", "20 a 23",
  tabela de padrões, quadro do Cap. 24).
- `mkdocs.yml`, `docs/index.md`, `docs/modulo6/{index,mapa-conhecimento,entrega}.md`, `docs/mapa-conceitos.md`, `.ai/rules/{05,07,08}`: ajustar números e
  acrescentar o capítulo novo; entrega final: exigir ponto de entrada e acrescentar a pergunta "o que no seu sistema **não** está persistido, e o que seria preciso persistir (e ORM?)".
- Cap. 21: trocar o "O que vem a seguir" (gancho passa a ser "como alguém usa o sistema?"). Memória do projeto.

## Arco narrativo

O M5 terminou com `PagarPedido` chamando a notificação explicitamente e com a promessa de que a lista
de reações a um pagamento só cresce (estoque, auditoria, log, financeiro). A dor do M6:
**quem faz não deveria conhecer quem reage**. O módulo troca a lista de chamadas dentro do caso de uso
por *fatos* que o sistema anuncia e *reações* que se inscrevem, e depois mostra como acrescentar
comportamento transversal (log, auditoria) sem editar o que já funciona.

## Ponto de partida (código real do Cap. 19)

- `aplicacao/pagar_pedido.py` chama `ServicoNotificacaoPedido.pedido_pago` diretamente.
- `Produto.quantidade_estoque` existe, mas **nada dá baixa**: a baixa de estoque é funcionalidade nova,
  e é o exemplo natural de reação que não pertence ao `PagarPedido`.
- Não existe auditoria nem log.
- Camadas: `dominio/`, `aplicacao/`, `infraestrutura/`; regra de dependência vigiada por
  `tests/test_arquitetura.py`. Tudo o que for criado tem de respeitá-la.

## Decisões propostas (revisar antes de escrever)

- **Eventos em memória e síncronos**, dentro do mesmo processo. Sem fila, sem broker, sem assíncrono.
  Fila/mensageria é mencionada como "o que viria depois", não implementada.
- **O evento é um fato no passado**, imutável: `PedidoPago`, `PedidoDespachado` (`@dataclass(frozen=True)`
  em `dominio/eventos.py`). Nome no passado × caso de uso no imperativo é o contraste central.
- **Quem publica:** o caso de uso, depois de guardar o pedido (`atualizar`). Alternativa "a entidade
  registra eventos e o caso de uso os publica" é discutida em uma caixa de decisão, não implementada.
- **Barramento (`BarramentoEventos`):** contrato (`publicar`, `inscrever`) na **aplicação** (DIP, Cap. 19);
  implementação em memória na **infraestrutura**; a **raiz de composição** inscreve os manipuladores.
- **Ordem do Observer clássico → eventos:** Cap. 20 mostra o Observer "puro" (sujeito com lista de
  observadores) e o Cap. 21 o evolui para barramento de eventos tipados. Fica claro que o segundo é o
  primeiro com um intermediário.
- **Manipuladores do E-Commerce:** notificação (migra do `PagarPedido`), baixa de estoque, auditoria.
- **Decorator** no Cap. 22 embrulha casos de uso e/ou repositório (log, medição de tempo), em vez de
  novas linhas em `PagarPedido`. Empilhar decoradores é demonstrado.
- **Command com handler** entra como contraste *nominal* no Cap. 22 (comando = intenção, evento = fato),
  sem refatorar os casos de uso inteiros. Completa a nota de nomenclatura do Cap. 18.
- Persistência de auditoria: em memória por padrão; versão SQLite é desafio (a suíte de contrato do M5
  mostra o caminho).

## Capítulos

### Cap. 20 — Quem precisa saber? (Observer)
Gancho: o último parágrafo do Cap. 19. Mostra `PagarPedido` com a nova exigência (baixa de estoque)
e a lista crescendo; contabiliza as dependências do caso de uso. Introduz **Observer** na forma clássica:
sujeito mantém lista de observadores e chama `atualizar`. Aplicado a um objeto simples (não ao `Pedido`
inteiro), para ficar visível a estrutura. Armadilhas: observador que falha, ordem de notificação,
esquecer de cancelar a inscrição. Callbacks em Python (uma função é um observador) como nota.
Projeto Financeiro: observador para alertas de meta estourada.

### Cap. 21 — Fatos, não ordens (eventos de domínio)
Do Observer ao **barramento de eventos**. `PedidoPago` como fato imutável; `BarramentoEventos` na aplicação,
implementação em memória na infraestrutura. `PagarPedido` passa a só pagar, guardar e publicar.
Notificação vira manipulador. Baixa de estoque nasce como manipulador novo, sem tocar no caso de uso
(a prova do módulo, análoga a "o serviço não muda" do Cap. 17). Testes: o caso de uso publica o evento;
cada manipulador é testado sozinho. O teste de arquitetura continua verde.

### Cap. 22 — Embrulhando comportamento (Decorator) e o que é um comando
Log e auditoria sem editar `PagarPedido`: decoradores de caso de uso (mesma interface, delegam ao
embrulhado). Empilhar (log + tempo). Decorator × herança × evento: quando usar cada um (evento reage a
um fato; decorator envolve uma execução). Contraste comando × evento e a forma fiel comando + handler.
Gancho: e se um manipulador falhar?

### Cap. 23 — Quando a reação falha (e o que fica de fora)
Falha em manipuladores: o pagamento já foi confirmado e a baixa de estoque quebra. Estratégias: deixar
propagar, isolar e registrar, tentar de novo (só mencionar). Consistência: por que "pagar" e "dar baixa"
não são atômicos aqui (liga com a transação do Cap. 17). Eventos × testes. Fecho curto sobre padrões
que somem em Python (Strategy vira função, Singleton vira módulo; o Singleton como alerta, substituído
pela raiz de composição). Mapa dos padrões do curso inteiro. Prepara a entrega final.

## Retroativos e desafios (não obrigatórios)

- **State**: trocar a tabela de transições de `StatusPedido` por objetos de estado (nota já existe no Cap. 6).
- **Adapter**: gateway de pagamento externo atrás da porta de pagamento; fecha o vocabulário de Ports & Adapters.
- **Composite**: `Categoria` hierárquica. **Chain of Responsibility**: validação de cupom.
Entram como Nível 3/Desafio nos exercícios, ou ficam de fora. Não cobrir os 23 padrões do GoF.

## Fora de escopo

Mensageria real (RabbitMQ, Kafka), assíncrono (`asyncio`), event sourcing, CQRS completo, sagas,
Unit of Work, ORM na prática. **Framework web:** apenas o esboço de REST do Cap. 22 (texto, não executado); implementação real
fica como exercício ou capítulo bônus.

## Testes (meta, a confirmar na verificação)

Parte-se de 165 (fim do M5). **Verificado:** Cap. 20 = 191, Cap. 21 = 196, Cap. 22 = 204, Cap. 23 = 210.
Cada capítulo com snapshot em `code/modulo6/capituloNN/` (cumulativo; o 20 parte de `code/modulo5/capitulo19/`).

## Projeto Financeiro (paralelo)

Cap. 20: observador de meta estourada. Cap. 21: eventos `LancamentoRegistrado` / `MetaAtingida` e
manipuladores (alerta, notificação). Cap. 22: log/auditoria de importações com decorator. Cap. 23:
falha em alerta não pode impedir o registro do lançamento.

## Entrega final

Substitui o antigo "Módulo 7". Diferente dos checkpoints M2–M5: é a entrega **final** (avaliada pelo conjunto),
cobrindo do Capítulo 1 ao 23. Conteúdo proposto: código organizado nas três camadas, testes (incluindo
arquitetura), eventos com pelo menos dois manipuladores, um decorator, e um **documento** de decisões
(quais padrões usou, quais recusou e por quê; o que mudaria com mensageria real). Apresentação
curta opcional. **A definir com o professor:** peso, formato de apresentação e prazo.

## Consequências para outros arquivos (a fazer junto com a escrita)

- `mkdocs.yml` e `docs/index.md`: nav do Módulo 6 e frase de abertura.
- `.ai/rules/07-curriculum.md`: Módulo 6 detalhado; remover o Módulo 7; mover "Entrega final" para o 6.
- `.ai/rules/08-course-roadmap.md`: aulas 20–23; ajustar "Ordem dos padrões" (Observer já consta; incluir Decorator).
- `.ai/rules/05-domain.md`: eventos e manipuladores no domínio.
- `docs/modulo5/entrega.md` e `docs/modulo{2,3,4}/entrega.md`: trocar "não substitui a entrega final do Módulo 7".
- `docs/modulo6/mapa-conhecimento.md` e atualização de `docs/mapa-conceitos.md`.

## Perguntas em aberto (resolvidas em 2026-11-14)

1. Caps. 20 e 21 ficaram **separados** (Observer clássico, depois barramento). A baixa de estoque nasce como observador no Cap. 20; a auditoria é a "prova" do Cap. 21 (uma reação nova só pela composição).
2. Decorator e comando × evento ficaram **no mesmo capítulo** (22); o comando é só esboçado, sem refatorar os casos de uso.
3. Falha em manipuladores tem **capítulo próprio** (23), que também fecha o curso com o quadro de padrões.
4. Entrega final: pesos propostos (domínio 1,0; variações e criação 1,5; persistência e camadas 2,0; eventos e transversal 2,0; testes 1,5; documento 1,5; organização 0,5) e sugestão de valer o dobro de um checkpoint. **Prazo em aberto.**

## Desvios em relação ao plano original

- A baixa de estoque entrou já no Cap. 20 (como observador), e não no Cap. 21.
- `Aplicacao` (composição) passou a expor `produtos`, `barramento` e `auditoria`, para testes e demonstrações.
- `BarramentoEmMemoria(ao_falhar=...)`: propaga por padrão; a composição isola e registra (log + auditoria).
- Facade foi mantido no roadmap (decisão de 2026-11-14): `ServicoPedido` é reconhecido como Facade no Cap. 15.

## Pendências

- Pontos fracos conhecidos, listados como exercício: nada impede vender produto sem estoque (Cap. 23, Nível 2); `DarBaixaNoEstoque` não é idempotente (Nível 3).
- `site/` não foi regenerado por mim (o `zensical serve` do usuário reconstrói); build limpo em cópia: 11,7 s, sem avisos.
