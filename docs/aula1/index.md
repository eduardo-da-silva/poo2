# Aula 1 — Introdução ao Curso e Início do Projeto E-Commerce

## Objetivos da aula

Ao final desta aula você será capaz de:

- Entender a diferença entre desenvolver software e apenas escrever código
- Revisar os principais conceitos da Programação Orientada a Objetos
- Compreender o domínio do sistema de E-Commerce que será desenvolvido ao longo do curso
- Identificar as primeiras entidades do domínio
- Compreender o projeto que será desenvolvido individualmente durante o semestre

---


## Escrever código é fácil. Projetar software é difícil.

Imagine que uma loja virtual precise calcular o valor total do carrinho de compras. Onde esse cálculo deveria acontecer?

- Na classe `Produto`?
- Na classe `Cliente`?
- Na classe `Pedido`?
- Na classe `Carrinho`?
- Em uma função separada?
- Em um serviço?

Todas essas alternativas são tecnicamente possíveis. Entretanto, apenas algumas delas conduzem a um projeto organizado e de fácil manutenção.

Durante este curso aprenderemos a tomar esse tipo de decisão utilizando princípios consolidados da Engenharia de Software.

!!! warning "Reflexão importante"

    **As primeiras linhas de código de um projeto são as mais caras.** Quando escolhemos mal as responsabilidades das classes, criamos dependências desnecessárias ou utilizamos abstrações inadequadas, esses problemas tendem a acompanhar o projeto durante meses ou até anos.

---

## Nossa primeira preocupação: modelar o domínio

Antes de escrever qualquer linha de código precisamos responder algumas perguntas:

- O que existe dentro de um E-Commerce?
- Quais objetos fazem parte desse sistema?
- Quais deles possuem comportamento próprio?
- Quais apenas armazenam informações?
- Quais dependem uns dos outros?
- Quais podem existir sozinhos?

Responder corretamente essas perguntas costuma ser muito mais importante do que escrever rapidamente centenas de linhas de código.

Um projeto bem modelado tende a evoluir naturalmente. Um projeto mal modelado costuma acumular problemas a cada nova funcionalidade. Por esse motivo, nossa primeira atividade será compreender o domínio do problema antes de iniciar a implementação.

---

## Aplicando ao Projeto Financeiro

Ao longo do curso, ao final de cada seção, você encontrará uma pequena reflexão sobre como aplicar o mesmo conceito ao Sistema de Controle Financeiro Pessoal. O objetivo não é copiar o código. É transferir o raciocínio. Fique atento a essas seções — elas são a chave para realmente aprender os princípios, e não apenas repetir exemplos.

---

Antes de começarmos a modelar, precisamos entender os dois projetos que guiarão nosso semestre.
