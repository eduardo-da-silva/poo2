# Decisões e pendências pós-Módulo 5

> Notas de planejamento (2026-11-08). Nada aqui foi escrito nos capítulos ainda.
> Retomar antes de planejar o Módulo 6. Consultar junto com `.ai/rules/`.

## Decisões

- **Módulo 7 (Refatoração) não será feito.** Os conceitos (SOLID, refatoração, code smells) já foram
  tratados ao longo do curso. O `mapa-conceitos.md` já tem a seção de SOLID.
- **Consequência a resolver:** a entrega final do Projeto Financeiro (hoje prevista para o Módulo 7)
  precisa migrar para o fim do Módulo 6. Atualizar `.ai/rules/07-curriculum.md`, `08-course-roadmap.md`
  e as páginas `entrega.md` (que dizem "não substitui a entrega final do Módulo 7").
- **Módulo 6 (Eventos)** continua sendo o próximo; o Cap. 19 já termina no gancho (`PagarPedido`
  acumulando reações).

## Ajustes de nomenclatura nos Módulos 1–5 (a aplicar)

- **Repository (Cap. 16):** já é nomeado como conceito; passar a chamá-lo explicitamente de *padrão*,
  como Strategy e Factory.
- **Use cases (Cap. 18):** não chamar de Command. Nota dizendo que o design é um *parente simplificado*
  do Command: nossos use cases não carregam dados (colaboradores no construtor, parâmetros em
  `executar`). A forma fiel é comando (dados) + handler, como em CQRS. Prepara o Módulo 6
  (comando = intenção; evento = fato ocorrido). O nome adequado hoje é *Application Service* / *Interactor*.
- **Data Mapper (Cap. 17):** os repositórios SQLite fazem mapeamento manual + `Pedido.reconstituir`.
  Nomear e contrastar com Active Record (o que um ORM como o do Django faz).
- **Ports & Adapters (Cap. 19):** `FabricaNotificacao` e os repositórios abstratos são portas;
  implementações SQLite/memória/e-mail/SMS são adaptadores. Já descrito sem o vocabulário.
- **State:** `StatusPedido` é tabela de transições (máquina de estados), não o padrão State.
  Não confundir nem nomear como State sem refatorar.
- **Facade (decidido em 2026-11-14):** fica na lista. O `ServicoPedido` (Caps. 15–17) é reconhecido como Facade
  por nota no Cap. 15; o Cap. 18 explica que a fachada, ao crescer, se desfaz em casos de uso. Feito.

## Padrões que ficam de fora (candidatos, por prioridade)

1. **Decorator** — encaixa no Módulo 6: log/auditoria embrulhando use case ou repositório, em vez de
   mais linhas em `PagarPedido`; também empilhar descontos.
2. **State** — `Pedido` tem estados desde o Módulo 2; objetos de estado no lugar da tabela de transições.
3. **Adapter** — gateway de pagamento externo; fecha o vocabulário de Ports & Adapters.
4. **Composite** — `Categoria` hierárquica.
5. **Command** (com dados + handler) — junto do Módulo 6.
6. **Builder, Chain of Responsibility, Singleton** — Singleton como alerta (a raiz de composição o
   substitui); Chain para validação de cupom.

Plano provável: Módulo 6 com Observer + Decorator + Command/Handler; State e Adapter como retroativos
ou desafios. Fecho curto sobre padrões que "somem" em Python (Strategy vira função, Singleton vira módulo).
Não cobrir os 23 padrões do GoF.

## Pendências técnicas

- ~~`_TRANSIcoES_VALIDAS` em `status_pedido.py`~~ **Corrigido em 2026-11-15** para `_TRANSICOES_VALIDAS` em todos os snapshots (Módulos 2 a 6) e no Cap. 6. Todas as suítes passam.
- `site/` não foi regenerado com `mkdocs build` (mkdocs não instalado neste ambiente).
- ~~Rodar as suítes de `code/modulo5/capitulo16..19`~~ Rodadas em 2026-11-15 (137 / 154 / 160+1 xfail / 165), junto com as dos demais módulos.
- `slides/avaliacao-01-revisao.html` está solto, fora do `mkdocs.yml`.
