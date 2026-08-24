from datetime import date, timedelta

import pytest
from ecommerce.categoria import Categoria
from ecommerce.cupom import Cupom
from ecommerce.estrategia_desconto import DescontoPercentual, SemDesconto
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto


class TestPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.mouse = Produto("Mouse", 150.0, 20, self.cat)

    def test_criar_pedido_vazio(self) -> None:
        pedido = Pedido()
        assert pedido.quantidade_itens() == 0
        assert pedido.calcular_total() == 0.0
        assert pedido.status == "criado"

    def test_adicionar_item(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        assert pedido.quantidade_itens() == 1

    def test_calcular_total(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 2)
        pedido.adicionar_item(self.mouse, 3)
        total_esperado = (2 * 3500.0) + (3 * 150.0)
        assert pedido.calcular_total() == total_esperado

    def test_status_inicial(self) -> None:
        pedido = Pedido()
        assert pedido.status == "criado"

    def test_confirmar_pagamento(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        assert pedido.status == "pago"
        assert pedido.pagamento is not None
        assert pedido.pagamento.confirmado is True
        assert pedido.pagamento.valor == 3500.0

    def test_enviar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        pedido.enviar()
        assert pedido.status == "enviado"

    def test_entregar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        pedido.enviar()
        pedido.entregar()
        assert pedido.status == "entregue"

    def test_cancelar_pedido_criado(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.cancelar()
        assert pedido.status == "cancelado"

    def test_nao_cancelar_pedido_entregue(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        pedido.enviar()
        pedido.entregar()
        with pytest.raises(ValueError):
            pedido.cancelar()

    def test_nao_cancelar_pedido_enviado(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        pedido.enviar()
        with pytest.raises(ValueError):
            pedido.cancelar()

    def test_transicao_invalida_lanca_erro(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        with pytest.raises(ValueError):
            pedido.enviar()

    def test_nao_adicionar_apos_pagar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        with pytest.raises(ValueError):
            pedido.adicionar_item(self.mouse, 1)

    def test_confirmar_pagamento_sem_itens(self) -> None:
        pedido = Pedido()
        with pytest.raises(ValueError):
            pedido.confirmar_pagamento()

    def test_calcular_total_sem_estrategia(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        assert pedido.calcular_total() == 3500.0

    def test_calcular_total_com_estrategia_sem_desconto(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        assert pedido.calcular_total(SemDesconto()) == 3500.0

    def test_calcular_total_com_desconto_percentual(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        assert pedido.calcular_total(DescontoPercentual(15)) == 3500.0 * 0.85

    def test_aplicar_cupom_valido(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        cupom = Cupom("BEMVINDO10", date.today() + timedelta(days=1), DescontoPercentual(10))
        pedido.aplicar_cupom(cupom)
        assert pedido.cupom is cupom
        assert pedido.calcular_total() == 3500.0 * 0.90

    def test_aplicar_cupom_expirado_lanca_erro(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        cupom = Cupom("PROMOANTIGA", date.today() - timedelta(days=1), DescontoPercentual(10))
        with pytest.raises(ValueError):
            pedido.aplicar_cupom(cupom)

    def test_pagamento_reflete_desconto_do_cupom(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        cupom = Cupom("BEMVINDO10", date.today() + timedelta(days=1), DescontoPercentual(10))
        pedido.aplicar_cupom(cupom)
        pedido.confirmar_pagamento()
        assert pedido.pagamento.valor == 3500.0 * 0.90
