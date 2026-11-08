import pytest
from ecommerce.categoria import Categoria
from ecommerce.item_pedido import ItemPedido
from ecommerce.produto import Produto


class TestItemPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)

    def test_criar_item_pedido(self) -> None:
        item = ItemPedido(self.notebook, 2, self.notebook.preco)
        assert item.produto == self.notebook
        assert item.quantidade == 2
        assert item.preco_no_momento == 3500.0

    def test_calcular_subtotal(self) -> None:
        item = ItemPedido(self.notebook, 3, self.notebook.preco)
        assert item.calcular_subtotal() == 10500.0

    def test_quantidade_invalida(self) -> None:
        with pytest.raises(ValueError):
            ItemPedido(self.notebook, 0, self.notebook.preco)

    def test_quantidade_negativa(self) -> None:
        with pytest.raises(ValueError):
            ItemPedido(self.notebook, -1, self.notebook.preco)

    def test_preco_invalido(self) -> None:
        with pytest.raises(ValueError):
            ItemPedido(self.notebook, 1, -10.0)

    def test_preco_zero(self) -> None:
        with pytest.raises(ValueError):
            ItemPedido(self.notebook, 1, 0.0)

    def test_preco_congelado_no_momento(self) -> None:
        item = ItemPedido(self.notebook, 1, self.notebook.preco)
        self.notebook.alterar_preco(4000.0)
        assert item.preco_no_momento == 3500.0

    def test_item_pedido_sem_setter(self) -> None:
        item = ItemPedido(self.notebook, 2, self.notebook.preco)
        with pytest.raises(AttributeError):
            item.quantidade = 5  # type: ignore
