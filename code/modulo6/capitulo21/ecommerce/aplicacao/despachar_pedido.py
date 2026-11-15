from ecommerce.aplicacao.barramento_eventos import BarramentoEventos
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.entrega import Entrega
from ecommerce.dominio.eventos import PedidoDespachado
from ecommerce.dominio.expedidor import Expedidor
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class DespacharPedido:
    """Caso de uso: enviar um pedido pago e anunciar que ele saiu."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        expedidor: Expedidor,
        barramento: BarramentoEventos,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._expedidor = expedidor
        self._barramento = barramento

    def executar(self, pedido_id: int, cliente: Cliente) -> Entrega:
        pedido = self._repositorio_pedido.obter(pedido_id)
        entrega = self._expedidor.despachar(pedido)
        self._repositorio_pedido.atualizar(pedido)
        self._barramento.publicar(PedidoDespachado(pedido, cliente, entrega))
        return entrega
