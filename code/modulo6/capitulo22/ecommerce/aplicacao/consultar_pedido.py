from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class ConsultarPedido:
    """Caso de uso de consulta: em que pe esta um pedido."""

    def __init__(self, repositorio_pedido: RepositorioPedido) -> None:
        self._repositorio_pedido = repositorio_pedido

    def executar(self, pedido_id: int) -> Pedido:
        return self._repositorio_pedido.obter(pedido_id)
