import pytest
from ecommerce.categoria import Categoria
from ecommerce.pagamento import Pagamento
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestPagamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.pedido = Pedido()
        self.pedido.adicionar_item(self.notebook, 1)

    def test_criar_pagamento(self) -> None:
        pag = Pagamento(self.pedido, 3500.0)
        assert pag.pedido == self.pedido
        assert pag.valor == 3500.0
        assert pag.confirmado is False

    def test_confirmar_pagamento(self) -> None:
        pag = Pagamento(self.pedido, 3500.0)
        pag.confirmar()
        assert pag.confirmado is True

    def test_confirmar_pagamento_ja_confirmado(self) -> None:
        pag = Pagamento(self.pedido, 3500.0)
        pag.confirmar()
        with pytest.raises(ValueError):
            pag.confirmar()

    def test_valor_invalido_zero(self) -> None:
        with pytest.raises(ValueError):
            Pagamento(self.pedido, 0)

    def test_valor_invalido_negativo(self) -> None:
        with pytest.raises(ValueError):
            Pagamento(self.pedido, -100)

    def test_data_e_hoje(self) -> None:
        from datetime import date
        pag = Pagamento(self.pedido, 3500.0)
        assert pag.data == date.today()
