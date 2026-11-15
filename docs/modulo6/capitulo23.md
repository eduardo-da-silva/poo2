# Capítulo 23 — Quando a reação falha

!!! info "Situação da Empresa"

    Na sexta à noite, a loja anunciou uma promoção de um notebook com **uma única unidade**. Duas pessoas, Ana e Bia, colocaram o produto no carrinho com poucos segundos de diferença. As duas finalizaram a compra, e o sistema criou os dois pedidos sem reclamar.

    Ana pagou. Bia pagou logo depois. Na tela de Bia apareceu uma mensagem de erro. Mas o banco dela mostrava o pagamento aprovado.

O Capítulo 20 deixou este cenário registrado em teste, como dívida. Chegou a hora de pagá-la, e de entender por que o problema é mais sutil do que parece.

---

## O que aconteceu, passo a passo

O estoque tinha uma unidade. Ana pagou, e a baixa a reduziu a zero. Quando Bia paga, o `PagarPedido` faz o que sempre fez, e depois publica `PedidoPago`. O barramento entrega o evento aos manipuladores **na ordem de inscrição**:

| Passo | O que acontece | Estado depois |
|---|---|---|
| 1 | O pedido de Bia é confirmado e **guardado como pago** | Pedido: pago |
| 2 | `NotificarClienteDoPagamento` avisa Bia: "pagamento confirmado" | Bia foi avisada de que está tudo certo |
| 3 | `DarBaixaNoEstoque` tenta tirar uma unidade e lança `EstoqueInsuficienteError` | Estoque: 0, e a baixa não foi feita |
| 4 | O erro sobe pelo barramento, pelo `PagarPedido`, e chega a quem chamou | Bia vê uma mensagem de erro |
| 5 | `RegistrarAuditoria` **nunca roda** | Nenhuma trilha do pagamento de Bia |

O sistema contou **três versões** da mesma história: o banco de dados diz "pago", a notificação diz "confirmado", e a tela diz "erro". Nenhuma delas está errada sozinha. O problema é que o erro de uma *reação* foi tratado como erro do *fato*.

---

## 🧠 Pense

1. O pagamento de Bia aconteceu. Se a baixa de estoque falhou, o **pagamento** deveria ser desfeito? Quem decide isso: o estoque ou a regra de pagamento?
2. A falta de estoque é um problema da **reação** ou do **fato**? Em que momento do fluxo ela deveria ter sido percebida?
3. Se a auditoria não rodou, alguém ficará sabendo que existe um pedido pago sem estoque baixado?

---

## Três posturas diante de uma reação que falha

Não existe uma resposta única. Existem três posturas, e cada uma faz sentido em um tipo de situação:

| Postura | O que faz | Quando usar |
|---|---|---|
| **Propagar** | O erro sobe, os manipuladores seguintes não rodam | Quando a reação **faz parte** da operação: se falhou, o fato não deveria valer. É o comportamento que o barramento tem hoje |
| **Isolar e registrar** | Cada manipulador falha sozinho; o erro é anotado; os outros continuam | Quando o fato **já é verdade** e as reações são independentes entre si |
| **Repetir ou compensar** | Tentar de novo mais tarde, ou desfazer o efeito | Quando a reação precisa acontecer de qualquer jeito. Exige cuidados extras, e fica fora deste curso |

Pagamento confirmado é um **fato consumado**: o dinheiro já saiu da conta de Bia. A notificação, a baixa e a auditoria são reações a ele. A segunda postura é a que se encaixa.

---

## Isolar: o barramento aprende a falhar

A mudança é pequena e fica na implementação do barramento, que ganha uma função opcional, `ao_falhar`, chamada quando um manipulador lança uma exceção:

```python title="ecommerce/infraestrutura/barramento_em_memoria.py" linenums="1" hl_lines="1 3 9-10 17-23"
AoFalhar = Callable[[object, Manipulador, Exception], None]


class BarramentoEmMemoria(BarramentoEventos):
    """Entrega cada evento, na hora e no mesmo processo, a quem se inscreveu no seu tipo.

    Sem `ao_falhar`, o erro de um manipulador sobe para quem publicou e os manipuladores
    seguintes nao rodam. Com `ao_falhar`, o erro e entregue a essa funcao e os
    seguintes continuam: uma reacao que falha nao derruba as outras.
    """

    def __init__(self, ao_falhar: AoFalhar | None = None) -> None:
        self._manipuladores: dict[type, list[Manipulador]] = {}
        self._ao_falhar = ao_falhar

    def publicar(self, evento: object) -> None:
        for manipulador in list(self._manipuladores.get(type(evento), [])):
            try:
                manipulador(evento)
            except Exception as erro:
                if self._ao_falhar is None:
                    raise
                self._ao_falhar(evento, manipulador, erro)
```

