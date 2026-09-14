from datetime import date, timedelta

import pytest
from ecommerce.categoria import Categoria
from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.forma_pagamento import FormaPagamento
from ecommerce.pagamento import PagamentoBoleto, PagamentoCartao, PagamentoPix
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestCriadorPagamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.pedido = Pedido()
        self.pedido.adicionar_item(self.notebook, 1)
        self.criador = CriadorPagamento()

    def test_cria_pagamento_pix(self) -> None:
        pagamento = self.criador.criar(FormaPagamento.PIX, self.pedido, 3500.0)
        assert isinstance(pagamento, PagamentoPix)
        assert pagamento.valor == 3500.0

    def test_cria_pagamento_boleto(self) -> None:
        pagamento = self.criador.criar(
            FormaPagamento.BOLETO,
            self.pedido,
            3500.0,
            vencimento=date.today() + timedelta(days=5),
        )
        assert isinstance(pagamento, PagamentoBoleto)

    def test_cria_pagamento_cartao_com_parcelas(self) -> None:
        pagamento = self.criador.criar(
            FormaPagamento.CARTAO_CREDITO, self.pedido, 3600.0, parcelas=3
        )
        assert isinstance(pagamento, PagamentoCartao)
        assert pagamento.parcelas == 3

    def test_forma_desconhecida_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            self.criador.criar("pix", self.pedido, 3500.0)  # type: ignore[arg-type]
