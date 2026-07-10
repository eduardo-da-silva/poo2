# Estrutura dos Capítulos

## Objetivo deste documento

Este documento define a estrutura padrão utilizada em todos os capítulos do curso.

O objetivo não é obrigar que todos os capítulos possuam exatamente a mesma organização, mas garantir consistência ao longo de todo o material.

Cada capítulo deve conduzir o aluno desde um problema real até uma solução bem fundamentada, mostrando não apenas o resultado, mas principalmente o processo de tomada de decisão.

---

# Estrutura geral

Sempre que possível, cada capítulo deve seguir a seguinte sequência:

1. Contextualização
2. Problema
3. Discussão
4. Modelagem
5. Implementação
6. Refatoração
7. Aplicação no Projeto Financeiro
8. Resumo
9. Preparação para o próximo capítulo

Nem todas as seções precisam existir em todos os capítulos, mas a ordem lógica deve ser preservada.

---

# 1. Contextualização

Todo capítulo deve começar contextualizando o leitor.

O aluno precisa compreender:

- onde estamos;
- o que já foi desenvolvido;
- qual problema iremos resolver;
- por que esse problema surgiu agora.

Nunca iniciar diretamente com código.

Exemplo desejado:

> Até este momento nosso E-Commerce já permite cadastrar produtos e categorias. Entretanto, ainda não existe nenhuma forma de um cliente selecionar produtos para compra. Nesta aula resolveremos esse problema implementando o Carrinho de Compras.

---

# 2. Apresentação do problema

Toda implementação deve nascer de uma necessidade.

Evitar frases como:

> Hoje aprenderemos composição.

Preferir:

> Nosso sistema possui um carrinho que armazena produtos. Entretanto, como representar diferentes quantidades do mesmo produto?

A necessidade deve justificar o novo conceito.

---

# 3. Discussão

Antes de implementar qualquer solução, discutir possíveis alternativas.

Utilizar perguntas como:

- O que precisamos representar?
- Quem possui essa informação?
- Quem deveria executar essa regra?
- Existe mais de uma solução?
- Como essa decisão afetará o futuro do sistema?

A discussão deve estimular o pensamento crítico.

---

# 4. Modelagem

Somente após compreender o problema iniciar a modelagem.

Nesta etapa apresentar:

- entidades;
- objetos;
- relacionamentos;
- responsabilidades;
- regras de negócio.

Sempre que possível utilizar diagramas Mermaid.

Preferir diagramas simples.

Evitar excesso de detalhes.

Os diagramas devem ajudar na compreensão, não impressionar pela complexidade.

---

# 5. Implementação

Somente nesta etapa iniciar a codificação.

Antes de cada bloco de código explicar seu objetivo.

Após cada bloco explicar:

- por que foi implementado dessa forma;
- quais alternativas existiam;
- quais problemas foram evitados.

Evitar grandes blocos de código sem interrupções.

Intercalar explicações e implementação.

---

# Organização da implementação

Sempre que possível seguir esta ordem:

## Definição da classe

Apresentar sua responsabilidade.

Explicar por que ela existe.

---

## Atributos

Explicar por que cada atributo pertence à classe.

Questionar quando algum atributo parecer inadequado.

---

## Construtor

Explicar quais informações são obrigatórias.

Evitar construtores gigantes.

---

## Métodos

Apresentar um método por vez.

Explicar sua responsabilidade.

Discutir possíveis alternativas.

---

## Exemplo de utilização

Após implementar um comportamento importante, mostrar um pequeno exemplo de uso.

Os exemplos devem ser simples.

O foco continua sendo o projeto.

---

# 6. Discussão de Projeto

Após uma implementação importante, criar uma seção chamada:

## Decisão de Projeto

Nela explicar:

- por que essa solução foi escolhida;
- quais alternativas foram descartadas;
- quais benefícios ela oferece;
- quais limitações ela possui.

Essa seção aproxima o aluno do processo de desenvolvimento profissional.

---

# 7. Erros comuns

