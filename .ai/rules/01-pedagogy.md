# Metodologia Pedagógica

## Objetivo deste documento

Este documento define como o conteúdo do curso deve ser ensinado.

Ele não estabelece o estilo de escrita, mas sim a sequência didática, a forma de apresentar conceitos e a maneira como o aluno deve ser conduzido ao longo do curso.

Todo material produzido deve seguir estas diretrizes.

---

# Filosofia de ensino

O curso deve ensinar o aluno a pensar como um desenvolvedor experiente.

O objetivo não é ensinar Python.

O objetivo não é ensinar sintaxe.

O objetivo é ensinar como tomar boas decisões de projeto.

Sempre que houver conflito entre apresentar um recurso da linguagem ou discutir uma decisão de projeto, priorizar a decisão de projeto.

---

# O aluno nunca deve decorar

O aluno não deve memorizar conceitos.

Ele deve compreendê-los.

Sempre que possível, evitar definições prontas.

Em vez de apresentar imediatamente um conceito, criar uma situação onde o próprio aluno perceba sua necessidade.

Exemplo inadequado:

> Coesão é o grau em que os elementos de uma classe estão relacionados.

Exemplo desejado:

> Imagine uma classe Produto que também envia e-mails, gera boletos, autentica usuários e controla estoque. Você considera essa uma boa modelagem? Por quê?

Somente depois da discussão apresentar o conceito de coesão.

---

# O ciclo de aprendizagem

Todo novo conceito deve seguir, preferencialmente, esta sequência.

## 1. Apresentar um problema

O aluno precisa sentir que existe uma dificuldade.

Sem problema não existe motivação.

---

## 2. Discutir possíveis soluções

Nunca apresentar imediatamente a solução correta.

Sempre levantar hipóteses.

Exemplo:

Quem deveria calcular o total do carrinho?

- Produto?
- Cliente?
- Carrinho?
- Item?

Essa discussão desenvolve pensamento crítico.

---

## 3. Modelar

Antes do código, discutir o domínio.

Identificar objetos.

Relacionamentos.

Responsabilidades.

Regras de negócio.

---

## 4. Implementar

Somente agora escrever código.

Cada decisão deve ser explicada.

Nunca escrever grandes blocos de código sem comentários.

---

## 5. Refatorar

Sempre que possível mostrar uma primeira solução simples.

Depois melhorá-la.

O aluno deve perceber que software evolui.

---

## 6. Generalizar

Ao final do assunto mostrar que aquele conceito poderá ser reutilizado em diversos contextos.

---

# A ordem importa

Nunca apresentar um recurso da linguagem antes que exista necessidade.

Exemplo inadequado.

Hoje aprenderemos Strategy.

Exemplo desejado.

Hoje nosso sistema possui três formas diferentes de calcular desconto.

Nossa implementação começou a ficar difícil de manter.

Como podemos resolver esse problema?

Somente depois apresentar Strategy.

---

# A curiosidade deve conduzir a aula

O aluno deve querer descobrir a resposta.

O texto deve provocar perguntas.

Alguns exemplos.

- Será que essa classe realmente deveria fazer isso?

- Existe uma forma melhor?

- O que acontecerá quando adicionarmos uma nova funcionalidade?

- Como evitar alterar esse código novamente?

Essas perguntas tornam a leitura ativa.

---

# Mostrar software evoluindo

O projeto nunca deve parecer completamente planejado.

Novas necessidades devem surgir naturalmente.

Exemplo.

Primeiro existe um Produto.

Depois surge Categoria.

Depois Carrinho.

Depois Pedido.

Depois Pagamento.

Depois diferentes meios de pagamento.

Depois cupons.

Depois estoque.

Essa evolução deve parecer consequência das decisões anteriores.

---

# Valorizar a tomada de decisão

O foco da aula nunca deve ser:

"Veja este código."

O foco deve ser:

"Veja por que escolhemos esse código."

Explicar alternativas é tão importante quanto mostrar a solução adotada.

---

# Sempre comparar alternativas

Sempre que existir mais de uma solução razoável, apresentá-las.

Exemplo.

Guardar uma lista de Produtos dentro do Carrinho.

ou

Criar ItemCarrinho.

Discutir vantagens.

Desvantagens.

Impactos futuros.

Somente então decidir.

---

# Mostrar consequências

Toda decisão possui consequências.

Sempre explicá-las.

Exemplo.

"Hoje essa solução parece mais trabalhosa.

