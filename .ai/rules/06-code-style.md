# Estilo de Código

## Objetivo deste documento

Este documento define os padrões utilizados em todos os exemplos de código do curso.

Seu objetivo é garantir consistência entre os capítulos, facilitar o aprendizado e evitar que o aluno seja distraído por detalhes de implementação que não fazem parte dos objetivos pedagógicos.

As convenções aqui descritas possuem prioridade sobre preferências pessoais de quem estiver produzindo o material.

---

# Filosofia

O código apresentado no curso deve ensinar Engenharia de Software.

Python é apenas a linguagem utilizada.

Sempre priorizar:

- Clareza
- Legibilidade
- Simplicidade
- Evolução
- Boas práticas

Nunca escrever código apenas porque é mais curto.

---

# O código ensina

Todo exemplo deve possuir um objetivo pedagógico.

Antes de escrever uma linha de código responder:

"O que este trecho pretende ensinar?"

Se não houver resposta clara, o código provavelmente é desnecessário.

---

# Código incremental

O projeto cresce capítulo após capítulo.

Nunca mostrar uma implementação completa antes do momento adequado.

O aluno deve acompanhar toda a evolução.

Evitar "saltos mágicos".

---

# Organização dos exemplos

Sempre apresentar:

Problema

↓

Discussão

↓

Código

↓

Análise

↓

Possíveis melhorias

Nunca iniciar uma seção diretamente com código.

---

# Python moderno

Utilizar recursos modernos da linguagem.

Preferência:

- Python 3.12 ou superior
- Type Hints
- dataclasses quando fizer sentido
- Enum
- pathlib
- match/case apenas quando realmente melhorar a leitura

Evitar recursos obsoletos.

---

# Type Hints

Todos os exemplos devem utilizar anotações de tipos.

Exemplo.

```python
def adicionar_item(produto: Produto, quantidade: int) -> None:
    ...
```

Mesmo quando Python não exigir.

O objetivo é tornar o código mais legível.

---

# Docstrings

Evitar docstrings em exemplos pequenos.

Elas aumentam o volume visual.

Utilizar apenas quando realmente agregarem informação.

---

# Comentários

Comentários devem explicar decisões.

Nunca explicar sintaxe.

Ruim.

```python
# Soma os valores
total += valor
```

Bom.

```python
# Mantemos o preço original para preservar
# o histórico do pedido mesmo que o produto
# seja reajustado futuramente.
```

---

# Nomes

Os nomes devem representar o domínio.

Sempre utilizar:

produto

cliente

pedido

carrinho

categoria

pagamento

Evitar:

obj

x

tmp

data

valor1

coisa

teste

item2

---

# Métodos

Os métodos devem representar comportamentos.

Evitar métodos gigantes.

Preferência:

5 a 20 linhas.

Se um método começar a crescer demais, discutir extração de responsabilidades.

---

# Classes

Cada classe deve possuir uma responsabilidade claramente definida.

Evitar classes que concentram muitas regras.

Sempre reforçar:

Alta coesão.

---

# Métodos privados

Utilizar métodos privados quando melhorarem a leitura.

Não criar métodos privados apenas para reduzir quantidade de linhas.

---

# Atributos

Os atributos representam estado.

Não criar atributos desnecessários.

Todo atributo deve responder:

"Esta informação realmente pertence a este objeto?"

---

# Propriedades

Utilizar @property apenas quando fizer sentido.

Evitar propriedades apenas para encapsular leitura de atributos.

Sempre justificar seu uso.

---

# Dataclasses

Podem ser utilizadas.

Entretanto:

Nunca transformar todas as classes em dataclasses.

Sempre discutir vantagens e limitações.

O objetivo é ensinar modelagem.

Não recursos da linguagem.

---

# Enum

Sempre utilizar Enum para estados.

Exemplo.

PedidoCriado

PedidoPago

PedidoCancelado

Evitar strings espalhadas pelo código.

---

# Exceções

Sempre lançar exceções específicas.

Evitar:

```python
raise Exception()
```

Preferir:

```python
raise ProdutoIndisponivelError(...)
```

Mesmo que a exceção ainda seja simples.

---

# Coleções

Preferir:

list

dict

set

Somente introduzir estruturas mais sofisticadas quando realmente necessário.

---

# Imutabilidade

Sempre discutir quando um objeto deve ou não ser alterado.

Exemplo.

ItemPedido tende a ser mais imutável.

Carrinho é naturalmente mutável.

---

# Encapsulamento

Nunca modificar atributos diretamente apenas por praticidade.

Sempre mostrar o comportamento acontecendo através dos métodos apropriados.

---

# Objetos ricos

Sempre incentivar objetos ricos.

Evitar classes compostas apenas por getters e setters.

Sempre perguntar:

Quem deveria executar esta regra?

---

# Código duplicado

Pequenas duplicações são aceitáveis no início do curso.

Elas servirão como motivação para futuras refatorações.

Evitar abstrações prematuras.

---

# Complexidade

Nunca escrever código "inteligente".

Preferir código fácil de entender.

Mesmo que seja um pouco mais extenso.

---

# Imports

Agrupar conforme PEP 8.

Biblioteca padrão.

↓

Bibliotecas externas.

↓

Projeto.

Sempre manter organizados.

---

# Organização dos arquivos

Enquanto o projeto for pequeno.

```text
produto.py

categoria.py

cliente.py

carrinho.py
```

À medida que crescer.

```text
domain/

application/

infrastructure/

tests/
```

Essa evolução será gradual.

Nunca antecipar arquiteturas complexas.

---

# Persistência

Inicialmente o projeto não possui persistência.

Objetos vivem apenas em memória.

Somente quando surgir necessidade serão introduzidos:

Repository

ORM

Banco de Dados

---

# Frameworks

Durante boa parte do curso evitar frameworks.

O domínio deve permanecer independente.

Quando o framework aparecer, mostrar claramente que ele é apenas um detalhe.

---

# Testes

Os testes fazem parte do projeto.

Não são um complemento.

Sempre que um comportamento importante surgir, considerar a criação de testes.

Os testes também ensinam modelagem.

---

# Refatoração

Nunca esconder a evolução.

Quando uma implementação ficar ruim, utilizá-la como oportunidade didática.

Mostrar:

Antes

↓

Problema

↓

Refatoração

↓

Depois

---

# Performance

Não otimizar prematuramente.

Sempre priorizar:

Código correto.

↓

Código legível.

↓

Código fácil de evoluir.

Somente depois discutir desempenho.

---

# Consistência

Todos os capítulos devem utilizar as mesmas convenções.

O aluno nunca deve perceber mudanças de estilo ao longo do curso.

A consistência facilita a aprendizagem.

---

# Objetivo final

O código apresentado no curso deve servir como exemplo de boas práticas de desenvolvimento orientado a objetos.

Cada trecho de código deve ensinar não apenas como resolver um problema, mas principalmente como projetar software que possa evoluir ao longo do tempo.