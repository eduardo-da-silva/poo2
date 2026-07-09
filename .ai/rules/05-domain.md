# Domínio do Sistema de E-Commerce

## Objetivo deste documento

Este documento define o domínio utilizado durante todo o curso.

Ele funciona como uma especificação viva do sistema.

Seu objetivo é impedir inconsistências entre diferentes capítulos do curso.

Sempre que houver dúvida sobre responsabilidades, entidades ou regras de negócio, este documento deve ser consultado.

Este documento deve evoluir junto com o curso.

Ele não representa a implementação.

Ele representa o conhecimento do domínio.

---

# Princípios

O software deve refletir o domínio.

Nunca adaptar o domínio apenas para facilitar a implementação.

Sempre que uma decisão de implementação entrar em conflito com uma boa modelagem do domínio, priorizar o domínio.

O código deve servir ao negócio.

Não o contrário.

---

# Linguagem Ubíqua

Todos os capítulos devem utilizar sempre os mesmos nomes.

Evitar sinônimos.

Exemplo.

Sempre utilizar:

Produto

Nunca:

Mercadoria

Item

Artigo

Da mesma forma:

Cliente

Categoria

Carrinho

Pedido

Pagamento

Cupom

ItemCarrinho

ItemPedido

Essa consistência reduz a carga cognitiva do aluno.

---

# Evolução do domínio

O sistema não será implementado de uma única vez.

Ele evoluirá.

A ordem prevista é aproximadamente a seguinte.

## Primeira etapa

Categoria

Produto

Cliente

Carrinho

ItemCarrinho

---

## Segunda etapa

Pedido

ItemPedido

---

## Terceira etapa

Pagamento

FormaPagamento

---

## Quarta etapa

Cupom

Promoções

Descontos

---

## Quinta etapa

Estoque

Movimentação

Reserva

---

## Sexta etapa

Notificações

Persistência

Testes

Padrões de projeto

---

# Entidades principais

Durante praticamente todo o curso estas serão as entidades centrais do domínio.

Cliente

Categoria

Produto

Carrinho

ItemCarrinho

Pedido

ItemPedido

Pagamento

Cupom

Estoque

Nem todas existirão desde o início.

Elas serão introduzidas gradualmente.

---

# Responsabilidade das entidades

Antes de implementar qualquer classe responder:

"Qual problema do domínio esta entidade resolve?"

Nenhuma entidade deve existir apenas porque "parece necessária".

---

# Cliente

## O que representa

Uma pessoa que realiza compras no sistema.

---

## Responsabilidades

Manter seus próprios dados.

Possuir um carrinho.

Realizar pedidos.

Consultar histórico de compras.

---

## Não é responsabilidade do Cliente

Calcular totais.

Aplicar descontos.

Controlar estoque.

Processar pagamentos.

Emitir notas.

Essas responsabilidades pertencem a outros objetos.

---

## Informações esperadas

Nome

Email

CPF

Telefone

Endereço

Esses atributos poderão evoluir durante o curso.

---

# Categoria

## O que representa

Uma classificação utilizada para organizar produtos.

---

## Responsabilidades

Agrupar produtos.

Organizar catálogo.

Permitir navegação.

---

## Não é responsabilidade

Calcular preços.

Aplicar descontos.

Controlar estoque.

Conhecer clientes.

---

# Produto

## O que representa

Um item comercializado pelo E-Commerce.

---

## Responsabilidades

Conhecer seu próprio nome.

Conhecer seu preço.

Conhecer sua categoria.

Responder perguntas sobre seu estado.

Aplicar regras relacionadas ao próprio produto.

---

## Não é responsabilidade

Calcular total do carrinho.

Controlar pedidos.

Conhecer clientes.

Conhecer pagamentos.

Conhecer cupons.

Conhecer banco de dados.

Conhecer interface gráfica.

---

## Informações esperadas

Nome

Descrição

Preço

Categoria

Situação

Código

Esses atributos poderão aumentar futuramente.

---

# Carrinho

## O que representa

A seleção de produtos que um cliente pretende comprar.

---

## Responsabilidades

Adicionar itens.

Remover itens.

Alterar quantidades.

Calcular valor total.

Listar itens.

Esvaziar carrinho.

---

## Não é responsabilidade

Receber pagamento.

Controlar estoque.

Emitir pedido.

Gerar nota fiscal.

Enviar e-mails.

Persistir informações.

---

# ItemCarrinho

## O que representa

Um produto adicionado ao carrinho.

Não representa o produto em si.

Representa a participação do produto dentro daquele carrinho.

---

## Responsabilidades

Conhecer o produto.

Conhecer a quantidade.

Conhecer o preço praticado naquele momento.

Calcular subtotal.

---

## Informações esperadas

Produto

Quantidade

Preço unitário

Subtotal

---

## Observação importante

Sempre que um relacionamento passar a possuir informações próprias, considerar transformá-lo em uma entidade.

ItemCarrinho é um excelente exemplo desse princípio.

---

# Pedido

## O que representa

A confirmação de uma compra.

