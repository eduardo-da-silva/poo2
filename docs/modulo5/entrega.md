# Entrega da Quarta Parte do Projeto

O Módulo 5 tratou de uma pergunta que todo sistema que cresce acaba enfrentando: **onde ficam as coisas, e quem pode saber disso?** A resposta foi separar o que o sistema *é* (domínio) do que ele *faz* (aplicação) e de como fala com o mundo externo (infraestrutura), com uma regra simples: as dependências apontam para dentro, e as abstrações pertencem a quem as usa.

No E-Commerce isso apareceu em repositórios, SQLite, casos de uso e camadas. No seu Projeto Financeiro, o mesmo caminho se repete: lançamentos que precisam sobreviver ao programa, serviços que coordenam importações e relatórios, e uma estrutura que precisa dizer o que é cada coisa.

É hora de consolidar de novo antes de seguirmos para o Módulo 6.

---

## O que você já deveria ter construído

- ✔ Identidade (`id`) nas entidades principais e um repositório (contrato + implementação em memória) para **lançamentos** — e para o que mais fizer sentido no seu domínio (Capítulo 16)
- ✔ Uma segunda implementação do mesmo repositório, em **SQLite**, passando na **mesma suíte de contrato** que a implementação em memória (Capítulo 17)
- ✔ Código organizado em **domínio**, **aplicação** e **infraestrutura**, com **casos de uso** no lugar de um serviço genérico (Capítulo 18)
- ✔ Uma **raiz de composição** capaz de montar o sistema com pelo menos duas configurações de armazenamento (Capítulo 19)
- ✔ **Testes de arquitetura** que verificam a regra de dependência (Capítulos 18 e 19)

Se algum desses itens ainda não existe, volte ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** organizado como pacote Python, com as três camadas visíveis na estrutura de pastas (`dominio/`, `aplicacao/`, `infraestrutura/`) e a raiz de composição fora delas.
2. **Testes automatizados** (`pytest`) cobrindo casos de sucesso e de erro, todos passando. Devem incluir:
    - uma suíte de contrato de repositório que roda contra **todas** as implementações;
    - pelo menos um teste que prove que os dados **sobrevivem a um reinício** (arquivo real em diretório temporário);
    - testes de arquitetura com no mínimo duas regras de dependência.
3. **Um documento curto** (`README.md` ou similar) respondendo, com justificativa:
    - Que consultas o seu repositório oferece além de `obter` e `listar`? Por que elas fazem parte do contrato?
    - O que você **decidiu não persistir** nesta etapa e por quê?
    - Houve algum teste que passava em memória e falhou no SQLite? O que isso revelou?
    - Quantas violações de dependência seu teste de arquitetura encontrou na primeira vez? Como você as resolveu?
    - Se amanhã você quisesse trocar o SQLite por um ORM, **quais arquivos mudariam**? Quais não?

Como nos checkpoints anteriores, não existe uma única resposta certa — o que será avaliado é se a decisão foi consciente e se o código é consistente com ela.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta — converse com seu professor se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Repositórios e contrato | 2,0 | Contrato na linguagem do domínio; devolve objetos completos; implementação em memória funcional |
| Persistência em SQLite | 2,0 | Mesmo contrato, mapeamento correto, dados sobrevivem ao reinício |
| Casos de uso e camadas | 2,0 | Uma classe por intenção; camadas visíveis; domínio sem import de infraestrutura |
| Inversão de dependências e composição | 1,5 | Contratos do lado de quem usa; raiz de composição única; duas configurações de armazenamento |
| Testes automatizados | 1,5 | Contrato rodando em todas as implementações; teste de reinício; testes de arquitetura |
| Decisões de projeto documentadas | 0,5 | Perguntas do README respondidas e justificadas |
| Organização e coesão do código | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

---

Assim como nos checkpoints anteriores, isto é formativo — o objetivo é ter decisões que você consegue explicar, não um sistema perfeito. No Módulo 6, o E-Commerce e o seu Projeto Financeiro passam a reagir a acontecimentos sem que quem os causa precise conhecer quem reage: eventos.
