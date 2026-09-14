class Cliente:

    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email
        self.carrinho: "Carrinho | None" = None
        self._pedidos: list["Pedido"] = []

    @property
    def pedidos(self) -> list["Pedido"]:
        return list(self._pedidos)

    def possui_carrinho(self) -> bool:
        return self.carrinho is not None

    def adicionar_pedido(self, pedido: "Pedido") -> None:
        self._pedidos.append(pedido)

    def finalizar_compra(self) -> "Pedido":
        if self.carrinho is None:
            raise ValueError("Cliente nao possui carrinho")
        if not self.carrinho.itens:
            raise ValueError("Carrinho vazio")
        pedido = self.carrinho.finalizar()
        self._pedidos.append(pedido)
        self.carrinho.esvaziar()
        return pedido


if __name__ == "__main__":
    from ecommerce.carrinho import Carrinho
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    mouse = Produto("Mouse", 150.0, 20, cat)

    c = Cliente("Maria", "maria@email.com")
    c.carrinho = Carrinho()
    c.carrinho.adicionar_item(notebook, 1)
    c.carrinho.adicionar_item(mouse, 2)

    pedido = c.finalizar_compra()
    print(f"Pedido criado: {pedido.quantidade_itens()} itens, R$ {pedido.calcular_total():.2f}")
    print(f"Pedidos do cliente: {len(c.pedidos)}")
    print(f"Carrinho vazio: {c.carrinho.quantidade_itens()}")
