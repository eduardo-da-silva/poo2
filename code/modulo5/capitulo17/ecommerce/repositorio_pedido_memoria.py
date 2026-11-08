from ecommerce.pedido import Pedido
from ecommerce.repositorio_pedido import PedidoNaoEncontradoError, RepositorioPedido


class RepositorioPedidoMemoria(RepositorioPedido):

    def __init__(self) -> None:
        self._pedidos: dict[int, Pedido] = {}
        self._proximo_id = 1

    def adicionar(self, pedido: Pedido) -> None:
        pedido.atribuir_id(self._proximo_id)
        self._pedidos[self._proximo_id] = pedido
        self._proximo_id += 1

    def obter(self, id: int) -> Pedido:
        if id not in self._pedidos:
            raise PedidoNaoEncontradoError(f"Pedido {id} nao encontrado")
        return self._pedidos[id]

    def listar(self) -> list[Pedido]:
        return list(self._pedidos.values())

    def atualizar(self, pedido: Pedido) -> None:
        if pedido.id is None or pedido.id not in self._pedidos:
            raise PedidoNaoEncontradoError("Pedido nunca foi adicionado")
        self._pedidos[pedido.id] = pedido


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    repositorio = RepositorioPedidoMemoria()
    pedido = Pedido()
    pedido.adicionar_item(Produto("Mouse", 150.0, 20, Categoria("Informática")), 2)
    repositorio.adicionar(pedido)
    print(f"Pedido {pedido.id}: R$ {repositorio.obter(pedido.id).calcular_total():.2f}")