Entretanto, quando implementarmos cupons de desconto ela evitará alterações em diversas classes."

Essa antecipação aumenta a percepção arquitetural do aluno.

---

# Introduzir conceitos apenas quando necessários

Evitar capítulos puramente teóricos.

Cada conceito deve resolver um problema existente.

Se ainda não existe necessidade para determinado padrão ou princípio, ele ainda não deve aparecer.

---

# Utilizar perguntas socráticas

Ao longo do texto utilizar perguntas como ferramenta de ensino.

Exemplos.

Quem deveria conhecer essa informação?

Quem realmente precisa dessa dependência?

O objeto possui informações suficientes para executar essa tarefa?

Estamos violando alguma responsabilidade?

Essas perguntas estimulam reflexão.

---

# Trabalhar com hipóteses

Sempre que possível construir hipóteses.

Exemplo.

"E se amanhã surgir um novo meio de pagamento?"

"E se houver desconto para clientes VIP?"

"E se o preço do produto mudar depois que ele entrar no carrinho?"

Essas hipóteses justificam futuras evoluções.

---

# O código nunca é o protagonista

O protagonista é o problema.

O código é apenas uma consequência.

Evitar capítulos compostos apenas por código.

Antes de cada trecho o aluno deve compreender por que ele existe.

Depois do código o aluno deve compreender por que ele foi escrito daquela maneira.

---

# Evitar exemplos artificiais

Sempre utilizar exemplos do domínio do E-Commerce.

Evitar exemplos clássicos como:

Animal

Pessoa

Conta Bancária

Carro

Funcionário

Esses exemplos somente poderão ser utilizados para explicações extremamente rápidas.

Todo aprendizado deve permanecer conectado ao projeto principal.

---

# O professor pensa em voz alta

Durante o texto, o professor deve demonstrar seu raciocínio.

Exemplo.

"Poderíamos armazenar apenas uma lista de produtos.

Mas espere...

Como controlaríamos a quantidade?

Talvez exista uma abstração melhor."

O aluno deve acompanhar esse processo mental.

---

# O aluno participa da construção

Sempre criar momentos onde o aluno possa responder antes da solução aparecer.

Exemplos.

Pense.

Reflita.

Discuta.

Faça uma previsão.

O que você faria?

Esses momentos aumentam o engajamento.

---

# O erro é uma ferramenta didática

Mostrar soluções ruins.

Mostrar código mal projetado.

Mostrar responsabilidades incorretas.

Mostrar classes excessivamente acopladas.

Depois explicar os problemas.

O aluno aprende comparando.

---

# Pequenas vitórias

Cada capítulo deve terminar com sensação de progresso.

Mesmo pequenas implementações devem parecer uma conquista.

Evitar capítulos onde apenas teoria é apresentada.

---

# Conectar os capítulos

Ao final de cada capítulo responder três perguntas.

O que aprendemos?

Como isso melhorou nosso sistema?

O que faremos a seguir?

Essa conexão mantém a continuidade do curso.

---

# Revisões constantes

Sempre revisar naturalmente conceitos anteriores.

Nunca criar grandes capítulos de revisão.

Exemplo.

Ao introduzir composição, relembrar rapidamente encapsulamento.

Ao falar sobre Strategy, revisar responsabilidade das classes.

O conhecimento deve ser continuamente reforçado.

---

# O Projeto Financeiro

Ao final de praticamente todos os capítulos criar uma pequena seção.

## Aplicando ao Projeto Financeiro

Nela o aluno deverá refletir.

Como esse conceito pode ser utilizado em seu projeto?

Não fornecer implementação.

Fornecer apenas direcionamentos.

O objetivo é desenvolver autonomia.

---

# Encerramento de cada capítulo

Todo capítulo deve terminar com quatro elementos.

## Resumo

Apresentar os principais conceitos aprendidos.

---

## O que mudou no sistema

Mostrar claramente a evolução do projeto.

---

## Aplicação no Projeto Financeiro

Explicar como o aluno pode utilizar aquele conhecimento.

---

## Preparação para o próximo capítulo

Criar expectativa.

Mostrar qual problema surgirá a seguir.

O aluno deve terminar o capítulo querendo continuar.

---

# Objetivo final

Ao concluir o curso, o aluno deverá perceber que Programação Orientada a Objetos não consiste em criar classes.

Consiste em compreender problemas, modelar soluções e distribuir corretamente responsabilidades entre objetos que colaboram entre si.

Toda aula deve aproximar o aluno desse objetivo.