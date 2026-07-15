import pytest
from ecommerce.categoria import Categoria
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_criar_pedido_vazio(self) -> None:
        pedido = Pedido()
        assert pedido.quantidade_itens() == 0
        assert pedido.calcular_total() == 0.0
        assert pedido.status == "criado"

    def test_adicionar_item(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        assert pedido.quantidade_itens() == 1

    def test_calcular_total(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        pedido.adicionar_item(self.mouse, 3)
        total_esperado = (2 * 3500.0) + (3 * 150.0)
        assert pedido.calcular_total() == total_esperado

    def test_itens_retorna_copia(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        itens = pedido.itens
        with pytest.raises(AttributeError):
            itens.append = None  # should not interfere

    def test_nao_adicionar_apos_finalizado(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido._status = "pago"
        with pytest.raises(ValueError):
            pedido.adicionar_item(self.mouse, 1)
