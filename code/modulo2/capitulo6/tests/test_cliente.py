from ecommerce.cliente import Cliente


class TestCliente:

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
