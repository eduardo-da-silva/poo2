## Manual do Projeto

> Este documento é a porta de entrada da pasta `rules`.

Antes de produzir, revisar ou modificar qualquer material deste curso, leia este documento.

Ele resume toda a filosofia do projeto e indica quais documentos devem ser consultados em cada situação.

---

# O que é este projeto?

Este projeto não é apenas um conjunto de apostilas.

Ele é um curso completo de Programação Orientada a Objetos baseado na construção incremental de um software real.

O objetivo não é ensinar Python.

Python é apenas a linguagem utilizada.

O verdadeiro objetivo é ensinar Engenharia de Software utilizando Programação Orientada a Objetos.

Ao final do curso o aluno deverá ser capaz de analisar problemas, modelar domínios, distribuir responsabilidades entre objetos e construir software preparado para evoluir.

---

# Filosofia

Todo o material deve seguir as seguintes ideias.

- O domínio vem antes da implementação.

- O problema vem antes da solução.

- A modelagem vem antes do código.

- A responsabilidade vem antes da sintaxe.

- A simplicidade vem antes da abstração.

- A evolução vem antes da otimização.

Sempre que existir dúvida entre duas abordagens, escolher aquela que favorece o aprendizado.

---

# O projeto principal

Todo o curso gira em torno de um único sistema.

Um E-Commerce.

O software será construído do zero.

Nenhuma implementação aparece pronta.

Tudo evolui aula após aula.

O sistema cresce da mesma forma que um software real cresce.

---

# Projeto paralelo

Os alunos desenvolverão um Sistema Financeiro Pessoal.

Esse sistema nunca será implementado pelo professor.

Ele existe para obrigar o aluno a transferir conhecimento para outro domínio.

Todo novo conceito aprendido no E-Commerce deverá ser aplicado ao Projeto Financeiro.

---

# Como ensinar

Toda aula deve seguir, sempre que possível, esta sequência.

Problema

↓

Discussão

↓

Modelagem

↓

Implementação

↓

Refatoração

↓

Exercícios

↓

Projeto Financeiro

↓

Resumo

↓

Próxima aula

Nunca iniciar diretamente pelo código.

---

# O papel do código

O código não é o protagonista.

O protagonista é a decisão de projeto.

Cada trecho de código representa uma escolha.

Essa escolha deve ser explicada.

O aluno deve compreender não apenas como escrever o código, mas principalmente por que ele foi escrito daquela maneira.

---

# A voz do autor

O autor atua como um desenvolvedor experiente.

Ele conduz o raciocínio do aluno.

Ele faz perguntas.

Ele compara alternativas.

Ele mostra consequências.

Ele evita respostas prontas.

O texto deve parecer uma conversa entre um desenvolvedor experiente e alguém que está aprendendo a projetar software.

---

# O domínio

O domínio do curso é a principal fonte de verdade.

Nenhuma aula deve modificar responsabilidades das entidades sem atualizar a documentação do domínio.

A linguagem utilizada deve permanecer consistente durante todo o curso.

Evitar sinônimos.

Produto sempre será Produto.

Carrinho sempre será Carrinho.

Pedido sempre será Pedido.

---

# O código

Todo código deve priorizar:

clareza;

legibilidade;

boas práticas;

evolução.

Nunca utilizar recursos apenas porque são mais sofisticados.

Sempre escolher a implementação que melhor favorece o aprendizado.

---

# A identidade visual

O curso possui uma linguagem visual própria.

Ela deve ser utilizada de forma consistente.

As seções recorrentes incluem:

🧠 Pense

💡 Conceito

🏗️ Decisão de Projeto

⚠️ Erro Comum

🔍 Análise

🎯 Exercícios

🧩 Aplicando ao Projeto Financeiro

📌 Resumo

Essas seções fazem parte da identidade do curso.

---

# O que evitar

Evitar:

- exemplos artificiais;

- domínio de animais;

- domínio de carros;

- exemplos desconectados do projeto;

- capítulos compostos apenas por código;

- excesso de definições formais;

- abstrações prematuras;

- arquitetura complexa nas primeiras aulas.

---

# Evolução do software

O software cresce naturalmente.

Produto

↓

Categoria

↓

Cliente

↓

Carrinho

↓

ItemCarrinho

↓

Pedido

↓

Pagamento

↓

Promoções

↓

Persistência

↓

Eventos

↓

Arquitetura

Nenhuma etapa deve ser antecipada.

---

# Evolução pedagógica

O curso evolui da seguinte forma.

Modelagem

↓

Responsabilidades

↓

Coesão

↓

Acoplamento

↓

Composição

↓

Encapsulamento

↓

Colaboração

↓

Polimorfismo

↓

Padrões

↓

Arquitetura

↓

Refatoração

Essa ordem deve ser respeitada.

---

# Como utilizar esta pasta

## Escrevendo um novo capítulo

Consultar:

- 07-curriculum.md
- 08-course-roadmap.md
- 05-domain.md
- 06-code-style.md
- 04-author-voice.md

---

## Revisando um capítulo

Consultar:

- 10-review-checklist.md

---

## Criando exercícios

Consultar:

- regras de pedagogia;
- roadmap da aula;
- projeto financeiro.

---

## Criando código

Consultar:

- domínio;
- estilo de código;
- roadmap.

---

## Criando diagramas

Consultar:

- linguagem visual.

---

# Objetivo final

Ao terminar este curso, o aluno não deverá apenas saber escrever classes.

Ele deverá pensar como um engenheiro de software.

Ele deverá compreender que Programação Orientada a Objetos é uma forma de modelar problemas do mundo real, distribuir responsabilidades corretamente e construir sistemas preparados para evoluir.

Esse é o verdadeiro propósito deste projeto.

---

# Documentos da pasta `rules`

## Filosofia do curso

- 00-course.md

## Metodologia

- 01-pedagogy.md

## Estrutura das aulas

- 02-course-structure.md

## Linguagem visual

- 03-visual-language.md

## Voz do autor

- 04-author-voice.md

## Domínio

- 05-domain.md

## Estilo de código

- 06-code-style.md

## Currículo

- 07-curriculum.md

## Roadmap das aulas

- 08-course-roadmap.md

## Próximos documentos

Ainda serão produzidos:

- patterns-roadmap.md
- finance-project.md
- review-checklist.md
- mkdocs-guidelines.md
- ai-instructions.md

---

# Regra mais importante

Se existir qualquer conflito entre simplicidade da implementação e qualidade do aprendizado, priorizar sempre a qualidade do aprendizado.

Este curso ensina pessoas.

O código é apenas a ferramenta.