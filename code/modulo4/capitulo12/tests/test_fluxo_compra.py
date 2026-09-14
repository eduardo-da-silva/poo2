from ecommerce.carrinho import Carrinho
from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.produto import Produto


class TestFluxoCompra:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_fluxo_completo(self) -> None:
        maria = Cliente("Maria", "maria@email.com")
        maria.carrinho = Carrinho()
        maria.carrinho.adicionar_item(self.notebook, 1)
        maria.carrinho.adicionar_item(self.mouse, 2)

        pedido = maria.finalizar_compra()

        assert pedido.quantidade_itens() == 2
        assert pedido.calcular_total() == 3800.0
        assert pedido.status == "criado"
        assert len(maria.pedidos) == 1
        assert maria.carrinho.quantidade_itens() == 0

        pedido.confirmar_pagamento()
        assert pedido.status == "pago"

        pedido.enviar()
        assert pedido.status == "enviado"

        pedido.entregar()
        assert pedido.status == "entregue"

    def test_cliente_com_multiplos_pedidos(self) -> None:
        maria = Cliente("Maria", "maria@email.com")

        maria.carrinho = Carrinho()
        maria.carrinho.adicionar_item(self.notebook, 1)
        pedido1 = maria.finalizar_compra()

        maria.carrinho = Carrinho()
        maria.carrinho.adicionar_item(self.mouse, 3)
        pedido2 = maria.finalizar_compra()

        assert len(maria.pedidos) == 2
        assert maria.pedidos[0] == pedido1
        assert maria.pedidos[1] == pedido2
