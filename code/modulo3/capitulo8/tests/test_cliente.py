import pytest
from ecommerce.carrinho import Carrinho
from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.produto import Produto


class TestCliente:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_criar_cliente(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.nome == "João"
        assert c.email == "joao@email.com"

    def test_cliente_sem_carrinho(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.possui_carrinho() is False

    def test_cliente_inicia_sem_pedidos(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.pedidos == []

    def test_finalizar_compra(self) -> None:
        c = Cliente("Maria", "maria@email.com")
        c.carrinho = Carrinho()
        c.carrinho.adicionar_item(self.notebook, 1)
        c.carrinho.adicionar_item(self.mouse, 2)

        pedido = c.finalizar_compra()

        assert pedido.quantidade_itens() == 2
        assert pedido.status == "criado"
        assert len(c.pedidos) == 1
        assert c.pedidos[0] == pedido
        assert c.carrinho.quantidade_itens() == 0

    def test_finalizar_compra_sem_carrinho(self) -> None:
        c = Cliente("João", "joao@email.com")
        with pytest.raises(ValueError):
            c.finalizar_compra()

    def test_finalizar_compra_carrinho_vazio(self) -> None:
        c = Cliente("Maria", "maria@email.com")
        c.carrinho = Carrinho()
        with pytest.raises(ValueError):
            c.finalizar_compra()
