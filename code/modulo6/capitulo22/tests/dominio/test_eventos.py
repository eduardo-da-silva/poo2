from dataclasses import FrozenInstanceError

import pytest

from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago
from ecommerce.dominio.pedido import Pedido


def test_evento_e_um_fato_imutavel() -> None:
    evento = PedidoPago(Pedido(), Cliente("Maria", "maria@email.com"))
    with pytest.raises(FrozenInstanceError):
        evento.cliente = Cliente("Joao", "joao@email.com")


def test_eventos_com_os_mesmos_dados_sao_iguais() -> None:
    pedido = Pedido()
    maria = Cliente("Maria", "maria@email.com")
    assert PedidoPago(pedido, maria) == PedidoPago(pedido, maria)


def test_eventos_de_tipos_diferentes_nao_se_confundem() -> None:
    pedido = Pedido()
    maria = Cliente("Maria", "maria@email.com")
    assert PedidoPago(pedido, maria) != PedidoDespachado(pedido, maria, None)
