from ecommerce.dominio.eventos import PedidoPago
from ecommerce.dominio.repositorio_produto import RepositorioProduto


class DarBaixaNoEstoque:
    """Reage a PedidoPago tirando do estoque as unidades vendidas."""

    def __init__(self, repositorio_produto: RepositorioProduto) -> None:
        self._repositorio_produto = repositorio_produto

    def __call__(self, evento: PedidoPago) -> None:
        for item in evento.pedido.itens:
            # Buscamos o produto de novo: o do item pode ser uma copia
            # (no SQLite) e dois itens do mesmo produto nao podem se atropelar.
            produto = self._repositorio_produto.obter(item.produto.id)
            produto.dar_baixa(item.quantidade)
            self._repositorio_produto.atualizar(produto)