Sempre que possível incluir uma seção.

## Erros comuns

Apresentar implementações inadequadas.

Explicar por que parecem corretas inicialmente.

Mostrar os problemas gerados.

Evitar apenas afirmar que algo está errado.

Demonstrar as consequências.

---

# 8. Refatoração

Sempre que possível mostrar evolução.

Exemplo:

Primeira implementação simples.

↓

Nova necessidade.

↓

Código começa a apresentar problemas.

↓

Refatoração.

↓

Nova solução.

O aluno deve perceber que refatorar faz parte do desenvolvimento.

---

# 9. Exercícios de reflexão

Ao longo do capítulo inserir pequenas pausas.

Utilizar títulos como:

## Pense

## Reflita

## Antes de continuar

Essas seções não possuem resposta imediata.

O objetivo é fazer o aluno pensar antes de continuar lendo.

---

# 10. Exercícios práticos

Ao final do capítulo propor exercícios.

Sempre dividir em níveis.

## Nível 1

Fixação.

Poucas alterações.

---

## Nível 2

Aplicação.

Resolver problemas semelhantes.

---

## Nível 3

Desafio.

Exigir tomada de decisão.

Permitir diferentes soluções.

---

# 11. Projeto Financeiro

Praticamente todos os capítulos devem terminar com:

## Aplicando ao Projeto Financeiro

Essa seção não deve entregar a solução.

Ela deve provocar o aluno.

Exemplo.

"Nosso Carrinho possui ItemCarrinho.

Existe algum relacionamento semelhante no Sistema Financeiro?"

O aluno deve identificar sozinho.

---

# 12. Resumo

Todo capítulo deve terminar resumindo:

- conceitos aprendidos;
- decisões tomadas;
- melhorias realizadas;
- evolução do sistema.

Evitar repetir o texto do capítulo.

O resumo deve ser objetivo.

---

# 13. Próximo capítulo

Sempre finalizar criando expectativa.

Exemplo.

> Agora nosso cliente consegue adicionar produtos ao carrinho.

> Entretanto, ainda não existe nenhuma forma de finalizar uma compra.

> Esse será nosso próximo desafio.

O aluno deve perceber que o sistema continua evoluindo.

---

# Uso de diagramas

Sempre utilizar diagramas quando ajudarem na compreensão.

Preferência:

- Mermaid Class Diagram
- Mermaid Sequence Diagram
- Mermaid Flowchart

Evitar diagramas excessivamente complexos.

Um diagrama simples vale mais do que um diagrama completo e difícil de interpretar.

---

# Uso de tabelas

Utilizar tabelas para:

- comparar alternativas;
- resumir responsabilidades;
- listar diferenças;
- apresentar vantagens e desvantagens.

Evitar tabelas muito extensas.

---

# Uso de listas

Listas devem ser utilizadas apenas quando realmente melhorarem a leitura.

Evitar transformar todo o material em listas.

Dar preferência ao texto contínuo.

---

# Relação entre texto e código

A proporção aproximada desejada é:

- 60% explicação
- 40% código

O aluno deve compreender o código antes de vê-lo.

Nunca utilizar código como única explicação.

---

# Relação entre teoria e prática

Toda teoria deve aparecer para resolver um problema prático.

Toda prática deve reforçar um conceito teórico.

Nunca separar completamente teoria e prática.

---

# Progressão da complexidade

Cada capítulo deve aumentar ligeiramente a complexidade do sistema.

Nunca introduzir muitos conceitos novos simultaneamente.

Sempre construir sobre conhecimentos anteriores.

---

# Identidade do curso

Ao terminar qualquer capítulo, o leitor deve sentir que:

- aprendeu um conceito importante;
- evoluiu um sistema real;
- compreendeu uma decisão de projeto;
- está preparado para o próximo desafio.

Essa sensação de continuidade é uma das principais características deste curso.

Ao final do capítulo mostrar:

- o que foi construído
- quais conceitos apareceram
- o estado atual do sistema
- o próximo desafio