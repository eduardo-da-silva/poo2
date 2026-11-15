from ecommerce.dominio.produto import Produto
from ecommerce.dominio.repositorio_produto import RepositorioProduto


class ListarProdutos:
    """Caso de uso de consulta: quais produtos a loja tem."""

    def __init__(self, repositorio_produto: RepositorioProduto) -> None:
        self._repositorio_produto = repositorio_produto

    def executar(self) -> list[Produto]:
        return self._repositorio_produto.listar()
