from ecommerce.categoria import Categoria
from ecommerce.produto import Produto
from ecommerce.item_carrinho import ItemCarrinho


class TestItemCarrinho:

    def setup_method(self) -> None:
        cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, cat)

    def test_cria_item_com_produto_e_quantidade(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.produto is self.notebook
        assert item.quantidade == 2

    def test_preco_no_momento_igual_preco_do_produto(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.preco_no_momento == 3500.0

    def test_preco_no_momento_congela_preco_da_criacao(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        self.notebook.alterar_preco(4000.0)
        assert item.preco_no_momento == 3500.0

    def test_calcular_subtotal(self) -> None:
        item = ItemCarrinho(self.notebook, 2)
        assert item.calcular_subtotal() == 7000.0

    def test_subtotal_com_quantidade_um(self) -> None:
        item = ItemCarrinho(self.notebook, 1)
        assert item.calcular_subtotal() == 3500.0
