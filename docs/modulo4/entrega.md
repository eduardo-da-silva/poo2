# Entrega da Terceira Parte do Projeto

O Módulo 4 tratou de um problema que aparece em todo sistema que cresce: criar objetos também é uma responsabilidade, e espalhá-la com `if/elif` acopla quem cria a tudo que pode ser criado. A saída foi isolar a criação em **factories** — Simple Factory quando a decisão é um dado simples, Factory Method quando quem cria já é uma família de classes — e, no fim, parar de espalhar a montagem das dependências, com **Injeção de Dependências** e uma **raiz de composição**.

No E-Commerce isso apareceu em formas de pagamento, meios de entrega e notificações. No seu Projeto Financeiro, o mesmo padrão se repete em pelo menos três lugares: leitores de arquivo, importadores por origem e exportadores de relatório.

É hora de consolidar de novo antes de seguirmos para o Módulo 5.

---

## O que você já deveria ter construído

- ✔ Uma interface `Leitor` (equivalente), com pelo menos duas implementações (CSV, OFX, JSON…), criadas por uma factory — `CriadorLeitor` ou equivalente (Capítulo 12)
- ✔ Exportadores de relatório (`ExportadorRelatorio` equivalente), com pelo menos duas implementações (PDF, CSV, HTML…), usando **Factory Method** (Capítulo 13)
- ✔ Importadores por origem/banco, com uma factory decidindo qual instanciar — `CriadorImportador` ou equivalente (Capítulo 14)
- ✔ Um serviço de coordenação (equivalente ao `ServicoPedido`) que **recebe** seus colaboradores por injeção, e uma raiz de composição que monta o grafo num único lugar (Capítulo 15)
- ✔ Testes automatizados para tudo isso, usando dublês onde fizer sentido

Se algum desses itens ainda não existe, volte ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** das interfaces, implementações, factories e serviços acima, organizado como pacote Python (mesma estrutura `financeiro/` usada desde o Módulo 1).
2. **Testes automatizados** (`pytest`) cobrindo casos de sucesso e de erro, todos passando. Pelo menos um teste deve trocar um colaborador real por um dublê, sem editar o serviço.
3. **Um documento curto** (`README.md` ou similar) respondendo, com justificativa:
    - Em cada caso (leitor, importador, exportador), você usou Simple Factory ou Factory Method? O que te fez escolher?
    - Nos seus serviços, o que é **injetado** e o que ainda é **criado internamente**? Por quê?
    - Onde está sua raiz de composição? Que colaborador você conseguiria substituir hoje sem editar nenhum serviço?

Como nos checkpoints anteriores, não existe uma única resposta certa — o que será avaliado é se a decisão foi consciente e se o código é consistente com ela.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta — converse com seu professor se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Factory de leitores | 1,5 | Isola a criação; extensível sem editar quem usa o leitor |
| Factory Method de exportadores | 1,5 | Cada formato decide seu produto; pelo menos duas implementações funcionando |
| Factory de importadores | 1,5 | Decisão de criação por origem, sem `if/elif` espalhado |
| Injeção de dependências | 2,0 | Serviços recebem colaboradores prontos; nada de `new` interno; raiz de composição única |
| Testes automatizados | 2,0 | Sucesso e erro cobertos; suíte passando; pelo menos um dublê no lugar de um colaborador real |
| Decisões de projeto documentadas | 1,0 | Perguntas do README respondidas e justificadas |
| Organização e coesão do código | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

---

Assim como nos checkpoints anteriores, isto é formativo — o objetivo é ter decisões que você consegue explicar, não um sistema perfeito. No Módulo 5, o E-Commerce e o seu Projeto Financeiro passam a separar o domínio da infraestrutura: persistência, repositórios e camadas.
