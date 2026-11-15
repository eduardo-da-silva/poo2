# Entrega Final do Projeto

O Módulo 6 fecha o curso. Em seis módulos, o seu Projeto Financeiro passou de um conjunto de classes soltas a um sistema com domínio protegido, variações isoladas, criação controlada, camadas, persistência e reações a acontecimentos. A cada módulo houve um checkpoint. Esta é a entrega **final**: ela avalia o projeto como um todo, do Capítulo 1 ao 23.

Diferente dos checkpoints, aqui a pergunta não é "o que foi pedido neste módulo?", e sim: **o seu sistema, como está, é um sistema que consegue envelhecer bem?**

---

## O que você já deveria ter construído

- ✔ Um **domínio** modelado, com entidades, invariantes protegidas e estados com transições válidas (Capítulos 1 a 7)
- ✔ **Variações de comportamento** isoladas em contratos, com ao menos uma aplicação de Strategy (Capítulos 8 a 11)
- ✔ **Criação** controlada por factories e dependências **injetadas**, com raiz de composição (Capítulos 12 a 15)
- ✔ **Repositórios** em pelo menos duas implementações (memória e SQLite), **casos de uso** e **três camadas** com a regra de dependência verificada por teste (Capítulos 16 a 19)
- ✔ **Eventos de domínio** publicados por um barramento, com pelo menos **dois manipuladores** independentes (Capítulos 20 e 21)
- ✔ Pelo menos **um decorator** de comportamento transversal, como log ou medição de tempo (Capítulo 22)
- ✔ Uma **decisão consciente** sobre o que acontece quando uma reação falha (Capítulo 23)

Se algum desses itens ainda não existe, volte ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** organizado como pacote Python, com as três camadas visíveis (`dominio/`, `aplicacao/`, `infraestrutura/`) e a raiz de composição fora delas.
2. **Testes automatizados** (`pytest`), todos passando, cobrindo casos de sucesso e de erro. Devem incluir:
    - testes das regras de domínio (invariantes, transições);
    - uma suíte de contrato de repositório que roda contra **todas** as implementações;
    - testes de arquitetura com no mínimo duas regras de dependência;
    - testes de quem **publica** um evento e de cada **manipulador** separadamente;
    - pelo menos um teste em que uma reação **falha**, mostrando o que o sistema faz.
3. **Um documento de decisões** (`README.md` ou similar) respondendo, com justificativa:
    - **Quais padrões você usou e para qual problema?** Para cada um, qual era a dor antes dele.
    - **Quais padrões você considerou e recusou?** Por que não eram necessários?
    - Que **fatos** o seu sistema anuncia? Por que esses e não outros? Os eventos carregam objetos ou identificadores?
    - Se uma reação a um evento falha, o que acontece? Você **propaga** ou **isola**? Como a falha é vista por alguém?
    - O que no seu sistema **precisa ser atômico**? Está dentro de uma única operação?
    - Se o sistema passasse a usar **mensageria de verdade** (uma fila externa), quais arquivos mudariam? Quais não?
    - O que você mudaria, se começasse de novo?
4. **Apresentação curta** (opcional, a combinar com o professor): cinco a dez minutos mostrando o caminho de um lançamento ou pedido pelo sistema, do início ao último manipulador.

Como nos checkpoints, não existe uma única resposta certa. O que será avaliado é se a decisão foi **consciente**, se o código é **consistente** com ela, e se você consegue **explicá-la**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta, e o professor pode ajustá-los se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Domínio e regras de negócio | 1,0 | Entidades coesas; invariantes protegidas; estados com transições válidas |
| Variações e criação | 1,5 | Contratos para o que varia; factories; dependências injetadas; raiz de composição única |
| Persistência e camadas | 2,0 | Repositório com contrato e mais de uma implementação; casos de uso; domínio sem import de infraestrutura; DIP |
| Eventos e comportamento transversal | 2,0 | Eventos como fatos imutáveis; barramento; manipuladores independentes; decorator; falha tratada de forma consciente |
| Testes automatizados | 1,5 | Contrato rodando em todas as implementações; testes de arquitetura; publicadores e manipuladores testados separadamente |
| Documento de decisões | 1,5 | Perguntas respondidas e justificadas; padrões usados **e recusados** com argumento |
| Organização e legibilidade | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

!!! note "Sugestão de peso no conjunto do curso"

    Como esta entrega cobre o projeto inteiro, a sugestão é que ela valha **o dobro** de um checkpoint no conjunto das entregas do Projeto Financeiro. É uma proposta, que o professor pode alterar.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

Esta entrega é, ao mesmo tempo, avaliação e retrospectiva. O objetivo não é um sistema perfeito: é um sistema cujas decisões você consegue explicar, e que você sabe como fazer crescer.
