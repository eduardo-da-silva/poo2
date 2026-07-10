# Módulo 1 — Construindo o domínio

# Bem-vindo ao projeto

Imagine que você acabou de ser contratado por uma pequena empresa que vende produtos pela internet. 

Até hoje, tudo era controlado por planilhas. Os produtos ficam em um arquivo Excel. Os clientes são anotados em outro. Os pedidos são registrados manualmente. Com o aumento das vendas, ficou claro que esse processo não é mais suficiente. 

Ao longo deste curso, acompanharemos a evolução dessa empresa. Cada capítulo representará um novo desafio enfrentado pelo negócio. À medida que a empresa cresce, nosso sistema também crescerá. Os conceitos de Programação Orientada a Objetos surgirão naturalmente como ferramentas para resolver esses novos problemas.

Assim como acontece em projetos reais. Começaremos do zero a construção de um sistema de E-Commerce. Mas, ainda não escreveremos código, pois precisamos aprender a **pensar sobre o projeto**.

Queremos responder a uma pergunta fundamental:

> O que significa projetar software orientado a objetos?

A resposta envolve muito mais do que criar classes e instanciar objetos. Envolve compreender o problema, identificar os conceitos do domínio, distribuir responsabilidades e modelar relacionamentos entre entidades.

## O que você aprenderá

- Por que modelar o domínio é mais importante que escrever código
- Como objetos representam conceitos reais do negócio
- A diferença entre objetos ricos e anêmicos
- O que é encapsulamento (e o que **não** é)
- A pergunta mais importante do curso: **quem é responsável por isso?**
- Como descobrir entidades através de narrativas
- Como modelar relacionamentos com composição e associação
- Por que evitamos herança neste módulo

## O que existe hoje?

Neste momento, a empresa possui apenas:

- uma lista de produtos;
- um controle simples de preços;
- nenhuma regra de negócio;
- nenhuma persistência;
- nenhum pedido.

Nosso primeiro objetivo será representar esses produtos utilizando objetos.

## Estrutura do módulo

Este módulo está organizado em quatro capítulos:

1. **O que significa projetar software** — fundamentos, projetos da disciplina e princípios de orientação a objetos
2. **Conhecendo o domínio** — análise do problema, narrativa de compra e descoberta de entidades
3. **Primeiras entidades e relacionamentos** — modelagem das classes, composição vs. associação e decisões de projeto
4. **Mão na massa: implementando as classes** — criação do projeto, código das entidades e testes automatizados

---

Prepare-se para pensar menos em sintaxe e mais em design. Vamos começar.
