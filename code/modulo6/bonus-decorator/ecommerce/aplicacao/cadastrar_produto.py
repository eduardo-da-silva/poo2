from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.produto import Produto
from ecommerce.dominio.repositorio_produto import RepositorioProduto


class CadastrarProduto:
    """Caso de uso: colocar um produto novo no catalogo."""

    def __init__(self, repositorio_produto: RepositorioProduto) -> None:
        self._repositorio_produto = repositorio_produto

    def executar(
        self, nome: str, preco: float, quantidade_estoque: int, categoria: str
    ) -> Produto:
        produto = Produto(nome, preco, quantidade_estoque, Categoria(categoria))
        self._repositorio_produto.adicionar(produto)
        return produto