O comportamento **padrão** continua sendo propagar: quem criar um barramento sem `ao_falhar` não terá nenhuma falha engolida sem ter pedido por isso. O isolamento é uma escolha explícita, e quem escolhe é a raiz de composição.

O que fazer com a falha isolada? **Registrar**, para que alguém olhe depois. A raiz de composição passa uma função que escreve duas vezes: no log e na auditoria.

```python title="ecommerce/composicao.py" linenums="1"
    def registrar_falha(evento: object, manipulador: Manipulador, erro: Exception) -> None:
        # O fato ja aconteceu: a falha de uma reacao nao desfaz o pagamento.
        # Fica registrada para alguem olhar depois.
        mensagem = (
            f"FALHA: {_nome_de(manipulador)} nao tratou {type(evento).__name__} "
            f"({type(erro).__name__}: {erro})"
        )
        auditoria.registrar(mensagem)
        registrar(mensagem)

    barramento = BarramentoEmMemoria(ao_falhar=registrar_falha)
```

Agora o cenário de Ana e Bia, em um teste que roda nas duas configurações de armazenamento:

```python title="tests/test_composicao.py" linenums="1"
@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_falha_na_baixa_de_estoque_nao_desfaz_o_pagamento_nem_impede_as_outras_reacoes(
    armazenamento: str,
) -> None:
    app = montar_aplicacao(armazenamento, registrar=lambda linha: None)
    ultimo = app.cadastrar_produto.executar("Notebook", 3500.0, 1, "Informática")
    # ... Ana e Bia, cada uma com o notebook no carrinho, cada uma com seu pedido ...

    app.pagar_pedido.executar(pedido_da_ana.id, ana)
    app.pagar_pedido.executar(pedido_da_bia.id, bia)  # a ultima unidade ja foi

    assert app.produtos.obter(ultimo.id).quantidade_estoque == 0
    entradas = app.auditoria.entradas()
    assert f"PedidoPago: pedido {pedido_da_bia.id}, cliente Bia" in entradas
    falhas = [e for e in entradas if e.startswith("FALHA")]
    assert len(falhas) == 1
    assert "DarBaixaNoEstoque" in falhas[0]
    assert "EstoqueInsuficienteError" in falhas[0]
```

O pagamento de Bia **não gera erro** para quem chamou; a **auditoria** registrou o pagamento (o manipulador que vinha depois da falha rodou); e a trilha tem uma linha de `FALHA` dizendo qual reação não conseguiu tratar qual evento, e por quê. Alguém, olhando a auditoria, consegue descobrir que existe um pedido pago sem baixa.

E o barramento, sozinho, é testado nas duas posturas:

```python title="tests/infraestrutura/test_barramento_em_memoria.py" linenums="1"
def test_sem_ao_falhar_o_erro_sobe_e_os_seguintes_nao_rodam() -> None: ...

def test_com_ao_falhar_os_seguintes_continuam() -> None: ...

def test_ao_falhar_recebe_o_evento_o_manipulador_e_o_erro() -> None: ...
```

```bash
$ pytest tests/
```

??? tip "210 testes passando"

    Os 204 do capítulo anterior continuam verdes. Entraram quatro testes do barramento (propagar, isolar, o que `ao_falhar` recebe, e que os manipuladores anteriores à falha já rodaram) e o teste de ponta a ponta de Ana e Bia, que roda com memória e com SQLite.

!!! info "🏗️ Decisão de Projeto — quem escolhe entre propagar e isolar?"

    A escolha é da **raiz de composição**, não do `PagarPedido` e nem do barramento. O caso de uso só publica. O barramento oferece as duas posturas. Quem monta o sistema decide qual delas faz sentido **para aquele sistema**: em produção, isolar e registrar; em testes que precisam enxergar o erro de uma reação, o barramento padrão, que propaga.

---

## O que ainda não está resolvido

Isolar a falha impediu que o erro contaminasse tudo. Mas o problema de fundo continua: **o pagamento e a baixa não acontecem juntos**. Existe uma janela em que o pedido está pago e o estoque ainda não baixou, e, no caso da falha, essa janela nunca se fecha sozinha.

Isso liga com o que você viu no Capítulo 17. Cada repositório guarda suas mudanças em uma transação própria: o `atualizar` do pedido foi confirmado (`COMMIT`) antes de o primeiro manipulador ser chamado. Não há uma transação abrangendo as duas coisas. É o que se chama de **consistência eventual**: o sistema, por algum tempo, fica em um estado em que as partes não concordam, e depende de algo para voltar a concordarem.

Três observações para sair do capítulo com o quadro completo:

