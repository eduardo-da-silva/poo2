import pytest
from ecommerce.categoria import Categoria
from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.entrega import EntregaCorreios, EntregaTransportadora
from ecommerce.expedidor import ExpedidorCentroRegional, ExpedidorLojaCentral
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestExpedidor:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.criador = CriadorPagamento()

    def _pedido_pago(self) -> Pedido:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento(self.criador)
        return pedido

    def test_loja_central_despacha_pelos_correios(self) -> None:
        pedido = self._pedido_pago()
        entrega = ExpedidorLojaCentral().despachar(pedido)
        assert isinstance(entrega, EntregaCorreios)
        assert entrega.modalidade == "SEDEX"

    def test_centro_regional_despacha_por_transportadora(self) -> None:
        pedido = self._pedido_pago()
        entrega = ExpedidorCentroRegional().despachar(pedido)
        assert isinstance(entrega, EntregaTransportadora)

    def test_despachar_registra_entrega_e_muda_o_estado(self) -> None:
        pedido = self._pedido_pago()
        entrega = ExpedidorLojaCentral().despachar(pedido)
        assert pedido.entrega is entrega
        assert pedido.status == "enviado"

    def test_codigo_de_rastreio_tem_o_prefixo_do_meio(self) -> None:
        pedido = self._pedido_pago()
        entrega = ExpedidorLojaCentral().despachar(pedido)
        assert entrega.codigo_rastreio.startswith("BR")

    def test_nao_despacha_pedido_nao_pago(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        with pytest.raises(ValueError):
            ExpedidorLojaCentral().despachar(pedido)
