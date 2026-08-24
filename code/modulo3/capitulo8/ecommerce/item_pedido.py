class ItemPedido:

    def __init__(self, produto: "Produto", quantidade: int, preco_no_momento: float) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if preco_no_momento <= 0:
            raise ValueError("Preco deve ser positivo")
        self._produto = produto
        self._quantidade = quantidade
        self._preco_no_momento = preco_no_momento

    @property
    def produto(self) -> "Produto":
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def preco_no_momento(self) -> float:
        return self._preco_no_momento

    def calcular_subtotal(self) -> float:
        return self._preco_no_momento * self._quantidade


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    item = ItemPedido(notebook, 2, notebook.preco)
    print(f"Subtotal: R$ {item.calcular_subtotal():.2f}")
