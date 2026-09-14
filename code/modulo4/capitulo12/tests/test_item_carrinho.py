from ecommerce.categoria import Categoria
from ecommerce.item_carrinho import ItemCarrinho
from ecommerce.produto import Produto


class TestItemCarrinho:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)

    def test_criar_item_carrinho(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.produto == self.notebook
        assert item.quantidade == 2
        assert item.preco_no_momento == 3500.0

    def test_calcular_subtotal(self) -> None:
        item = ItemCarrinho(self.notebook, 3)
        assert item.calcular_subtotal() == 10500.0

    def test_preco_congelado_no_momento(self) -> None:
        item = ItemCarrinho(self.notebook, 1)
        self.notebook.alterar_preco(4000.0)
        assert item.preco_no_momento == 3500.0
