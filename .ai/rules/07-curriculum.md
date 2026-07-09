# rules/07-curriculum.md

# Currículo do Curso

## Objetivo

Este documento define a evolução completa do curso.

Ele representa o roteiro oficial do projeto.

Nenhum capítulo deve introduzir conceitos que pertençam a módulos futuros.

Todo novo conteúdo deve respeitar esta progressão.

---

# Estrutura Geral

O curso será dividido em sete módulos.

Cada módulo possui um objetivo próprio.

O projeto de E-Commerce evolui ao longo desses módulos.

O Projeto Financeiro acompanha a mesma evolução.

Cada módulo introduz apenas os conceitos necessários para resolver os problemas existentes naquele momento.

---

# Módulo 1
## Construindo o domínio

Objetivo.

Aprender a modelar objetos.

Começar a pensar em responsabilidades.

Introduzir composição.

Evitar herança.

---

Projeto

Criação do catálogo.

Categorias.

Produtos.

Clientes.

Carrinho.

Itens do carrinho.

---

Conceitos

Objetos.

Classes.

Responsabilidade.

Coesão.

Acoplamento.

Composição.

Objetos ricos.

Objetos anêmicos.

---

Projeto Financeiro

Cadastro de contas.

Categorias.

Lançamentos.

Movimentações.

---

Ao final deste módulo o aluno deverá conseguir modelar corretamente um pequeno domínio.

---

# Módulo 2
## Evoluindo o domínio

Objetivo.

Mostrar que software evolui.

Introduzir regras de negócio.

Criar objetos mais inteligentes.

---

Projeto

Pedidos.

Itens do pedido.

Estados.

Fluxo de compra.

---

Conceitos

Encapsulamento.

Invariantes.

Estados.

Colaboração entre objetos.

Responsabilidades.

---

Projeto Financeiro

Fechamento de lançamentos.

Conciliação.

Extrato.

---

Ao final deste módulo o aluno compreenderá como objetos colaboram.

---

# Módulo 3
## Estratégias

Objetivo.

Introduzir polimorfismo verdadeiro.

Eliminar condicionais.

---

Projeto

Descontos.

Promoções.

Cupons.

Frete.

---

Conceitos

Interfaces.

Polimorfismo.

Strategy.

Open/Closed.

---

Projeto Financeiro

Tipos de rendimento.

Tipos de juros.

Correções monetárias.

---

# Módulo 4
## Criando objetos

Objetivo.

Mostrar que criar objetos também é uma responsabilidade.

---

Projeto

Formas de pagamento.

Meios de entrega.

Notificações.

---

Conceitos

Factory.

Simple Factory.

Factory Method.

Dependency Injection.

---

Projeto Financeiro

Importadores.

Exportadores.

Leitores de arquivos.

---

# Módulo 5
## Organização do sistema

Objetivo.

Separar domínio da infraestrutura.

---

Projeto

Persistência.

Repositories.

Serviços.

Casos de uso.

---

Conceitos

Repository.

Camadas.

Arquitetura.

Inversão de dependências.

---

Projeto Financeiro

Persistência.

Importação.

Relatórios.

---

# Módulo 6
## Eventos

Objetivo.

Reduzir acoplamento.

---

Projeto

Notificações.

Logs.

Auditoria.

Estoque.

---

Conceitos

Observer.

Publisher.

Eventos.

Callbacks.

---

Projeto Financeiro

Alertas.

Metas.

Notificações.

---

# Módulo 7
## Refatoração

Objetivo.

Mostrar a evolução completa do software.

---

Projeto

Refatorações.

Melhorias.

Otimizações.

Testes.

Documentação.

---

Conceitos

SOLID.

Code Smells.

Refatoração.

Boas práticas.

---

Projeto Financeiro

Entrega final.

Documentação.

Apresentação.

---

# Evolução arquitetural

Durante todo o curso o sistema deverá crescer na seguinte ordem.

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

Cupom

↓

Promoções

↓

Estoque

↓

Persistência

↓

Eventos

↓

Refatorações

Essa ordem somente poderá ser alterada mediante justificativa pedagógica.

---

# Evolução dos conceitos

A sequência prevista é.

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

Polimorfismo

↓

Padrões de Projeto

↓

Arquitetura

↓

SOLID

↓

Refatoração

Nunca inverter essa ordem.

---

# Projeto Financeiro

O Projeto Financeiro acompanha exatamente a evolução do E-Commerce.

O professor nunca implementará esse sistema.

O aluno deverá fazer sozinho a adaptação.

O objetivo é consolidar o aprendizado.

---

# Objetivos de aprendizagem

Ao concluir o curso o aluno deverá ser capaz de:

Modelar pequenos domínios.

Distribuir responsabilidades.

Aplicar composição.

Evitar objetos anêmicos.

Aplicar encapsulamento.

Utilizar polimorfismo.

Aplicar padrões de projeto.

Separar domínio de infraestrutura.

Escrever software preparado para evolução.

---

# Critério de progressão

Uma aula somente poderá introduzir um conceito novo se:

o problema existir;

o aluno possuir conhecimento suficiente;

o conceito resolver um problema real;

o sistema estiver pronto para evoluir.

Evitar antecipações.

---

# Identidade do curso

O curso ensina Engenharia de Software.

Python é apenas a ferramenta utilizada.

Todo o currículo deve refletir essa filosofia.