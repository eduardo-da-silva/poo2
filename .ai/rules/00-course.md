# Curso de Programação Orientada a Objetos II
## Visão Geral do Projeto

---


# Objetivo deste documento

Este documento apresenta a visão geral do curso, seus objetivos pedagógicos, a metodologia adotada e as decisões que orientam toda a produção do material.

Todos os capítulos, exemplos, exercícios e projetos devem respeitar as definições estabelecidas neste documento.

Em caso de conflito entre este documento e qualquer outro arquivo da pasta `rules`, este documento possui prioridade.

---

# Objetivo do curso

Este curso ensina Programação Orientada a Objetos II por meio da evolução contínua de um único sistema. O objetivo não é ensinar sintaxe, mas desenvolver a capacidade de projetar software. Ao final, o aluno deve ser capaz de justificar decisões de modelagem, distribuir responsabilidades entre objetos e evoluir um sistema de forma incremental.

Este curso tem como objetivo ensinar Programação Orientada a Objetos por meio do desenvolvimento incremental de um sistema real.

O foco do curso não é ensinar a sintaxe da linguagem Python.

Python será utilizada apenas como ferramenta de implementação.

O verdadeiro objetivo é desenvolver no aluno a capacidade de:

- compreender um domínio de negócio;
- modelar problemas utilizando objetos;
- distribuir corretamente responsabilidades entre classes;
- identificar e reduzir acoplamento;
- aumentar coesão;
- escrever código legível e evolutivo;
- aplicar princípios clássicos da orientação a objetos;
- compreender quando utilizar padrões de projeto;
- desenvolver software de forma incremental.

Ao final do curso, espera-se que o aluno seja capaz de projetar sistemas orientados a objetos de pequeno e médio porte utilizando boas práticas de Engenharia de Software.

---

# Público-alvo

Este curso destina-se a estudantes que já possuem conhecimentos básicos de programação em Python.

Os alunos já conhecem conceitos como:

- variáveis;
- estruturas condicionais;
- estruturas de repetição;
- funções;
- módulos;
- listas;
- dicionários;
- tratamento de exceções;
- classes;
- objetos;
- encapsulamento;
- herança;
- polimorfismo.

O curso não deve voltar a ensinar esses assuntos desde o início.

Sempre que necessário, eles poderão ser rapidamente revisados dentro do contexto do projeto.

---

# Filosofia do curso

Este curso parte da seguinte premissa:

> Aprender Orientação a Objetos significa aprender a tomar decisões de projeto.

O aluno não deve decorar definições.

O aluno deve compreender por que determinadas decisões produzem software melhor.

Sempre que possível, o material deve incentivar perguntas como:

- Quem deveria ser responsável por esta regra?
- Esta classe realmente precisa conhecer aquela?
- Este comportamento pertence a este objeto?
- Esta abstração representa corretamente o domínio?

O desenvolvimento do pensamento crítico é mais importante do que memorizar conceitos.

---

# Metodologia

Todo o curso será baseado em um único projeto principal.

Esse projeto evoluirá continuamente durante o semestre.

Novas funcionalidades serão adicionadas gradualmente.

Novos conceitos serão apresentados apenas quando surgirem naturalmente durante essa evolução.

Evitar exemplos artificiais sempre que possível.

Evitar exemplos clássicos como:

- Animal
- Cachorro
- Gato
- Pessoa
- Funcionário
- Carro

Esses exemplos somente poderão aparecer caso sejam utilizados para comparação extremamente rápida.

Todo o restante do curso deve utilizar o domínio do E-Commerce.

---

# Projeto principal

O projeto desenvolvido em sala será um sistema de E-Commerce.

O sistema será construído desde sua concepção.

Durante o curso o sistema evoluirá passando por diversas etapas.

Exemplos:

- produtos;
- categorias;
- clientes;
- carrinho;
- pedidos;
- pagamentos;
- estoque;
- cupons;
- notificações;
- persistência;
- testes;
- padrões de projeto.

