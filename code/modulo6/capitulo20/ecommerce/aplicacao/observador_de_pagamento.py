from abc import ABC, abstractmethod

from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.pedido import Pedido


class ObservadorDePagamento(ABC):
    """Quem quer ser avisado quando um pedido e pago."""

    @abstractmethod
    def atualizar(self, pedido: Pedido, cliente: Cliente) -> None:
        ...
