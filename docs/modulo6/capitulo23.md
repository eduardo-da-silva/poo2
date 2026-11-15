# Capítulo 23 — Bônus: padrões que ficaram de fora

!!! info "Situação da Empresa"

    O sistema está de pé, e a diretoria viu a demonstração. Na saída, o gerente fez uma pergunta que o time não esperava: "Eu li que existem vinte e poucos padrões de projeto. A gente usou uns oito ou dez. O resto não serve para nada?"

    A resposta honesta é: serve, quando há uma dor que ele resolve. A nossa não pediu os outros.

Este capítulo é um **bônus**. Ele não traz código novo para o E-Commerce nem exercícios. É um **mapa**: para cada padrão que ficou de fora, mostra a dor que ele resolveria, onde ele entraria no nosso sistema e no seu Projeto Financeiro, e quando **não** vale a pena usá-lo. Os detalhes de implementação ficam por conta da sua pesquisa, e isso é de propósito.

---

## Como usar este capítulo

Na [entrega final](entrega.md), **15% da nota** (proposta de 1,5 ponto) vem de um padrão que **você escolhe neste catálogo, pesquisa e implementa** no seu Projeto Financeiro. As regras, em resumo:

- A escolha é entre os sete padrões abaixo: **Decorator, State, Adapter, Composite, Chain of Responsibility, Command com handler e Builder**. Outro padrão só com aprovação prévia do professor.
- O padrão precisa resolver uma **dor real do seu projeto**. Aplicar um padrão onde não havia problema, só para pontuar, vale menos do que escolher um que resolve algo e explicar bem.
- Você implementa, **testa**, e no documento de decisões explica o que pesquisou, o que adaptou ao seu caso, o **custo** que o padrão trouxe e por que escolheu este e não outro da lista.

Para decidir, use a mesma ordem do curso inteiro: **primeiro a dor, depois o padrão**. Antes de ler o catálogo, procure no seu projeto por três sintomas:

1. Algum `if/elif` cresce a cada nova regra?
2. Alguma classe acumula responsabilidades que não são dela?
3. Alguma mudança pequena obriga a editar muitos arquivos?

O que você achar vai apontar, quase sempre, para um dos padrões abaixo.

---

## O catálogo

Cada padrão tem o mesmo roteiro: a dor, como o padrão resolveria, onde entraria, quando **não** usar, e uma ideia para o Projeto Financeiro.

### 1. Decorator

**A dor.** Queremos acrescentar algo *em volta* de uma operação (log, medição de tempo, tentar de novo se falhar) sem editar a operação, e sem repetir o mesmo bloco em cada caso de uso. Um evento não serve: ele só enxerga o que acontece **depois** de um fato, e não o início, a falha ou a duração.

**Como resolveria.** Um objeto **embrulha** outro de mesma interface, faz algo antes e/ou depois e delega o trabalho. Como o decorador tem a interface do embrulhado, as capas se empilham.

```python
class ComLog:
    def __init__(self, caso_de_uso, registrar): ...
    def executar(self, *args, **kwargs):
        registrar("inicio"); resultado = self._caso_de_uso.executar(*args, **kwargs)
        registrar("fim"); return resultado
```

**Onde entraria.** Em `composicao.py`: `pagar_pedido = ComLog(PagarPedido(...), registrar)`. O `PagarPedido` não muda. A variante para repositórios (um `RepositorioPedido` com cache ou com log, de mesma interface) é muito comum.

**Quando não usar.** Quando o comportamento extra é uma **reação a um fato** (use evento), ou específico de um único caso de uso (acrescente na própria classe). Cuidado com o decorador que engole exceções ou que não devolve o resultado do embrulhado.

**No Projeto Financeiro.** Log e medição de tempo da importação de extrato; contagem de lançamentos importados.

!!! tip "Código de referência"

    Uma implementação completa e testada, com `ComLog`, `ComTempo` (relógio injetado) e empilhamento, está em `code/modulo6/bonus-decorator/`. Ela não faz parte do caminho principal do curso: é um ponto de partida para você ler, e não para copiar.

### 2. State

**A dor.** O `StatusPedido` é uma **tabela de transições**: um dicionário diz quais mudanças são válidas. Quando cada estado passa a ter *comportamento* diferente (cancelar um pedido pago estorna o pagamento; cancelar um pedido já enviado é recusado; cancelar um pedido criado só muda o status), o `Pedido` se enche de `if self._status == ...`.

**Como resolveria.** Cada estado vira um **objeto** com seu próprio comportamento (`EstadoCriado`, `EstadoPago`, `EstadoEnviado`...). O `Pedido` guarda o estado atual e **delega** a ele: `self._estado.cancelar(self)`.

