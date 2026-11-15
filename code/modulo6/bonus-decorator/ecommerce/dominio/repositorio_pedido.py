from abc import ABC, abstractmethod

from ecommerce.dominio.pedido import Pedido


class PedidoNaoEncontradoError(Exception):
    pass


class RepositorioPedido(ABC):
    """Contrato de guarda dos pedidos: o dominio so conhece esta interface."""

    @abstractmethod
    def adicionar(self, pedido: Pedido) -> None:
        """Guarda um pedido novo e atribui a ele uma identidade."""
        ...

    @abstractmethod
    def obter(self, id: int) -> Pedido:
        ...

    @abstractmethod
    def listar(self) -> list[Pedido]:
        ...

    @abstractmethod
    def atualizar(self, pedido: Pedido) -> None:
        """Registra as mudancas feitas em um pedido que ja foi guardado."""
        ...
