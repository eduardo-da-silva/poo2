from abc import ABC, abstractmethod

from ecommerce.dominio.produto import Produto


class ProdutoNaoEncontradoError(Exception):
    pass


class RepositorioProduto(ABC):
    """Contrato de guarda dos produtos: o dominio so conhece esta interface."""

    @abstractmethod
    def adicionar(self, produto: Produto) -> None:
        """Guarda um produto novo e atribui a ele uma identidade."""
        ...

    @abstractmethod
    def obter(self, id: int) -> Produto:
        ...

    @abstractmethod
    def listar(self) -> list[Produto]:
        ...

    @abstractmethod
    def atualizar(self, produto: Produto) -> None:
        """Registra as mudancas feitas em um produto que ja foi guardado."""
        ...
