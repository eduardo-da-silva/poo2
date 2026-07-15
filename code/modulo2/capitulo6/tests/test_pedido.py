import pytest
from ecommerce.categoria import Categoria
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

    def test_pagar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.pagar()
        assert pedido.status == "pago"
        assert pedido.pagamento is not None

    def test_enviar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.pagar()
        pedido.enviar()
        assert pedido.status == "enviado"

    def test_entregar(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.pagar()
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
        pedido.pagar()
        pedido.enviar()
        pedido.entregar()
        with pytest.raises(ValueError):
            pedido.cancelar()

    def test_nao_cancelar_pedido_enviado(self) -> None:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.pagar()
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
        pedido.pagar()
        with pytest.raises(ValueError):
            pedido.adicionar_item(self.mouse, 1)
