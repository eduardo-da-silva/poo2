# Plano de Escrita — Módulo 6: Eventos

> Documento de planejamento do Módulo 6. Consultar junto com `.ai/rules/` e
> `.ai/plans/decisoes-pos-modulo5.md`. Descreve **o que** escrever e **em que ordem**;
> não substitui as regras de estilo. **Status: escrito em 2026-11-14** (Caps. 20–23, snapshots em `code/modulo6/`, índice, mapa e entrega final). Prazo da entrega final em aberto (`[DATA A DEFINIR]`); pesos são sugestão.

**Capítulos:** 20 a 23 (o Módulo 5 terminou no Capítulo 19)
**Conceitos:** Observer (publisher/subscriber), eventos de domínio, Decorator, Command × evento, falha em reações
**Entrega:** **entrega final** do Projeto Financeiro (`docs/modulo6/entrega.md`). Não há Módulo 7:
a entrega final migrou para cá (ver `decisoes-pos-modulo5.md`).

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
Unit of Work, framework web, ORM na prática.

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
