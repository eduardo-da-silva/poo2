# Plano de Escrita — Módulo 5: Organização do Sistema

> Documento de planejamento do Módulo 5. Consultar junto com `.ai/rules/`.
> Descreve **o que** escrever e **em que ordem**; não substitui as regras de estilo.

**Capítulos:** 16 a 19 (o Módulo 4 terminou no Capítulo 15)
**Conceitos:** Repository, persistência (SQLite, sem ORM), camadas, casos de uso, inversão de dependências
**Entrega:** sim — `docs/modulo5/entrega.md` (checkpoint formativo, nos moldes de M2–M4)

## Arco narrativo

O M4 terminou com o grafo de objetos montado numa raiz de composição, mas tudo vive em memória e
a coordenação (`ServicoPedido`) mora misturada ao domínio. A dor do M5: **o sistema precisa lembrar,
e o domínio não pode saber onde**. Os quatro capítulos separam *o que o sistema é* de *onde e como
ele guarda e entrega as coisas*.

## Decisões tomadas

- Persistência com `sqlite3` da biblioteca padrão, mapeamento manual, **sem ORM**.
- O ORM é apresentado como alternativa no Cap. 17 (onde afetaria o código e por que a troca é
  barata) e retomado no Cap. 19 (o que a regra de dependência garante).
- Persistimos `Produto` e `Pedido` (itens + status). `Pagamento`, `Entrega` e `Cupom` ficam
  **fora** da persistência de propósito — dívida visível, vira desafio (Nível 3) no Cap. 17.
- `Cliente` não é persistido (o `Pedido` ainda não referencia o cliente).
- Identidade: `Produto.id` / `Pedido.id`, atribuídos uma única vez pelo repositório (`atribuir_id`).
- Contrato de repositório testado por uma suíte única, parametrizada por implementação
  (`conftest.py` com a fixture `infra`: memória e SQLite).
- O `ServicoPedido` do M4 é substituído por casos de uso no Cap. 18.
- A regra de dependência é verificada por teste automatizado (`tests/test_arquitetura.py`),
  que nasce com uma violação conhecida (`xfail`) no Cap. 18 e passa no Cap. 19.

## Capítulos

### Cap. 16 — O sistema precisa lembrar (Repository)
Problema: pedidos e produtos só existem enquanto o script roda e são passados de mão em mão.
Introduz identidade (`id`), `RepositorioProduto` / `RepositorioPedido` (ABC) e as implementações
em memória. `ServicoPedido` passa a receber `pedido_id`. Armadilha: o repositório em memória
devolve a *mesma* referência — `atualizar` parece inútil. Projeto Financeiro: repositório de lançamentos.
Testes: 137.

### Cap. 17 — Guardando de verdade (SQLite)
Segunda implementação do mesmo contrato (`RepositorioProdutoSQLite`, `RepositorioPedidoSQLite`),
esquema, mapeamento linha↔objeto, `Pedido.reconstituir`. O serviço não muda. A mesma suíte roda
nas duas implementações; agora o `atualizar` esquecido aparece. Seção "E o ORM?". Testes: 154.

### Cap. 18 — Casos de uso e camadas
`dominio/`, `aplicacao/`, `infraestrutura/`. `ServicoPedido` vira `CadastrarProduto`,
`FinalizarCompra`, `PagarPedido`, `DespacharPedido`. `composicao.py` como raiz de composição.
Teste de arquitetura com uma violação conhecida (aplicação importa infraestrutura). Testes: 160 + 1 xfail.

### Cap. 19 — Quem depende de quem? (Inversão de dependências)
Regra de dependência; a porta `Notificacao`/`FabricaNotificacao` sobe para a aplicação, a infra passa
a depender dela. O `xfail` vira teste verde. Trocar memória × SQLite × (ORM) é mudança só na
composição. Fecha o módulo. Testes: 165.

## Fora de escopo

Observer/eventos (M6), ORM na prática, framework web, Facade, persistência de pagamento/entrega/cupom,
transações entre repositórios (unit of work).

## Projeto Financeiro (paralelo)

Cap. 16: repositório de lançamentos em memória. Cap. 17: versão SQLite + suíte de contrato.
Cap. 18: casos de uso (importar extrato, gerar relatório) e camadas. Cap. 19: regra de dependência
e raiz de composição.