- **A falha deve ser vista.** A linha `FALHA` na auditoria só ajuda se alguém lê. Num sistema real, ela dispararia um alerta ou entraria numa lista de pendências para reprocessar.
- **Repetir não é de graça.** Imagine que alguém decida reprocessar o evento de Bia depois de repor estoque. O `DarBaixaNoEstoque` **não é idempotente**: rodá-lo duas vezes sobre o mesmo evento dá baixa duas vezes. Para repetir com segurança, um manipulador precisa conseguir reconhecer que já tratou aquele evento. É uma propriedade que se projeta, não que aparece sozinha.
- **O erro de verdade está antes.** A causa do problema de Bia não é um manipulador: é o sistema ter aceitado **vender o que não tinha**. Nem `Carrinho` nem `FinalizarCompra` verificam o estoque. Um evento de falha é um remendo; a regra "não aceite pedidos sem estoque" pertence ao domínio, no momento da compra. Esse é o exercício de Nível 2.

!!! warning "⚠️ Erro comum — isolar para esconder"

    Isolar a falha e registrá-la em um lugar que ninguém olha é o mesmo que ignorá-la. A decisão de isolar só é boa **junto com** a decisão de quem vai ver o registro e o que fazer com ele.

!!! warning "⚠️ Erro comum — usar eventos para o que precisa ser atômico"

    Se duas coisas **precisam** acontecer juntas ou nenhuma (por exemplo, debitar uma conta e creditar outra), elas não devem ser ligadas por um evento. Evento é para o que vem **depois** de um fato consumado. O que precisa ser atômico pertence à mesma transação, dentro do mesmo caso de uso.

---

## Padrões que "somem" em Python

O módulo apresentou o Observer em dois momentos, e logo na primeira versão apareceu uma pista: em Python, o observador podia ser uma **função**. Essa é uma regra mais geral. Vários padrões que, em linguagens como Java, exigem várias classes, se reduzem em Python a algo muito menor:

| Padrão | Em linguagens com classes obrigatórias | Em Python |
|---|---|---|
| **Strategy** | Interface + uma classe por estratégia | Uma **função**: `desconto: Callable[[float], float]`. As classes continuam úteis quando a estratégia tem estado ou vários métodos |
| **Observer / Command** | Interface + classe por observador | Uma função ou um objeto com `__call__`, como nossos manipuladores |
| **Factory** | Classe fábrica | A própria **classe** é um objeto que se chama; um dicionário `{canal: classe}` substitui o `if/elif` |
| **Decorator** | Classes embrulhando classes | Existe sintaxe própria, `@decorador`, para embrulhar **funções** |
| **Singleton** | Classe com construtor privado e instância estática | Um **módulo**: ele é carregado uma única vez, e seus objetos são únicos |

O quadro **não** diz que as classes que escrevemos estavam erradas. Ele diz que, quando um papel se reduz a "algo que se chama", o mais simples é muitas vezes uma função. Escolhemos classes onde o papel tinha nome, dependências ou estado, como `NotificarClienteDoPagamento`.

O **Singleton** merece um alerta à parte. Ele é um padrão famoso, e é quase sempre uma armadilha: uma instância global é uma dependência escondida, que qualquer código alcança sem declarar. A **raiz de composição** do Capítulo 15 resolve o que ele prometia (uma só instância, compartilhada) **sem** a parte nociva: quem precisa de algo o recebe pelo construtor.

---

## Os padrões do curso, em um quadro

Este quadro reúne o que o curso apresentou e o problema real que cada padrão resolveu no E-Commerce:

| Padrão | Capítulo | Problema que resolveu | O que o sistema ganhou |
|---|---|---|---|
| **Strategy** | 9 | Regras de desconto que mudam | Acrescentar uma regra sem tocar no `Pedido` |
| **Simple Factory** | 12 | `if/elif` de criação espalhado | A criação em um só lugar |
| **Template Method** | 12 | Pagamentos com o mesmo roteiro e passos diferentes | O roteiro fixo, e só o passo variável nas subclasses |
| **Factory Method** | 13 | Escolher o meio de entrega | Quem usa a entrega não conhece a classe concreta |
| **Facade** | 15 | Fluxo que coordena várias peças | Um caminho curto: `servico.pagar(...)` |
| **Injeção de Dependências** | 15 | Objetos que criavam suas próprias dependências | Dependências recebidas de fora e trocáveis nos testes |
| **Repository** | 16 | Dados presos à memória | Domínio que não sabe onde os dados ficam |
| **Data Mapper** | 17 | Traduzir objeto ↔ tabela | Mapeamento fora do domínio |
| **Ports & Adapters** | 19 | Detalhes técnicos misturados ao negócio | Contratos do lado de quem usa; detalhes trocáveis |
| **Observer** | 20 | Um caso de uso conhecendo todo mundo que reage | Reações acrescentadas sem abrir o caso de uso |
| **Publish/Subscribe** | 21 | Lista de observadores repetida; aviso sem nome | Fatos com nome e um único ponto de assinatura |
| **Decorator** | 22 | Log e tempo dentro de cada caso de uso | Comportamento transversal em volta, sem editar |

