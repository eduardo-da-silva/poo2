from ecommerce.categoria import Categoria
from ecommerce.produto import Produto
from ecommerce.carrinho import Carrinho


class TestCarrinho:

    def setup_method(self) -> None:
        cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, cat)
        self.mouse = Produto("Mouse", 150.0, 20, cat)

    def test_carrinho_vazio(self) -> None:
        carrinho = Carrinho()
        assert carrinho.quantidade_itens() == 0

    def test_adicionar_item_ao_carrinho(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        assert carrinho.quantidade_itens() == 1

    def test_adicionar_multiplos_itens(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        assert carrinho.quantidade_itens() == 2

    def test_remover_item_do_carrinho(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 2)
        carrinho.remover_item(self.notebook)
        assert carrinho.quantidade_itens() == 1

    def test_calcular_total_com_um_item(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 2)
        assert carrinho.calcular_total() == 7000.0

    def test_calcular_total_com_varios_itens(self) -> None:
        carrinho = Carrinho()
        carrinho.adicionar_item(self.notebook, 1)
        carrinho.adicionar_item(self.mouse, 3)
        assert carrinho.calcular_total() == 3950.0

    def test_calcular_total_carrinho_vazio(self) -> None:
        carrinho = Carrinho()
        assert carrinho.calcular_total() == 0.0

    def test_adicionar_quantidade_invalida(self) -> None:
        carrinho = Carrinho()
        try:
            carrinho.adicionar_item(self.notebook, 0)
            assert False, "Deveria ter lançado exceção"
        except ValueError:
            pass
