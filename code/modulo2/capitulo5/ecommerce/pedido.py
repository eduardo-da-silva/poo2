from ecommerce.item_pedido import ItemPedido


class Pedido:

    def __init__(self) -> None:
        self._itens: list[ItemPedido] = []
        self._status = "criado"

    @property
    def itens(self) -> list[ItemPedido]:
        return list(self._itens)

    @property
    def status(self) -> str:
        return self._status

    def adicionar_item(self, produto: "Produto", quantidade: int) -> None:
        if self._status != "criado":
            raise ValueError("Não é possível adicionar itens a um pedido já finalizado")
        preco_no_momento = produto.preco
        self._itens.append(ItemPedido(produto, quantidade, preco_no_momento))

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self._itens)

    def quantidade_itens(self) -> int:
        return len(self._itens)


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    mouse = Produto("Mouse", 150.0, 20, cat)

    pedido = Pedido()
    pedido.adicionar_item(notebook, 1)
    pedido.adicionar_item(mouse, 2)

    print(f"Itens no pedido: {pedido.quantidade_itens()}")
    print(f"Total: R$ {pedido.calcular_total():.2f}")
    print(f"Status: {pedido.status}")
