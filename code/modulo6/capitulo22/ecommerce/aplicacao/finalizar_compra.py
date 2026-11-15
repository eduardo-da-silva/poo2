from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class FinalizarCompra:
    """Caso de uso: transformar o carrinho do cliente em um pedido guardado."""

    def __init__(self, repositorio_pedido: RepositorioPedido) -> None:
        self._repositorio_pedido = repositorio_pedido

    def executar(self, cliente: Cliente) -> Pedido:
        pedido = cliente.finalizar_compra()
        self._repositorio_pedido.adicionar(pedido)
        return pedido
