from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.entrega import Entrega
from ecommerce.expedidor import Expedidor
from ecommerce.forma_pagamento import FormaPagamento
from ecommerce.repositorio_pedido import RepositorioPedido
from ecommerce.servico_notificacao_pedido import ServicoNotificacaoPedido


class ServicoPedido:
    """Coordena o ciclo de vida de um pedido usando colaboradores injetados."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        criador_pagamento: CriadorPagamento,
        expedidor: Expedidor,
        servico_notificacao: ServicoNotificacaoPedido,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._criador_pagamento = criador_pagamento
        self._expedidor = expedidor
        self._servico_notificacao = servico_notificacao

    def finalizar_compra(self, cliente: "Cliente") -> "Pedido":
        pedido = cliente.finalizar_compra()
        self._repositorio_pedido.adicionar(pedido)
        return pedido

    def pagar(
        self,
        pedido_id: int,
        cliente: "Cliente",
        forma: FormaPagamento = FormaPagamento.PIX,
        **dados: object,
    ) -> None:
        pedido = self._repositorio_pedido.obter(pedido_id)
        pedido.confirmar_pagamento(self._criador_pagamento, forma, **dados)
        self._repositorio_pedido.atualizar(pedido)
        self._servico_notificacao.pedido_pago(pedido, cliente)

    def despachar(self, pedido_id: int, cliente: "Cliente") -> Entrega:
        pedido = self._repositorio_pedido.obter(pedido_id)
        entrega = self._expedidor.despachar(pedido)
        self._repositorio_pedido.atualizar(pedido)
        self._servico_notificacao.pedido_enviado(pedido, cliente)
        return entrega


if __name__ == "__main__":
    from ecommerce.carrinho import Carrinho
    from ecommerce.categoria import Categoria
    from ecommerce.cliente import Cliente
    from ecommerce.criador_notificacao import CriadorNotificacao
    from ecommerce.expedidor import ExpedidorLojaCentral
    from ecommerce.produto import Produto
    from ecommerce.repositorio_pedido_memoria import RepositorioPedidoMemoria
    from ecommerce.repositorio_produto_memoria import RepositorioProdutoMemoria

    # Raiz de composicao: um unico lugar monta o grafo de objetos.
    repositorio_produto = RepositorioProdutoMemoria()
    repositorio_pedido = RepositorioPedidoMemoria()
    servico_pedido = ServicoPedido(
        repositorio_pedido=repositorio_pedido,
        criador_pagamento=CriadorPagamento(),
        expedidor=ExpedidorLojaCentral(),
        servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacao()),
    )

    notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    repositorio_produto.adicionar(notebook)

    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(repositorio_produto.obter(1), 1)

    pedido = servico_pedido.finalizar_compra(maria)
    servico_pedido.pagar(pedido.id, maria)
    servico_pedido.despachar(pedido.id, maria)
    print(f"Status guardado: {repositorio_pedido.obter(pedido.id).status}")
