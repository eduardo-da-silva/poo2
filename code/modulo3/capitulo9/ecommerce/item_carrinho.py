class ItemCarrinho:

    def __init__(self, produto: "Produto", quantidade: int) -> None:
        self.produto = produto
        self.quantidade = quantidade
        self.preco_no_momento = produto.preco

    def calcular_subtotal(self) -> float:
        return self.preco_no_momento * self.quantidade


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    item = ItemCarrinho(notebook, 2)
    print(f"Subtotal: R$ {item.calcular_subtotal():.2f}")