Cada novo recurso servirá como contexto para introduzir novos conceitos da disciplina.

---

# Projeto paralelo

Os alunos desenvolverão individualmente um Sistema Financeiro Pessoal.

Esse projeto acompanhará toda a evolução do E-Commerce.

O professor nunca desenvolverá esse sistema em sala.

O objetivo é obrigar o aluno a aplicar os mesmos princípios em outro domínio.

Sempre que um novo conceito for apresentado no projeto principal, o aluno deverá analisar como aplicá-lo ao projeto financeiro.

---

# Aprendizagem baseada em evolução

O sistema nunca deve aparecer pronto.

Toda funcionalidade deve surgir porque existe uma necessidade anterior.

Exemplo.

Primeiro existe um carrinho.

Depois surge a necessidade de calcular o total.

Depois aparece um desconto.

Depois aparecem cupons.

Depois surgem diferentes estratégias de desconto.

Essa evolução deve parecer natural.

Evitar antecipar conceitos.

---

# Aprendizagem baseada em problemas

Cada novo assunto deve começar com um problema.

Nunca iniciar um capítulo apresentando sintaxe.

A sequência desejada é:

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

Generalização

O aluno deve perceber por que determinado conceito é necessário antes de conhecê-lo.

---

# Engenharia de Software antes da linguagem

Sempre que houver conflito entre ensinar um recurso da linguagem ou discutir uma decisão de projeto, priorizar a decisão de projeto.

O curso ensina Engenharia de Software utilizando Python.

Não ensina Python utilizando exemplos de Engenharia de Software.

---

# Desenvolvimento incremental

Nenhuma aula deve apresentar a solução completa.

Cada capítulo deve deixar espaço para evolução futura.

O sistema deve crescer de forma semelhante a um software real.

É desejável que algumas decisões sejam revistas posteriormente.

Isso permitirá mostrar aos alunos o valor da refatoração.

---

# Erros fazem parte do aprendizado

Sempre que possível apresentar:

- soluções ingênuas;
- erros comuns;
- decisões equivocadas;
- alternativas de implementação.

Esses exemplos são tão importantes quanto a solução correta.

O aluno aprende comparando soluções.

---

# Objetivo das aulas

Cada aula deve possuir quatro objetivos simultâneos.

1. Evoluir o sistema.

2. Ensinar um conceito de POO.

3. Melhorar o projeto existente.

4. Preparar terreno para a próxima aula.

Nenhuma aula deve existir apenas para apresentar teoria.

---

# Relação entre teoria e prática

A teoria deve surgir da prática.

A prática nunca deve parecer apenas um exercício de programação.

Cada trecho de código representa uma decisão de projeto.

Essa decisão deve ser explicitamente discutida.

---

# Evolução da complexidade

As primeiras aulas devem parecer simples.

Entretanto, desde o início, o projeto deve ser organizado para crescer.

A complexidade do domínio deve aumentar gradualmente.

O aluno nunca deve sentir que um conceito foi introduzido "do nada".

---

# Papel do professor

Durante todo o material, o professor atua como um desenvolvedor experiente conduzindo uma equipe.

O professor não apenas mostra código.

Ele explica decisões.

Levanta dúvidas.

Questiona alternativas.

Mostra consequências.

Corrige escolhas.

O aluno deve sentir que está acompanhando o raciocínio de um desenvolvedor experiente.

---

# Resultado esperado

Ao concluir este curso, o aluno não deverá apenas saber criar classes.

Ele deverá ser capaz de analisar um problema real, identificar objetos relevantes, distribuir responsabilidades corretamente e construir sistemas orientados a objetos capazes de evoluir ao longo do tempo.

Este documento define a identidade do curso.

Todos os demais arquivos da pasta `rules` detalham como essa identidade deve ser aplicada na produção do material.