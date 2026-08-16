# Entrega da Primeira Parte do Projeto

Dois módulos ficaram para trás. No Módulo 1, você tirou do papel as primeiras classes do seu Sistema de Controle Financeiro Pessoal. No Módulo 2, ensinou esse sistema a fechar um período, conferir se as contas batem e gerar um resumo. Ninguém fez isso por você — cada capítulo trouxe uma pergunta, e você precisou responder sozinho, adaptando ao seu próprio domínio o que viu acontecer no E-Commerce.

Esse é exatamente o ponto do exercício: **software evolui porque o negócio evolui**, e agora é hora de parar, olhar pra trás e consolidar o que evoluiu no seu projeto antes de seguirmos para o Módulo 3.

---

## O que você já deveria ter construído

- ✔ `Conta` — nome, saldo (Capítulo 4)
- ✔ `Categoria` — nome, usada para classificar gastos (Capítulo 4)
- ✔ `Lancamento` — descrição, valor, data, categoria (Capítulo 4)
- ✔ `Fechamento` — consolida os lançamentos de um período (Capítulo 5)
- ✔ `Conciliacao` — verifica se débitos e créditos batem (Capítulo 6)
- ✔ `Extrato` — resume os fechamentos de um período (Capítulo 7)
- ✔ Testes automatizados para cada uma dessas classes

Se algum desses itens ainda não existe no seu projeto, esse é o momento de voltar ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** das classes listadas acima, organizado como um pacote Python (mesma ideia de `ecommerce/` → `financeiro/` usada desde o Capítulo 4).
2. **Testes automatizados** (`pytest`) cobrindo casos de sucesso e casos de erro, todos passando.
3. **Um documento curto** (`README.md` ou similar) respondendo, com justificativa, as perguntas de projeto que os Capítulos 5 a 7 deixaram em aberto:
    - No `Fechamento`, os lançamentos originais foram copiados ou referenciados? Por quê?
    - `Conciliacao` virou uma classe própria ou um método de `Fechamento`? Por quê?
    - O que acontece quando não há lançamentos no período, ou quando a conciliação não bate?

Não existe uma única resposta certa para essas perguntas — o que será avaliado é se a decisão foi tomada conscientemente e se o código é consistente com ela.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta — converse com seu professor se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Modelagem das entidades (`Conta`, `Categoria`, `Lancamento`) | 2,0 | Nomes fiéis ao domínio, responsabilidades bem distribuídas, encapsulamento |
| `Fechamento` | 1,5 | Consolidação correta do período; decisão sobre cópia/referência justificada |
| `Conciliacao` | 1,5 | Invariante débito = crédito validada; erro claro quando não bate |
| `Extrato` | 1,5 | Resumo correto do período; decisão sobre onde mora a responsabilidade |
| Testes automatizados | 2,0 | Casos de sucesso e de erro cobertos, suíte inteira passando |
| Decisões de projeto documentadas | 1,0 | Perguntas dos capítulos respondidas e justificadas |
| Organização e coesão do código | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

---

Este é um checkpoint formativo, não o fim do projeto. O objetivo não é ter um sistema perfeito, é ter um sistema **seu**, construído com decisões que você consegue explicar. No Módulo 3, tanto o E-Commerce quanto o seu Projeto Financeiro vão continuar evoluindo — e as bases que você consolidar aqui vão sustentar tudo o que vem depois.
