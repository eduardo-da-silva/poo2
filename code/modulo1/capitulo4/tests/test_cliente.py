from ecommerce.cliente import Cliente


class TestCliente:

    def test_cria_cliente_com_nome_e_email(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.nome == "João"
        assert c.email == "joao@email.com"

    def test_cliente_sem_carrinho(self) -> None:
        c = Cliente("João", "joao@email.com")
        assert c.possui_carrinho() is False
