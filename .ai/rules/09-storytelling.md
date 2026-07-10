# Storytelling e Evolução do Sistema

## Objetivo

Este curso acompanha o desenvolvimento de um único sistema ao longo de todos os módulos.

O objetivo não é apresentar exemplos isolados, mas sim permitir que o aluno acompanhe a evolução de um software real, percebendo como novas necessidades de negócio levam naturalmente à evolução da arquitetura e da modelagem.

Cada capítulo representa um novo momento da vida da empresa.

---

# A empresa

Existe apenas uma empresa fictícia durante todo o curso.

Ela possui um e-commerce relativamente simples, mas em constante crescimento.

Inicialmente, seus processos são manuais ou pouco estruturados.

À medida que o curso avança, novas necessidades surgem, exigindo mudanças na modelagem, na arquitetura e na implementação.

A empresa deve permanecer a mesma durante todo o curso.

Nunca criar um novo sistema apenas para demonstrar um conceito.

---

# Evolução gradual

Cada capítulo deve representar uma evolução natural do sistema.

Nunca introduzir funcionalidades complexas antes que elas sejam necessárias.

Sempre partir de uma versão simples e funcional.

O sistema deve crescer de forma incremental.

Exemplo:

- cadastro de produtos
- clientes
- pedidos
- estoque
- pagamentos
- descontos
- cupons
- notificações
- persistência
- integrações

A ordem pode variar conforme o módulo, mas sempre deve parecer consequência da evolução do negócio.

---

# O problema vem antes da solução

Novos conceitos de Programação Orientada a Objetos nunca devem aparecer apenas porque fazem parte da ementa.

Primeiro surge um problema.

Depois o aluno percebe as limitações da solução atual.

Somente então uma nova técnica, princípio ou padrão é apresentado.

Evitar frases como:

> Agora aprenderemos Strategy.

Preferir:

> A empresa passou a oferecer diferentes políticas de desconto. Como organizar essa lógica sem criar um grande bloco de condicionais?

---

# Situação da empresa

Todo capítulo deve começar contextualizando o estado atual do projeto.

O aluno deve entender claramente:

- o que já existe;
- o que ainda não existe;
- qual problema surgiu;
- qual será o objetivo daquele capítulo.

Essa contextualização deve ser curta (2 a 5 parágrafos).

---

# Estado atual do sistema

Sempre que fizer sentido, apresentar resumidamente o que já foi construído.

Exemplo:

✔ Produtos

✔ Categorias

✔ Clientes

✘ Pedidos

✘ Pagamentos

✘ Estoque

Esse quadro ajuda o aluno a perceber a evolução do projeto.

---

# Decisões de projeto

Sempre que uma decisão importante for tomada, explicar rapidamente as alternativas consideradas.

Sempre responder perguntas como:

- Por que criar uma nova classe?
- Por que não colocar esse método em Produto?
- Por que usar composição?
- Por que evitar herança?

O objetivo não é apenas mostrar a solução, mas ensinar o processo de tomada de decisão.

---

# Pequenas histórias

É recomendável utilizar pequenas situações do cotidiano da empresa.

Exemplos:

- um cliente solicitou desconto;
- um produto ficou sem estoque;
- surgiu uma nova forma de pagamento;
- o gerente pediu um relatório;
- houve necessidade de cancelar um pedido.

Essas situações devem ser simples e objetivas.

Evitar criar narrativas longas.

O foco continua sendo o desenvolvimento de software.

---

# Continuidade

Cada capítulo deve terminar preparando naturalmente o próximo.

Evitar encerramentos abruptos.

Sempre indicar qual será o próximo desafio enfrentado pela empresa.

O aluno deve sentir que está acompanhando um único projeto em constante evolução.

---

# Coerência

Todas as entidades, regras e exemplos devem permanecer coerentes ao longo do curso.

Evitar alterar nomes, conceitos ou regras de negócio sem justificativa.

Caso uma regra mude, explicar que a mudança ocorreu porque a empresa evoluiu ou porque um novo requisito surgiu.

---

# O aluno faz parte da equipe

Sempre que possível, escrever como se o aluno estivesse participando do desenvolvimento do sistema.

Exemplos:

- Nossa próxima tarefa será...
- Precisamos decidir...
- Vamos implementar...
- Agora precisamos reorganizar o código...

Evitar criar uma narrativa em primeira pessoa como personagem ("eu fiz", "eu pensei"). A ideia é colocar o leitor no papel de desenvolvedor da equipe.

---

# O objetivo do storytelling

O storytelling existe para conectar os capítulos.

Ele nunca deve substituir o conteúdo técnico.

Seu papel é fornecer contexto, motivação e continuidade, tornando os conceitos mais naturais e memoráveis.

O foco principal do curso continua sendo ensinar Engenharia de Software e Programação Orientada a Objetos.