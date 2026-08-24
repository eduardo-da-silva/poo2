# Entrega da Segunda Parte do Projeto

O Módulo 3 introduziu o primeiro padrão de projeto do curso: Strategy. Não foi apresentado como uma receita pronta — apareceu porque um `if/elif` de desconto começou a incomodar, e voltou a aparecer mais duas vezes (cupom, frete) porque o mesmo formato de problema se repetiu. Se o seu Projeto Financeiro seguiu o mesmo caminho, você já sentiu essa repetição em pelo menos três lugares: rendimento, juros, correção monetária.

É hora de consolidar de novo antes de seguirmos para o Módulo 4.

---

## O que você já deveria ter construído

- ✔ Uma interface de estratégia de desconto (equivalente a `EstrategiaDesconto`), com pelo menos duas implementações (Capítulo 9)
- ✔ Uma entidade equivalente a `Cupom`, com validade e regra de desconto (Capítulo 10)
- ✔ Uma interface de estratégia de frete (equivalente a `EstrategiaFrete`), com pelo menos duas implementações (Capítulo 11)
- ✔ No Projeto Financeiro: estratégias para tipos de rendimento, tipos de juros e correções monetárias — cada uma decidida por você (classes separadas, reaproveitamento por composição, ou uma única interface para mais de um conceito)
- ✔ Testes automatizados para tudo isso

Se algum desses itens ainda não existe, volte ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** das interfaces e implementações acima, organizado como pacote Python (mesma estrutura `financeiro/` já usada desde o Módulo 1).
2. **Testes automatizados** (`pytest`) cobrindo casos de sucesso e de erro, todos passando.
3. **Um documento curto** (`README.md` ou similar) respondendo, com justificativa:
    - Suas estratégias de rendimento, juros e correção monetária são interfaces separadas ou a mesma interface reaproveitada? Por quê?
    - Onde a estratégia escolhida é guardada — passada por parâmetro, ou como atributo de outra entidade (como fizemos com `Cupom` em relação a `Pedido`)? Por quê?
    - Que novo tipo de regra você conseguiria adicionar hoje sem editar nenhuma classe já existente?

Como no checkpoint anterior, não existe uma única resposta certa — o que será avaliado é se a decisão foi consciente e se o código é consistente com ela.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta — converse com seu professor se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Interface de estratégia (desconto e frete, ou seus equivalentes) | 2,0 | Contrato bem definido, aberto para extensão sem alterar código existente (Open/Closed) |
| Implementações de desconto | 1,5 | Pelo menos duas regras diferentes funcionando através da mesma interface |
| Entidade equivalente a `Cupom` | 1,5 | Validade verificada corretamente, composição com a estratégia de desconto (sem duplicar lógica) |
| Implementações de frete | 1,5 | Pelo menos duas regras diferentes, combinadas corretamente com desconto no valor final |
| Testes automatizados | 2,0 | Casos de sucesso e de erro cobertos, suíte inteira passando |
| Decisões de projeto documentadas | 1,0 | Perguntas respondidas e justificadas |
| Organização e coesão do código | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

---

Assim como no checkpoint anterior, isso é formativo — o objetivo é ter decisões que você consegue explicar, não um sistema perfeito. No Módulo 4, o E-Commerce e o seu Projeto Financeiro vão continuar evoluindo juntos, agora enfrentando um problema diferente: como criar objetos sem espalhar condicionais na hora de decidir o quê instanciar.
