from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.entrega import Entrega
from ecommerce.expedidor import Expedidor
from ecommerce.forma_pagamento import FormaPagamento
from ecommerce.servico_notificacao_pedido import ServicoNotificacaoPedido


class ServicoPedido:
    """Coordena o ciclo de vida de um pedido usando colaboradores injetados."""

    def __init__(
        self,
        criador_pagamento: CriadorPagamento,
        expedidor: Expedidor,
        servico_notificacao: ServicoNotificacaoPedido,
    ) -> None:
        self._criador_pagamento = criador_pagamento
        self._expedidor = expedidor
        self._servico_notificacao = servico_notificacao

    def pagar(
        self,
        pedido: "Pedido",
        cliente: "Cliente",
        forma: FormaPagamento = FormaPagamento.PIX,
        **dados: object,
    ) -> None:
        pedido.confirmar_pagamento(self._criador_pagamento, forma, **dados)
        self._servico_notificacao.pedido_pago(pedido, cliente)

    def despachar(self, pedido: "Pedido", cliente: "Cliente") -> Entrega:
        entrega = self._expedidor.despachar(pedido)
        self._servico_notificacao.pedido_enviado(pedido, cliente)
        return entrega


if __name__ == "__main__":
    from ecommerce.carrinho import Carrinho
    from ecommerce.categoria import Categoria
    from ecommerce.cliente import Cliente
    from ecommerce.criador_notificacao import CriadorNotificacao
    from ecommerce.expedidor import ExpedidorLojaCentral
    from ecommerce.produto import Produto

    # Raiz de composicao: um unico lugar monta o grafo de objetos.
    servico_pedido = ServicoPedido(
        criador_pagamento=CriadorPagamento(),
        expedidor=ExpedidorLojaCentral(),
        servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacao()),
    )

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)
    pedido = maria.finalizar_compra()

    servico_pedido.pagar(pedido, maria)
    servico_pedido.despachar(pedido, maria)
    pedido.entregar()
    print(f"Status final: {pedido.status}")
