# rules/08-course-roadmap.md

# Roadmap do Curso

## Objetivo

Este documento descreve a evolução completa do curso, aula a aula.

Ele serve como guia para a produção do material didático.

Antes de escrever qualquer capítulo, este documento deve ser consultado.

Cada aula representa um incremento do software.

Nenhuma funcionalidade deve surgir antes do momento previsto.

Nenhum conceito deve ser antecipado sem justificativa pedagógica.

---

# Estrutura de cada aula

Toda aula deve responder às seguintes perguntas.

## Objetivo

O que o aluno deverá aprender?

---

## Evolução do E-Commerce

Qual parte do sistema será construída?

---

## Projeto Financeiro

Como o aluno aplicará o mesmo conceito?

---

## Conceitos de POO

Quais conceitos serão reforçados?

---

## Discussões

Quais perguntas deverão ser feitas ao aluno?

---

## Código

Quais classes serão criadas ou modificadas?

---

## Diagramas

Quais diagramas deverão aparecer?

---

## Exercícios

Quais atividades serão propostas?

---

## Gancho

Como preparar a próxima aula?

---

# MÓDULO 1

## Aula 1
### O primeiro contato com o domínio

### Objetivo

Apresentar o curso.

Apresentar o projeto.

Mostrar que Orientação a Objetos é modelagem.

Não ensinar sintaxe.

---

### E-Commerce

Apresentação do domínio.

Produto.

Categoria.

Primeira modelagem.

Sem persistência.

Sem interface.

---

### Projeto Financeiro

Apresentar o domínio.

Conta.

Categoria.

Lançamento.

Nenhum código ainda.

---

### Conceitos

Modelagem.

Objeto.

Classe.

Responsabilidade.

Linguagem ubíqua.

---

### Discussões

O que realmente é um Produto?

Produto conhece Cliente?

Categoria calcula preço?

Quem deveria conhecer quem?

---

### Diagramas

Primeiro diagrama de classes.

Produto

Categoria

Relacionamento.

---

### Código

Classe Produto.

Classe Categoria.

Relacionamento entre ambas.

---

### Exercícios

Criar novas categorias.

Adicionar novos produtos.

Modelar atributos.

---

### Gancho

Agora temos produtos.

Mas ninguém pode comprá-los.

Como um cliente escolhe produtos?

---

# Aula 2

### Objetivo

Introduzir Cliente.

Mostrar colaboração entre objetos.

---

### E-Commerce

Cliente.

Primeira associação.

---

### Projeto Financeiro

Cadastro de contas.

---

### Conceitos

Relacionamentos.

Associações.

Responsabilidades.

---

### Discussões

Cliente deve conhecer Produto?

Produto deve conhecer Cliente?

---

### Código

Cliente.

Relacionamentos.

---

### Gancho

Cliente existe.

Agora ele precisa comprar.

---

# Aula 3

### Objetivo

Criar Carrinho.

Introduzir composição.

---

### E-Commerce

Carrinho.

Cliente possui Carrinho.

---

### Projeto Financeiro

Carteira.

Conta principal.

---

### Conceitos

Composição.

Responsabilidade.

Alta coesão.

---

### Discussões

Carrinho deve guardar Produtos?

Ou outra abstração?

---

### Código

Carrinho.

Adicionar produto.

Remover produto.

---

### Diagramas

Cliente

↓

Carrinho

---

### Gancho

Agora surge um problema.

Como controlar quantidades?

---

# Aula 4

### Objetivo

Criar ItemCarrinho.

Mostrar quando um relacionamento vira objeto.

---

### Conceitos

Composição.

Objetos ricos.

Modelagem.

---

### Discussões

Por que não guardar apenas Produto?

Onde fica a quantidade?

---

### Código

ItemCarrinho.

Subtotal.

Carrinho refatorado.

---

### Exercícios

Adicionar alteração de quantidade.

---

### Gancho

Nosso Carrinho funciona.

Mas quem calcula o total?

---

# Aula 5

### Objetivo

Refatorar Carrinho.

Distribuir responsabilidades.

---

### Conceitos

Coesão.

Acoplamento.

Objetos ricos.

---

### Discussões

Quem calcula subtotal?

Quem calcula total?

Quem conhece preço?

---

### Código

Refatoração completa.

---

### Gancho

Agora podemos finalizar uma compra.

---

# Aula 6

### Objetivo

Criar Pedido.

---

### Conceitos

Estado.

Responsabilidade.

Transição.

---

### Código

Pedido.

ItemPedido.

---

### Gancho

Pedido criado.

Mas ainda não existe pagamento.

---

# Aula 7

Pagamento.

Estados.

Primeira enumeração.

---

# Aula 8

Cupons.

Primeira implementação simples.

Sem Strategy.

---

# Aula 9

Problemas da implementação.

Condicionais crescendo.

Preparação para Strategy.

---

# Aula 10

Strategy.

Refatoração.

Primeiro padrão.

---

# MÓDULO 2

A partir deste ponto o roadmap continua exatamente no mesmo formato.

Cada aula deverá possuir:

Objetivos.

Conceitos.

Discussões.

Código.

Diagramas.

Exercícios.

Projeto Financeiro.

Gancho.

---

# Ordem dos padrões

Factory.

↓

Strategy.

↓

Observer.

↓

Repository.

↓

Facade.

↓

Dependency Injection.

Nunca antecipar padrões.

Cada um deve resolver um problema existente.

---

# Ordem das refatorações

Duplicação.

↓

Extração de métodos.

↓

Extração de classes.

↓

Polimorfismo.

↓

Camadas.

↓

Arquitetura.

---

# Crescimento da arquitetura

Inicialmente.

Arquivos simples.

↓

Pacotes.

↓

Domínio.

↓

Aplicação.

↓

Infraestrutura.

↓

Persistência.

Nunca começar o curso com arquitetura complexa.

---

# Evolução do Projeto Financeiro

O Projeto Financeiro sempre acompanha o E-Commerce.

Ele nunca deve ficar mais de uma aula atrasado.

O aluno deve conseguir aplicar imediatamente os conceitos recém-aprendidos.

---

# Regra de ouro

Toda aula deve responder claramente:

O que o software aprendeu?

O que o aluno aprendeu?

O que faremos na próxima aula?

Se uma dessas respostas não estiver clara, a aula deverá ser reestruturada.