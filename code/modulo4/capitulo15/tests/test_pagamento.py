from datetime import date, timedelta

import pytest
from ecommerce.categoria import Categoria
from ecommerce.pagamento import (
    Pagamento,
    PagamentoBoleto,
    PagamentoCartao,
    PagamentoPix,
)
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
from ecommerce.situacao_pagamento import SituacaoPagamento


class TestPagamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.pedido = Pedido()
        self.pedido.adicionar_item(self.notebook, 1)

    def test_pagamento_e_abstrato(self) -> None:
        with pytest.raises(TypeError):
            Pagamento(self.pedido, 3500.0)  # type: ignore[abstract]

    def test_pix_confirma_na_hora(self) -> None:
        pag = PagamentoPix(self.pedido, 3500.0, chave="loja@ecommerce.com")
        assert pag.situacao == SituacaoPagamento.PENDENTE
        pag.confirmar()
        assert pag.situacao == SituacaoPagamento.CONFIRMADO
        assert pag.confirmado is True

    def test_confirmar_pagamento_ja_confirmado(self) -> None:
        pag = PagamentoPix(self.pedido, 3500.0, chave="loja@ecommerce.com")
        pag.confirmar()
        with pytest.raises(ValueError):
            pag.confirmar()

    def test_valor_invalido_zero(self) -> None:
        with pytest.raises(ValueError):
            PagamentoPix(self.pedido, 0, chave="loja@ecommerce.com")

    def test_valor_invalido_negativo(self) -> None:
        with pytest.raises(ValueError):
            PagamentoPix(self.pedido, -100, chave="loja@ecommerce.com")

    def test_data_e_hoje(self) -> None:
        pag = PagamentoPix(self.pedido, 3500.0, chave="loja@ecommerce.com")
        assert pag.data == date.today()

    def test_boleto_no_prazo_confirma(self) -> None:
        pag = PagamentoBoleto(
            self.pedido, 3500.0, linha_digitavel="123", vencimento=date.today() + timedelta(days=3)
        )
        pag.confirmar()
        assert pag.situacao == SituacaoPagamento.CONFIRMADO

    def test_boleto_vencido_e_recusado(self) -> None:
        pag = PagamentoBoleto(
            self.pedido, 3500.0, linha_digitavel="123", vencimento=date.today() - timedelta(days=1)
        )
        pag.confirmar()
        assert pag.situacao == SituacaoPagamento.RECUSADO
        assert pag.confirmado is False

    def test_cartao_calcula_valor_da_parcela(self) -> None:
        pag = PagamentoCartao(self.pedido, 3600.0, bandeira="VISA", parcelas=3)
        assert pag.valor_parcela() == 1200.0

    def test_cartao_parcelas_invalidas(self) -> None:
        with pytest.raises(ValueError):
            PagamentoCartao(self.pedido, 3600.0, bandeira="VISA", parcelas=0)