```python
class EstadoPago:
    def cancelar(self, pedido):
        pedido.estornar_pagamento()
        pedido.mudar_para(EstadoCancelado())
```

**Onde entraria.** Em `dominio/`, substituindo `status_pedido.py`. A persistência mapeia o estado para o texto que já guardamos (`"pago"`), e o `Pedido.reconstituir` escolhe a classe certa.

**Quando não usar.** Com poucos estados e regras simples, a tabela basta e é mais fácil de ler. O State compensa quando o comportamento muda de estado para estado, não só as transições permitidas.

**No Projeto Financeiro.** O ciclo de vida de uma meta (ativa, atingida, estourada, encerrada) ou de um lançamento (pendente, conciliado, estornado).

### 3. Adapter

**A dor.** Precisamos usar algo que **já existe**, com uma interface que não é a nossa: um gateway de pagamento de um fornecedor externo, por exemplo, que fala em centavos, exige um *token* e devolve códigos de erro próprios. Se o resto do sistema passar a falar a língua do fornecedor, a dependência se espalha.

**Como resolveria.** Uma classe pequena **traduz** a interface externa para o contrato que a aplicação define, e só ela conhece o fornecedor.

```python
class PagamentoViaGateway(Pagamento):
    def confirmar(self):
        resposta = self._gateway.cobrar(centavos=int(self._valor * 100), token=self._token)
        self._situacao = traduzir(resposta)
```

**Onde entraria.** Em `infraestrutura/`, implementando a porta de pagamento. Os casos de uso continuam falando com `Pagamento`. É o que fecha o vocabulário de **Ports & Adapters** do Capítulo 19: nele "adaptador" é um termo geral, e o *Adapter* do GoF é a forma específica de traduzir uma interface existente para outra esperada.

**Quando não usar.** Quando você controla as duas pontas, basta ajustar uma delas. O Adapter é para o que você **não pode** (ou não quer) mudar.

**No Projeto Financeiro.** Leitores de extrato de bancos diferentes (um entrega CSV, outro OFX, outro uma API), todos atrás de um `LeitorExtrato` que devolve lançamentos do seu domínio.

### 4. Composite

**A dor.** Queremos tratar **uma parte** e **um conjunto de partes** da mesma forma. A `Categoria` hoje é plana. Quando surgem as subcategorias (Informática, dentro dela Periféricos, dentro dela Mouses), "qual o total vendido em Informática?" precisa somar tudo o que está abaixo, em qualquer profundidade.

**Como resolveria.** Folhas e nós compartilham a mesma interface (`total_vendido()`). O nó guarda filhos e delega a eles; quem chama não precisa saber se está diante de uma folha ou de uma árvore.

```python
class CategoriaComposta:
    def total_vendido(self):
        return sum(filha.total_vendido() for filha in self._filhas)
```

**Onde entraria.** Em `dominio/`, na `Categoria`; a persistência ganha uma coluna de "categoria pai" e a leitura reconstrói a árvore.

**Quando não usar.** Se a hierarquia tem profundidade fixa (sempre dois níveis), duas classes simples resolvem sem a recursão.

**No Projeto Financeiro.** Categorias de lançamentos (Alimentação, e dentro dela Restaurantes e Mercado): o gasto da categoria pai é a soma das filhas. É, provavelmente, o encaixe mais natural do catálogo.

### 5. Chain of Responsibility

**A dor.** Uma decisão passa por **vários critérios em sequência**, cada um podendo resolver ou deixar passar. A validação de um cupom é um bom exemplo: expirado? valor mínimo atingido? já usado? vale para esta categoria? Em um único método, vira uma escada de `if`.

**Como resolveria.** Cada critério é um **elo** que decide ou repassa ao próximo. Acrescentar ou reordenar um critério é montar a corrente de outro jeito.

```python
class ValidaValorMinimo:
    def validar(self, cupom, pedido):
        if pedido.calcular_total() < cupom.minimo:
            raise ValueError("valor minimo nao atingido")
        self._proximo.validar(cupom, pedido)
```

**Onde entraria.** Em `dominio/`, no `Cupom`; a montagem da corrente fica na raiz de composição ou numa factory.

**Quando não usar.** Em Python, uma **lista de funções** percorrida por um `for` costuma bastar e é bem mais curta. A corrente de objetos compensa quando cada elo tem estado, dependências ou decide **parar** o processo de formas diferentes. Não confunda com o Strategy, que escolhe **uma** alternativa; aqui várias podem agir em sequência.

**No Projeto Financeiro.** A categorização automática de lançamentos: uma regra por descrição ("UBER" é transporte), outra por valor, e uma final que classifica como "Outros".

### 6. Command com handler