Perceba o fio comum: **cada padrão apareceu quando o código mostrou uma dor**. Nenhum foi aplicado por antecipação, e nenhum deles é a resposta para uma pergunta que ainda não foi feita.

### O que ficou de fora

Este curso não cobre os 23 padrões do GoF, e nem pretende. Alguns que seguiriam naturalmente o que construímos, e que você pode explorar como desafio:

- **State**: `StatusPedido` é uma tabela de transições; transformar cada estado em um objeto com comportamento próprio é o padrão State.
- **Adapter**: um gateway de pagamento externo, de outro fornecedor, atrás da porta de pagamento. Completaria o vocabulário de Ports & Adapters.
- **Composite**: `Categoria` com subcategorias.
- **Chain of Responsibility**: validações em sequência, como as de um cupom.

---

## 🧩 Aplicando ao Projeto Financeiro

1. Provoque a falha: faça o alerta de meta estourada lançar uma exceção. O que acontece hoje com o registro do lançamento? Ele fica registrado? O erro sobe?
2. Escolha uma postura (propagar ou isolar) para o seu sistema e **justifique por escrito**. Se escolheu isolar, onde o erro fica registrado, e quem vai olhar?
3. Veja se há algo no seu sistema que **precisa** ser atômico e que você ligou por um evento. Se houver, o que faria diferente?

Este é o último capítulo antes da entrega final. Revise o seu sistema com o quadro de padrões acima: para cada padrão que você usou, qual dor ele resolveu? Para cada um que você **não** usou, por que não era necessário?

---

## 🎯 Exercícios

**Nível 1.** Escreva um teste em que dois manipuladores falham no mesmo evento e um terceiro, depois deles, funciona. Quantas chamadas a `ao_falhar` acontecem? O terceiro rodou?

**Nível 2.** Corrija a causa do problema de Bia: faça `FinalizarCompra` recusar um pedido cujo item excede o estoque, lançando `EstoqueInsuficienteError`. O que acontece com o caso de duas pessoas que finalizam a compra da **última unidade** antes de qualquer pagamento? A verificação na compra resolve esse caso? Se não, o que seria necessário (uma reserva)?

**Nível 3.** Torne o `DarBaixaNoEstoque` idempotente: ele deve reconhecer um evento que já tratou e não dar baixa de novo. Onde você guardaria essa informação? O que isso diz sobre o evento (ele precisa de um identificador)?

**🚀 Desafio.** Implemente um `ReprocessarFalhas` que leia as linhas `FALHA` da auditoria e tente tratar o evento de novo. O que o evento precisaria carregar para isso ser possível?

---

## 📌 Resumo

- Uma reação que falha, se o erro subir, faz o **fato** parecer ter falhado: o pagamento está guardado, mas o chamador vê um erro, e as reações seguintes não rodam
- Há três posturas: **propagar** (a reação faz parte da operação), **isolar e registrar** (o fato já é verdade) e **repetir ou compensar** (precisa acontecer de qualquer jeito)
- O barramento propaga por padrão; com `ao_falhar`, isola, e **quem escolhe é a raiz de composição**
- Isolar só é bom se a falha for **registrada e vista**
- Fato e reações não são atômicos: o sistema fica, por um tempo, em **consistência eventual**
- Repetir exige manipuladores **idempotentes**; `DarBaixaNoEstoque` ainda não é
- A causa de verdade do problema de Bia é a regra de estoque ausente na compra: um evento de falha é um remendo
- Em Python, vários padrões se reduzem a funções; o Singleton é um alerta, substituído pela raiz de composição
- Cada padrão do curso apareceu **depois** de uma dor concreta, nunca antes

## O que mudou no sistema

- ✔ A falha de uma reação não derruba as outras nem faz o pagamento parecer ter falhado
- ✔ A falha fica registrada na auditoria e no log
- ✔ Raiz de composição decide a postura diante de falhas
- ❌ Nada impede a venda de um produto sem estoque
- ❌ `DarBaixaNoEstoque` não é idempotente
- ❌ Ninguém é avisado das linhas de `FALHA`; elas só existem no registro

## O que vem a seguir

O Módulo 6 termina aqui, e com ele a parte de conteúdo do curso. O E-Commerce cria seus objetos com cuidado, guarda dados atrás de contratos, se organiza em camadas, anuncia fatos, reage a eles e se deixa observar. O que resta é consolidar: [a entrega final do Projeto Financeiro](entrega.md), que reúne tudo o que foi construído do Capítulo 1 ao 23.
