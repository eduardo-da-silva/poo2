from ecommerce.criador_notificacao import CriadorNotificacao


class ServicoNotificacaoPedido:

    def __init__(self, criador_notificacao: CriadorNotificacao) -> None:
        self._criador_notificacao = criador_notificacao

    def pedido_pago(self, pedido: "Pedido", cliente: "Cliente") -> None:
        mensagem = (
            f"Ola, {cliente.nome}. O pagamento do seu pedido foi confirmado. "
            f"Total: R$ {pedido.calcular_total():.2f}."
        )
        self._notificar(cliente, mensagem)

    def pedido_enviado(self, pedido: "Pedido", cliente: "Cliente") -> None:
        rastreio = pedido.entrega.codigo_rastreio if pedido.entrega is not None else "-"
        mensagem = (
            f"Ola, {cliente.nome}. Seu pedido foi enviado. "
            f"Codigo de rastreio: {rastreio}."
        )
        self._notificar(cliente, mensagem)

    def _notificar(self, cliente: "Cliente", mensagem: str) -> None:
        notificacao = self._criador_notificacao.criar(cliente.canal_preferido)
        notificacao.enviar(cliente.contato, mensagem)


if __name__ == "__main__":
    from ecommerce.carrinho import Carrinho
    from ecommerce.categoria import Categoria
    from ecommerce.cliente import Cliente
    from ecommerce.criador_pagamento import CriadorPagamento
    from ecommerce.expedidor import ExpedidorLojaCentral
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)
    pedido = maria.finalizar_compra()

    servico = ServicoNotificacaoPedido(CriadorNotificacao())

    pedido.confirmar_pagamento(CriadorPagamento())
    servico.pedido_pago(pedido, maria)

    ExpedidorLojaCentral().despachar(pedido)
    servico.pedido_enviado(pedido, maria)
