# Entrega Final do Projeto

O Módulo 6 fecha o curso. Em seis módulos, o seu Projeto Financeiro passou de um conjunto de classes soltas a um sistema com domínio protegido, variações isoladas, criação controlada, camadas, persistência e reações a acontecimentos. A cada módulo houve um checkpoint. Esta é a entrega **final**: ela avalia o projeto como um todo, do Capítulo 1 ao 22, mais **um padrão à sua escolha** no catálogo do bônus (Capítulo 23).

Diferente dos checkpoints, aqui a pergunta não é "o que foi pedido neste módulo?", e sim: **o seu sistema, como está, é um sistema que consegue envelhecer bem?**

---

## O que você já deveria ter construído

- ✔ Um **domínio** modelado, com entidades, invariantes protegidas e estados com transições válidas (Capítulos 1 a 7)
- ✔ **Variações de comportamento** isoladas em contratos, com ao menos uma aplicação de Strategy (Capítulos 8 a 11)
- ✔ **Criação** controlada por factories e dependências **injetadas**, com raiz de composição (Capítulos 12 a 15)
- ✔ **Repositórios** em pelo menos duas implementações (memória e SQLite), **casos de uso** e **três camadas** com a regra de dependência verificada por teste (Capítulos 16 a 19)
- ✔ **Persistência** em SQLite dos dados principais do seu domínio: ao reiniciar o programa, os dados continuam lá (Capítulos 16 e 17)
- ✔ Um **ponto de entrada**: pode ser um cenário com dados fixos, um menu de terminal ou uma API REST (Capítulo 22)
- ✔ **Eventos de domínio** publicados por um barramento, com pelo menos **dois manipuladores** independentes (Capítulos 20 e 21)
- ✔ Uma **decisão consciente** sobre o que acontece quando uma reação falha (Capítulo 22)
- ✔ **Um padrão do catálogo do bônus**, escolhido, pesquisado e implementado por você, para resolver uma dor real do seu projeto (Capítulo 23)

Se algum desses itens ainda não existe, volte ao capítulo correspondente antes de entregar.

---

## O que deve ser entregue

1. **Código-fonte** organizado como pacote Python, com as três camadas visíveis (`dominio/`, `aplicacao/`, `infraestrutura/`) e a raiz de composição fora delas, mais **uma interface** para usar o sistema: cenário fixo, menu de terminal ou REST. Deve existir um `main.py` na raiz, de modo que `python main.py` (com os argumentos que você precisar) rode o sistema. A interface fica fora das camadas internas e só chama os casos de uso. O sistema precisa **persistir** os dados principais em SQLite, e isso deve ser possível de demonstrar rodando o programa duas vezes.
2. **Testes automatizados** (`pytest`), todos passando, cobrindo casos de sucesso e de erro. Devem incluir:
    - testes das regras de domínio (invariantes, transições);
    - uma suíte de contrato de repositório que roda contra **todas** as implementações;
    - testes de arquitetura com no mínimo duas regras de dependência;
    - testes do **padrão do bônus** que você escolheu;
    - testes de quem **publica** um evento e de cada **manipulador** separadamente;
    - pelo menos um teste em que uma reação **falha**, mostrando o que o sistema faz.
3. **Um documento de decisões** (`README.md` ou similar) respondendo, com justificativa:
    - **Quais padrões você usou e para qual problema?** Para cada um, qual era a dor antes dele.
    - **Quais padrões você considerou e recusou?** Por que não eram necessários?
    - Que **fatos** o seu sistema anuncia? Por que esses e não outros? Os eventos carregam objetos ou identificadores?
    - Se uma reação a um evento falha, o que acontece? Você **propaga** ou **isola**? Como a falha é vista por alguém?
    - O que no seu sistema **precisa ser atômico**? Está dentro de uma única operação?
    - O que no seu sistema **não está persistido**? O que seria preciso persistir para ele ser completo, e em que ponto valeria usar um **ORM**?
    - Qual interface você escolheu (cenário, menu ou REST) e por quê? O que mudaria nas camadas internas se você trocasse por outra?
    - Se o sistema passasse a usar **mensageria de verdade** (uma fila externa), quais arquivos mudariam? Quais não?
    - O que você mudaria, se começasse de novo?
