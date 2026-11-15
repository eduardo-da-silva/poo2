from dataclasses import dataclass

from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.entrega import Entrega
from ecommerce.dominio.pedido import Pedido


@dataclass(frozen=True)
class PedidoPago:
    """Fato: o pagamento de um pedido foi confirmado."""

    pedido: Pedido
    cliente: Cliente


@dataclass(frozen=True)
class PedidoDespachado:
    """Fato: um pedido pago saiu para entrega."""

    pedido: Pedido
    cliente: Cliente
    entrega: Entrega
