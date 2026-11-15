from ecommerce.aplicacao.observador_de_pagamento import ObservadorDePagamento
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.pedido import Pedido


class NotificarClienteDoPagamento(ObservadorDePagamento):
    """Avisa o cliente, pelo canal que ele prefere, que o pagamento foi confirmado."""

    def __init__(self, servico_notificacao: ServicoNotificacaoPedido) -> None:
        self._servico_notificacao = servico_notificacao

    def atualizar(self, pedido: Pedido, cliente: Cliente) -> None:
        self._servico_notificacao.pedido_pago(pedido, cliente)
