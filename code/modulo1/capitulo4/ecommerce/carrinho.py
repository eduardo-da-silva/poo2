from ecommerce.item_carrinho import ItemCarrinho


class Carrinho:

    def __init__(self) -> None:
        self.itens: list[ItemCarrinho] = []

    def adicionar_item(self, produto: "Produto", quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover_item(self, produto: "Produto") -> None:
        self.itens = [i for i in self.itens if i.produto is not produto]

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self.itens)

    def quantidade_itens(self) -> int:
        return len(self.itens)


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    mouse = Produto("Mouse", 150.0, 20, cat)

    carrinho = Carrinho()
    carrinho.adicionar_item(notebook, 1)
    carrinho.adicionar_item(mouse, 2)

    print(f"Itens no carrinho: {carrinho.quantidade_itens()}")
    print(f"Total: R$ {carrinho.calcular_total():.2f}")