---

## Responsabilidades

Registrar a compra.

Conhecer seus itens.

Conhecer seu cliente.

Conhecer seu pagamento.

Possuir um estado.

---

## Estados possíveis

Criado

Aguardando pagamento

Pago

Cancelado

Enviado

Entregue

Essa lista poderá evoluir durante o curso.

---

# ItemPedido

Representa um produto efetivamente comprado.

É semelhante ao ItemCarrinho.

Entretanto possui responsabilidades diferentes.

Ele representa uma compra realizada.

Não uma intenção de compra.

---

# Pagamento

## O que representa

O processo de quitação financeira de um pedido.

---

## Responsabilidades

Conhecer valor.

Conhecer forma de pagamento.

Conhecer situação.

Registrar data.

---

## Não é responsabilidade

Modificar produtos.

Alterar carrinhos.

Controlar estoque.

---

# Cupom

## O que representa

Uma regra promocional.

---

## Responsabilidades

Verificar validade.

Calcular desconto.

Responder se pode ser aplicado.

---

## Não é responsabilidade

Alterar preços dos produtos.

Conhecer pagamentos.

Conhecer estoque.

---

# Estoque

## O que representa

A quantidade disponível de produtos.

---

## Responsabilidades

Registrar quantidade.

Reservar itens.

Liberar reservas.

Atualizar saldo.

---

## Não é responsabilidade

Controlar pedidos.

Calcular descontos.

Conhecer clientes.

---

# Relações entre entidades

Cliente

↓

possui

↓

Carrinho

↓

possui

↓

ItemCarrinho

↓

referencia

↓

Produto

Produto

↓

pertence

↓

Categoria

Pedido

↓

possui

↓

ItemPedido

↓

referencia

↓

Produto

Pedido

↓

possui

↓

Pagamento

Pedido

↓

pode utilizar

↓

Cupom

---

# Linguagem utilizada no código

Sempre utilizar os mesmos nomes.

Cliente

Categoria

Produto

Carrinho

ItemCarrinho

Pedido

ItemPedido

Pagamento

Cupom

FormaPagamento

Estoque

Nunca criar sinônimos para representar o mesmo conceito.

A linguagem do domínio deve permanecer consistente durante todo o curso.

---

# Invariantes do Domínio

As invariantes representam regras que nunca podem ser violadas.

Independentemente da implementação adotada, essas regras devem permanecer verdadeiras.

Sempre que uma nova funcionalidade for criada, verificar se nenhuma invariante está sendo quebrada.

---

## Produto

Um produto:

- sempre possui nome;
- sempre possui preço válido;
- pertence a exatamente uma categoria;
- nunca possui preço negativo;
- nunca conhece clientes;
- nunca conhece pedidos;
- nunca conhece pagamentos.

---

## Categoria

Uma categoria:

- possui um nome;
- pode não possuir produtos;
- não conhece clientes;
- não conhece pedidos.

---

## Cliente

Um cliente:

- pode possuir apenas um carrinho ativo;
- pode possuir diversos pedidos;
- pode nunca ter realizado uma compra;
- não conhece estoque;
- não conhece pagamento.

---

## Carrinho

Um carrinho:

- pertence a apenas um cliente;
- pode estar vazio;
- nunca possui produtos diretamente;
- sempre possui ItemCarrinho;
- calcula seu próprio total.

---

## ItemCarrinho

Um ItemCarrinho:

- referencia exatamente um produto;
- possui quantidade maior que zero;
- conhece o preço praticado naquele momento;
- calcula seu subtotal.

---

## Pedido

Um pedido:

- pertence a um cliente;
- possui pelo menos um ItemPedido;
- possui um estado;
- pode ou não possuir pagamento (dependendo do estado).

---

## ItemPedido

Um ItemPedido:

- referencia um produto;
- preserva o preço utilizado na compra;
- nunca altera seu valor após confirmação do pedido.

---

## Pagamento

Um pagamento:

- pertence a apenas um pedido;
- possui um valor;
- possui um estado.

---

## Cupom

Um cupom:

- possui uma validade;
- possui uma regra de desconto;
- pode tornar-se inválido.

---

# Regras de Negócio

As regras de negócio devem ser introduzidas gradualmente durante o curso.

Jamais apresentar todas simultaneamente.

---

## Produtos

Um produto não pode possuir preço negativo.

Um produto deve possuir nome.

Uma categoria deve existir antes do produto.

---

## Carrinho

Não é permitido adicionar quantidade negativa.

Itens iguais devem ser agrupados.

Remover um item elimina apenas aquele ItemCarrinho.

O carrinho calcula o total.

Jamais o Cliente.

---

## Pedido

Somente um carrinho válido pode gerar um pedido.

Após criado, o pedido preserva os preços praticados.

Alterações futuras no Produto não modificam pedidos antigos.

---

## Pagamento

Um pagamento nunca altera diretamente o Pedido.

Ele informa seu estado.

O Pedido reage a essa informação.

Essa separação será importante futuramente.

---

## Estoque