**A dor.** Nossos casos de uso recebem parâmetros soltos (`executar(pedido_id, cliente, forma)`). Queremos tratar **a intenção como um dado**: guardá-la, enfileirá-la, registrá-la, ou até **desfazê-la**. E queremos uma assinatura uniforme (`executar(comando)`) para todos os casos de uso.

**Como resolveria.** O **comando** é um objeto de dados imutável ("pagar o pedido 12 com Pix"), e o **handler** é quem o executa. É a forma fiel do padrão, de que os nossos casos de uso são um parente simplificado, como os Capítulos 18 e 21 explicaram.

```python
@dataclass(frozen=True)
class PagarPedidoComando:
    pedido_id: int
    forma: FormaPagamento = FormaPagamento.PIX
```

**Onde entraria.** Em `aplicacao/`: cada caso de uso ganha um comando e um handler. A entrada (menu, REST) monta o comando a partir do que recebe.

**Quando não usar.** Quando não há ganho em tratar a intenção como dado. Mais uma classe por operação é um custo real, e sem fila, histórico ou desfazer, ele é pura cerimônia. Variações maiores, como separar comandos de consultas em modelos diferentes (CQRS), ficam fora deste curso.

**No Projeto Financeiro.** `RegistrarLancamentoComando` com a possibilidade de **desfazer** o último lançamento, guardando os comandos executados.

### 7. Builder

**A dor.** Construir um objeto exige muitos passos ou muitas combinações opcionais, e o construtor vira uma lista de parâmetros difícil de ler. Isso aparece com força em **testes**: montar um `Pedido` pago, com cupom, com três itens, em cada teste.

**Como resolveria.** Um objeto à parte acumula as escolhas passo a passo e devolve o resultado no fim.

```python
pedido = (UmPedido().com_item(notebook, 1).com_cupom("PROMO10").pago().construir())
```

**Onde entraria.** Em `tests/`, como utilitário de massa de dados, ou em `aplicacao/` para um relatório com muitas opções.

**Quando não usar.** Em Python, **argumentos nomeados e valores padrão** resolvem a maioria dos casos que, em outras linguagens, pedem um Builder. Só vale quando há uma sequência de passos, ou regras entre as partes que precisam ser validadas na montagem.

**No Projeto Financeiro.** Massa de dados para testar relatórios (um mês com vinte lançamentos de categorias variadas), ou um gerador de relatório com filtros opcionais.

---

## Um alerta: o Singleton

O Singleton, o padrão que garante **uma única instância** de uma classe, é o mais famoso e o mais perigoso. Ele fica de fora do catálogo de propósito: uma instância global é uma **dependência escondida**, que qualquer código alcança sem declarar. Isso dificulta os testes e esconde o grafo de objetos.

A **raiz de composição** do Capítulo 15 entrega o que ele prometia (uma instância só, compartilhada) **sem** a parte nociva: quem precisa de algo o recebe pelo construtor.

---

## Padrões que "somem" em Python

Vários padrões, em linguagens que exigem uma classe para tudo, ocupam muitas linhas. Em Python, o papel muitas vezes se reduz a algo bem menor:

| Padrão | Em linguagens com classes obrigatórias | Em Python |
|---|---|---|
| **Strategy** | Interface mais uma classe por estratégia | Uma **função**: `desconto: Callable[[float], float]`. As classes continuam úteis quando a estratégia tem estado ou vários métodos |
| **Observer / Command** | Interface mais classe por observador | Uma função ou um objeto com `__call__`, como os nossos manipuladores |
| **Factory** | Classe fábrica | A própria **classe** é um objeto que se chama; um dicionário `{canal: classe}` substitui o `if/elif` |
| **Decorator** | Classes embrulhando classes | Existe sintaxe própria, `@decorador`, para embrulhar **funções** |
| **Chain of Responsibility** | Elos ligados por referências | Uma lista de funções percorrida por um `for` |
| **Builder** | Classe construtora | Argumentos nomeados e `dataclass` |
| **Singleton** | Construtor privado e instância estática | Um **módulo**, que é carregado uma única vez |

O quadro não diz que as classes que escrevemos estavam erradas. Diz que, quando um papel se reduz a "algo que se chama", o mais simples é muitas vezes uma função. Escolhemos classes onde o papel tinha nome, dependências ou estado.

---

## Os padrões do curso, em um quadro

Este quadro reúne o que o curso aplicou e o que ficou no catálogo:

| Padrão | Onde | Problema que resolveu | O que o sistema ganhou |
|---|---|---|---|
| **Strategy** | Cap. 9 | Regras de desconto que mudam | Acrescentar uma regra sem tocar no `Pedido` |
| **Simple Factory** | Cap. 12 | `if/elif` de criação espalhado | A criação em um só lugar |
| **Template Method** | Cap. 12 | Pagamentos com o mesmo roteiro e passos diferentes | Roteiro fixo, e só o passo variável nas subclasses |
| **Factory Method** | Cap. 13 | Escolher o meio de entrega | Quem usa a entrega não conhece a classe concreta |
| **Facade** | Cap. 15 | Fluxo que coordena várias peças | Um caminho curto: `servico.pagar(...)` |
| **Injeção de Dependências** | Cap. 15 | Objetos que criavam suas próprias dependências | Dependências recebidas de fora, trocáveis nos testes |
| **Repository** | Cap. 16 | Dados presos à memória | Domínio que não sabe onde os dados ficam |
| **Data Mapper** | Cap. 17 | Traduzir objeto e tabela | Mapeamento fora do domínio |
| **Ports & Adapters** | Caps. 19 e 22 | Detalhes técnicos misturados ao negócio | Contratos do lado de quem usa; detalhes trocáveis, de saída e de entrada |
| **Observer** | Cap. 20 | Um caso de uso conhecendo todo mundo que reage | Reações acrescentadas sem abrir o caso de uso |
| **Publish/Subscribe** | Cap. 21 | Lista de observadores repetida; aviso sem nome | Fatos com nome e um único ponto de assinatura |
| Decorator, State, Adapter, Composite, Chain, Command, Builder | Este capítulo | Ainda não houve dor suficiente | Catálogo para a sua pesquisa |

Perceba o fio comum: **cada padrão apareceu depois de uma dor concreta**. Nenhum foi aplicado por antecipação, e nenhum é a resposta para uma pergunta que ainda não foi feita. Este curso não cobre os 23 padrões do GoF, e nem pretende.

---

## Como pesquisar

Sem apontar um único caminho, alguns pontos de partida:

- O livro **Design Patterns**, de Gamma, Helm, Johnson e Vlissides (o "GoF"), é a referência original dos padrões deste catálogo.
- O livro **Patterns of Enterprise Application Architecture**, de Martin Fowler, é a origem de nomes como Repository e Data Mapper, que usamos ao longo do curso.
- O site **Refactoring.Guru** tem uma página para cada padrão, com diagramas e exemplos em várias linguagens, inclusive Python.
- A **documentação do Python** é o lugar certo para ver o que a linguagem já oferece (decoradores, `dataclass`, funções como valores).

Duas dicas. Primeiro, **leia o exemplo em outra linguagem e depois o traduza para o seu domínio**: copiar o exemplo do site, com `Pizza` e `Carro`, não responde à pergunta "qual é a minha dor?". Segundo, **escreva o teste antes de generalizar**: o teste mostra, de forma concreta, o que o padrão passou a permitir.

---

## Para a sua entrega

Antes de escrever uma linha, responda por escrito:

1. **Qual é a dor, no meu projeto?** Aponte o arquivo, o `if` que cresce, a repetição.
2. **Que padrão do catálogo ataca essa dor?** E qual outro da lista eu considerei e descartei?
3. **O que ficará mais simples e o que ficará mais complicado?** Todo padrão tem custo.
4. **Como vou testar?** O que o teste deve provar que antes não era possível?

Se, ao responder, você concluir que a dor não existe, **essa também é uma resposta válida**, e vale registrá-la no documento de decisões. Procure então outra dor, em outro lugar do projeto.

---

## 📌 Resumo

- O curso aplicou os padrões que encontraram uma dor no E-Commerce; o catálogo reúne os que **ficaram de fora**
- **Decorator** embrulha uma operação por fora; **State** troca a tabela de transições por objetos; **Adapter** traduz uma interface externa; **Composite** trata parte e conjunto da mesma forma; **Chain of Responsibility** passa a decisão por vários elos; **Command com handler** trata a intenção como dado; **Builder** monta objetos complexos por passos
- Cada padrão tem **custo**, e em Python muitos se reduzem a funções, listas e argumentos nomeados
- O **Singleton** é um alerta: a raiz de composição entrega o que ele prometia sem a parte nociva
- A regra do curso vale aqui também: **primeiro a dor, depois o padrão**
- Na entrega final, você escolhe um padrão do catálogo, pesquisa, implementa, testa e **justifica**

## O que mudou no sistema

Nada, de propósito. Este capítulo é um mapa de leitura, e não uma etapa do E-Commerce. O código do curso termina no Capítulo 22.

## O que vem a seguir

O curso termina aqui. O que resta é a [entrega final](entrega.md): o seu Projeto Financeiro, com persistência, uma interface, eventos e o padrão do bônus que você escolheu. O sistema que você construiu não é perfeito, mas as suas decisões são suas, e você sabe explicá-las e fazê-lo crescer.