4. **O padrão do bônus** (15% da nota), escolhido **na lista do catálogo do Capítulo 23**: Decorator, State, Adapter, Composite, Chain of Responsibility, Command com handler ou Builder. Outro padrão só com aprovação prévia do professor. O Singleton não entra, porque no curso ele é um alerta. A pesquisa fica por sua conta, e o que se avalia é o raciocínio, não o padrão em si:
    - **A dor é real?** Descreva, no seu projeto, o problema que existia antes do padrão e como o código ficou depois.
    - **A implementação está correta e testada?**
    - **O que você pesquisou?** Indique as fontes, o que adaptou ao seu caso e o **custo** que o padrão trouxe (mais classes, mais indireção, o que ficou mais difícil).
    - **Por que ele e não outro da lista?** Cite pelo menos um padrão que você considerou e descartou.

    Aplicar um padrão onde não havia problema, só para pontuar, vale menos do que escolher um que resolve algo e explicar bem.
5. **Apresentação curta** (opcional, a combinar com o professor): cinco a dez minutos mostrando o caminho de um lançamento ou pedido pelo sistema, do início ao último manipulador.

Como nos checkpoints, não existe uma única resposta certa. O que será avaliado é se a decisão foi **consciente**, se o código é **consistente** com ela, e se você consegue **explicá-la**.

---

## Como será avaliado

Nota de 0 a 10, distribuída pelos critérios abaixo. Os pesos são uma proposta, e o professor pode ajustá-los se algo aqui não fizer sentido para o seu caso.

| Critério | Peso | O que é avaliado |
|---|---|---|
| Domínio e regras de negócio | 0,5 | Entidades coesas; invariantes protegidas; estados com transições válidas |
| Variações e criação | 1,0 | Contratos para o que varia; factories; dependências injetadas; raiz de composição única |
| Persistência e camadas | 1,5 | Repositório com contrato e mais de uma implementação; casos de uso; domínio sem import de infraestrutura; DIP |
| Eventos | 1,5 | Eventos como fatos imutáveis; barramento; manipuladores independentes; falha de uma reação tratada de forma consciente |
| Testes automatizados | 1,5 | Contrato rodando em todas as implementações; testes de arquitetura; publicadores e manipuladores testados separadamente |
| Interface (ponto de entrada) | 1,0 | Funciona e é demonstrável; só chama casos de uso; fora das camadas internas; erros traduzidos para a linguagem do meio |
| **Padrão do bônus** (pesquisado e implementado) | 1,5 | Dor real no projeto; implementação correta e testada; fontes, adaptação e custo explicados; escolha justificada frente a outro padrão |
| Documento de decisões | 1,0 | Perguntas respondidas e justificadas; padrões usados **e recusados** com argumento |
| Organização e legibilidade | 0,5 | Estrutura de pacotes, nomes, sem responsabilidades misturadas |

!!! note "Sugestão de peso no conjunto do curso"

    Como esta entrega cobre o projeto inteiro, a sugestão é que ela valha **o dobro** de um checkpoint no conjunto das entregas do Projeto Financeiro. É uma proposta, que o professor pode alterar.

---

!!! info "📅 Prazo e entrega"

    Entregue um link de repositório Git (GitHub ou GitLab), com acesso liberado para o professor, até **[DATA A DEFINIR]**.

---

Esta entrega é, ao mesmo tempo, avaliação e retrospectiva. O objetivo não é um sistema perfeito: é um sistema cujas decisões você consegue explicar, e que você sabe como fazer crescer.
