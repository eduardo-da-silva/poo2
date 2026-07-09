# Linguagem Visual do Curso

## Objetivo deste documento

Este documento define a identidade visual do material didático.

A linguagem visual deve ajudar o aluno a compreender rapidamente o propósito de cada seção, reduzir a carga cognitiva durante a leitura e tornar a navegação mais agradável.

A identidade visual deve ser consistente durante todo o curso.

---

# Princípios

A aparência nunca deve existir apenas por estética.

Cada elemento visual possui uma função pedagógica.

Todo destaque deve comunicar algo importante.

Evitar excesso de caixas coloridas, emojis e destaques.

Quando tudo chama atenção, nada chama atenção.

---

# Hierarquia visual

Cada capítulo deve possuir uma hierarquia clara.

# Título do capítulo

## Seção

### Subseção

#### Pequenos tópicos

Nunca pular níveis de título.

Evitar criar capítulos muito profundos.

---

# Admonitions

O MkDocs Material oferece diversos tipos de caixas de destaque.

Elas devem ser utilizadas de forma consistente.

Não utilizar apenas porque "fica bonito".

---

## NOTE

Utilizar para observações importantes.

Exemplo:

- detalhes da linguagem;
- observações históricas;
- curiosidades.

Não utilizar para conceitos centrais.

---

## TIP

Utilizar para boas práticas.

Exemplos:

- sugestões de implementação;
- atalhos;
- boas decisões de projeto.

---

## IMPORTANT

Utilizar quando o aluno precisar lembrar de algo durante todo o curso.

Exemplos:

- responsabilidade das classes;
- encapsulamento;
- baixo acoplamento.

---

## WARNING

Utilizar para alertar sobre erros frequentes.

Exemplos.

- violação de encapsulamento;
- uso incorreto de herança;
- responsabilidades mal distribuídas.

Sempre explicar por que o erro ocorre.

Nunca apenas afirmar que está errado.

---

## EXAMPLE

Utilizar antes de exemplos maiores.

Separar claramente explicação e implementação.

---

## QUESTION

Utilizar para perguntas de reflexão.

Essas caixas não devem trazer a resposta imediatamente.

Elas existem para estimular o raciocínio.

---

## SUCCESS

Utilizar ao final de implementações importantes.

Exemplo.

"Nesta etapa nosso sistema já permite..."

Isso transmite sensação de progresso.

---

# Seções recorrentes

Algumas seções aparecem frequentemente ao longo do curso.

Sempre utilizar exatamente o mesmo título.

---

## 🧠 Pense

Objetivo.

Fazer o aluno parar antes de continuar.

Não responder imediatamente.

---

## 💡 Conceito

Apresentar um conceito importante.

Nunca iniciar diretamente com definições.

Sempre contextualizar antes.

---

## 🏗️ Decisão de Projeto

Talvez a seção mais importante do curso.

Sempre explicar:

- alternativas;
- decisão adotada;
- justificativa;
- consequências futuras.

Essa seção aproxima o aluno da realidade profissional.

---

## ⚠️ Erro comum

Mostrar implementações equivocadas.

Explicar por que parecem corretas.

Mostrar as consequências.

Nunca ridicularizar o erro.

---

## 🔍 Análise

Utilizar quando for necessário analisar uma implementação.

Comparar alternativas.

Discutir vantagens e desvantagens.

---

## 📌 Resumo

Encerrar o capítulo.

Apresentar apenas os principais pontos.

Não repetir todo o conteúdo.

---

## 🎯 Exercícios

Utilizar para atividades propostas.

Sempre que possível dividir em níveis.

---

## 🚀 Desafio

Exercícios sem solução única.

Estimular criatividade.

---

## 🧩 Aplicando ao Projeto Financeiro

Presente em praticamente todos os capítulos.

Não entregar implementação.

Estimular o aluno a adaptar o conhecimento.

---

# Diagramas

Diagramas são parte fundamental do curso.

Sempre preferir diagramas simples.

Evitar diagramas excessivamente completos.

Um bom diagrama explica uma única ideia.

---

# Mermaid

Sempre utilizar Mermaid quando possível.

Preferência:

Class Diagram

Flowchart

Sequence Diagram

State Diagram

Entity Relationship

---

# Diagramas de classes

Sempre utilizar quando:

- novas entidades surgirem;
- relacionamentos mudarem;
- responsabilidades forem redistribuídas.

Evitar diagramas enormes.

Atualizar o diagrama conforme o sistema evolui.

---

# Fluxogramas

Utilizar para:

- regras de negócio;
- fluxos de execução;
- algoritmos.

Nunca substituir código por fluxogramas.

Eles são complementares.

---

# Diagramas de sequência

Utilizar quando houver colaboração entre objetos.

Especialmente útil para mostrar:

Cliente

↓

Carrinho

↓

Produto

↓

Pagamento

---

# Tabelas

Utilizar tabelas para comparação.

Exemplo.

| Alternativa | Vantagem | Desvantagem |

Evitar tabelas muito grandes.

---

# Código

O código deve aparecer sempre depois da motivação.

Nunca iniciar uma seção com um bloco de código.

Sempre responder:

Por que esse código existe?

Antes de mostrar como ele funciona.

---

# Blocos de código

Evitar blocos gigantes.

Preferir:

explicação

↓

pequeno trecho

↓

explicação

↓

novo trecho

O aluno acompanha melhor.

---

# Comentários no código

Comentar apenas quando necessário.

Evitar comentar o óbvio.

Ruim.

```python
# Soma dois números
total = a + b
```

Bom.

```python
# Mantemos o subtotal no ItemCarrinho para preservar
# o preço praticado no momento da compra.
```

Comentários devem explicar decisões.

Não sintaxe.

---

# Imagens

Sempre que possível utilizar:

diagramas

ícones

esquemas

Evitar imagens decorativas.

Toda imagem deve ensinar alguma coisa.

---

# Emojis

Utilizar poucos emojis.

Sempre os mesmos.

Nunca utilizar emojis apenas para decorar.

Os emojis fazem parte da linguagem visual.

---

# Destaques

Utilizar negrito para:

- conceitos;
- nomes importantes;
- decisões.

Evitar excesso.

Se tudo estiver em destaque, nada estará.

---

# Citações

Utilizar citações para:

- princípios;
- boas práticas;
- regras importantes.

Exemplo.

> Um objeto deve conhecer apenas o necessário para cumprir sua responsabilidade.

---

# Resumos

Todo capítulo termina com um resumo.

O resumo deve caber em uma única tela.

O aluno deve conseguir revisar rapidamente antes da próxima aula.

---

# Continuidade

Sempre finalizar mostrando a evolução do projeto.

O aluno deve perceber claramente que o software está crescendo.

Nunca terminar um capítulo de forma abrupta.

---

# Objetivo final

Ao navegar pelo material, o aluno deve reconhecer imediatamente o tipo de conteúdo que está lendo apenas pela identidade visual utilizada.

A linguagem visual deve tornar o curso mais confortável de ler, mais fácil de revisar e mais agradável de acompanhar.