from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago


class NotificarClienteDoPagamento:
    """Reage a PedidoPago avisando o cliente pelo canal que ele prefere."""

    def __init__(self, servico_notificacao: ServicoNotificacaoPedido) -> None:
        self._servico_notificacao = servico_notificacao

    def __call__(self, evento: PedidoPago) -> None:
        self._servico_notificacao.pedido_pago(evento.pedido, evento.cliente)


class NotificarClienteDoEnvio:
    """Reage a PedidoDespachado avisando o cliente com o codigo de rastreio."""

    def __init__(self, servico_notificacao: ServicoNotificacaoPedido) -> None:
        self._servico_notificacao = servico_notificacao

    def __call__(self, evento: PedidoDespachado) -> None:
        self._servico_notificacao.pedido_enviado(evento.pedido, evento.cliente)
