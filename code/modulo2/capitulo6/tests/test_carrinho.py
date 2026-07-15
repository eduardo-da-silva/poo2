import pytest
from ecommerce.carrinho import Carrinho
from ecommerce.categoria import Categoria
from ecommerce.produto import Produto


class TestCarrinho:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_carrinho_inicia_vazio(self) -> None:
        carrinho = Carrinho()
        assert carrinho.quantidade_itens() == 0
        assert carrinho.calcular_total() == 0.0

    def test_adicionar_item(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 2)
        assert carrinho.quantidade_itens() == 1

    def test_calcular_total_com_itens(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 2)
        carrinho.adicionar_item(self.mouse, 3)
        total_esperado = (2 * 3500.0) + (3 * 150.0)
        assert carrinho.calcular_total() == total_esperado

    def test_remover_item(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        carrinho.remover_item(self.notebook)
        assert carrinho.quantidade_itens() == 1

    def test_adicionar_quantidade_invalida(self) -> None:
        carrinho = Carrinho()
        with pytest.raises(ValueError):
            carrinho.adicionar_item(self.notebook, 0)

    def test_finalizar_cria_pedido(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        pedido = carrinho.finalizar()
        assert pedido.quantidade_itens() == 2
        assert pedido.calcular_total() == 3500.0 + 2 * 150.0
        assert pedido.status == "criado"

    def test_finalizar_carrinho_vazio(self) -> None:
        carrinho = Carrinho()
        with pytest.raises(ValueError):
            carrinho.finalizar()