O estoque representa disponibilidade.

Ele não representa vendas.

São conceitos diferentes.

---

# Responsabilidades

Sempre responder estas perguntas.

Quem possui esta informação?

Quem precisa desta informação?

Quem deve executar esta regra?

Essas perguntas são mais importantes que a implementação.

---

# Distribuição de responsabilidades

Sempre buscar:

Alta coesão.

Baixo acoplamento.

Objetos ricos.

Métodos pequenos.

Pouco conhecimento entre classes.

---

# Objetos ricos

As regras de negócio devem permanecer dentro do domínio.

Evitar classes compostas apenas por atributos.

Evitar objetos anêmicos.

Exemplo inadequado.

Produto

↓

getPreço()

↓

Outra classe calcula tudo.

Exemplo desejado.

Produto participa do cálculo quando isso fizer sentido.

---

# Colaboração

Os objetos colaboram.

Eles não controlam uns aos outros.

Exemplo.

Carrinho pergunta ao ItemCarrinho seu subtotal.

O Carrinho não calcula utilizando diretamente:

preço × quantidade.

Cada objeto faz sua parte.

---

# Dependências

As dependências devem ser mínimas.

Uma classe conhece apenas aquilo que realmente necessita.

Quanto menos objetos uma classe conhecer, melhor.

---

# Relacionamentos permitidos

Cliente

↓

Carrinho

Carrinho

↓

ItemCarrinho

ItemCarrinho

↓

Produto

Produto

↓

Categoria

Pedido

↓

Pagamento

Pedido

↓

ItemPedido

ItemPedido

↓

Produto

---

# Relacionamentos proibidos

Produto

×

Cliente

Produto

×

Carrinho

Categoria

×

Pagamento

Pagamento

×

Estoque

Cliente

×

Cupom

Esses relacionamentos poderão existir apenas se houver forte justificativa durante a evolução do curso.

---

# Lei do Menor Conhecimento

Sempre que possível:

Uma classe conversa apenas com seus colaboradores imediatos.

Evitar cadeias como:

Cliente

↓

Carrinho

↓

Item

↓

Produto

↓

Categoria

↓

...

Esse tipo de navegação excessiva será utilizado para discutir acoplamento.

---

# Estados do domínio

O domínio muda ao longo do tempo.

Essas mudanças devem ser representadas explicitamente.

Exemplo.

Pedido

Criado

↓

Pago

↓

Separação

↓

Enviado

↓

Entregue

↓

Finalizado

Evitar utilizar diversas flags booleanas.

Preferir estados claros.

---

# Eventos importantes

Durante o curso poderão surgir eventos como:

Produto criado.

Produto alterado.

Produto removido.

Carrinho criado.

Produto adicionado ao carrinho.

Produto removido do carrinho.

Pedido criado.

Pedido pago.

Pedido enviado.

Cupom aplicado.

Esses eventos futuramente poderão justificar padrões de projeto.

---

# Fluxo principal do sistema

O fluxo principal do E-Commerce é:

Cliente

↓

consulta produtos

↓

escolhe produtos

↓

adiciona ao carrinho

↓

altera quantidades

↓

confirma compra

↓

gera pedido

↓

realiza pagamento

↓

pedido muda de estado

↓

estoque é atualizado

↓

pedido enviado

↓

pedido entregue

Todo novo conceito deve surgir dentro desse fluxo.

---

# Evolução do domínio

O domínio deve crescer naturalmente.

Nunca antecipar conceitos.

Exemplo.

Primeiras aulas.

Produto.

Categoria.

Carrinho.

Depois.

Pedido.

Mais tarde.

Pagamento.

Somente depois.

Promoções.

Strategy.

Factory.

Repository.

Persistência.

A IA nunca deve introduzir conceitos futuros.

---

# Escopo

Este curso não pretende construir um ERP.

O sistema deve permanecer simples.

Toda funcionalidade deve existir porque ajuda a ensinar um conceito.

Nunca adicionar complexidade apenas para tornar o sistema "mais real".

---

# Fora do escopo

Durante este curso não serão implementados:

Marketplace.

Múltiplos vendedores.

Frete internacional.

Tributação.

Emissão de Nota Fiscal.

Integração bancária.

Controle financeiro empresarial.

Microserviços.

Mensageria distribuída.

Escalabilidade.

Esses assuntos poderão ser mencionados, mas não fazem parte do domínio principal.

---

# Decisões arquiteturais

O domínio deve permanecer independente.

Ele não conhece:

Banco de Dados.

ORM.

Framework Web.

API REST.

Interface gráfica.

Arquivos.

Console.

Esses detalhes aparecerão apenas nas camadas externas quando necessário.

Mesmo nas primeiras aulas, incentivar essa separação.

---

# Objetivo deste documento

Este documento é a fonte da verdade do domínio.

Toda aula deve ser consistente com estas definições.

Caso uma nova necessidade surja, este documento deve ser atualizado antes da implementação.

O domínio evolui primeiro.

O código evolui depois.

Essa disciplina garante consistência durante todo o curso.