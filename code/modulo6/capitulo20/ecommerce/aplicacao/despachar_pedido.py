from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.entrega import Entrega
from ecommerce.dominio.expedidor import Expedidor
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class DespacharPedido:
    """Caso de uso: enviar um pedido pago e avisar o cliente."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        expedidor: Expedidor,
        servico_notificacao: ServicoNotificacaoPedido,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._expedidor = expedidor
        self._servico_notificacao = servico_notificacao

    def executar(self, pedido_id: int, cliente: Cliente) -> Entrega:
        pedido = self._repositorio_pedido.obter(pedido_id)
        entrega = self._expedidor.despachar(pedido)
        self._repositorio_pedido.atualizar(pedido)
        self._servico_notificacao.pedido_enviado(pedido, cliente)
        return entrega
