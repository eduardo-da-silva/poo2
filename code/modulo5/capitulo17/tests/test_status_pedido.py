from ecommerce.status_pedido import StatusPedido


class TestStatusPedido:

    def test_status_criado(self) -> None:
        assert StatusPedido.CRIADO == "criado"

    def test_status_pago(self) -> None:
        assert StatusPedido.PAGO == "pago"

    def test_transicao_valida(self) -> None:
        assert StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.PAGO) is True
        assert StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.CANCELADO) is True
        assert StatusPedido.transicao_valida(StatusPedido.PAGO, StatusPedido.ENVIADO) is True
        assert StatusPedido.transicao_valida(StatusPedido.ENVIADO, StatusPedido.ENTREGUE) is True

    def test_transicao_invalida(self) -> None:
        assert StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.ENTREGUE) is False
        assert StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.ENVIADO) is False
        assert StatusPedido.transicao_valida(StatusPedido.PAGO, StatusPedido.ENTREGUE) is False
        assert StatusPedido.transicao_valida(StatusPedido.ENTREGUE, StatusPedido.CANCELADO) is False

    def test_entregue_nao_transiciona(self) -> None:
        assert StatusPedido.transicao_valida(StatusPedido.ENTREGUE, StatusPedido.CANCELADO) is False
        assert StatusPedido.transicao_valida(StatusPedido.ENTREGUE, StatusPedido.PAGO) is False

    def test_cancelado_nao_transiciona(self) -> None:
        assert StatusPedido.transicao_valida(StatusPedido.CANCELADO, StatusPedido.CRIADO) is False
        assert StatusPedido.transicao_valida(StatusPedido.CANCELADO, StatusPedido.PAGO) is False
