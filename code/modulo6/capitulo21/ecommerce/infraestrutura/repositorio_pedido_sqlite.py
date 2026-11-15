import sqlite3

from ecommerce.dominio.item_pedido import ItemPedido
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import PedidoNaoEncontradoError, RepositorioPedido
from ecommerce.dominio.repositorio_produto import RepositorioProduto


class RepositorioPedidoSQLite(RepositorioPedido):

    def __init__(
        self, conexao: sqlite3.Connection, repositorio_produto: RepositorioProduto
    ) -> None:
        self._conexao = conexao
        # Os itens apontam para produtos: quem sabe reconstituir um Produto
        # e o repositorio de produtos, entao ele chega por injecao.
        self._repositorio_produto = repositorio_produto

    def adicionar(self, pedido: Pedido) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "INSERT INTO pedido (status) VALUES (?)", (pedido.status,)
            )
            self._gravar_itens(cursor.lastrowid, pedido)
        pedido.atribuir_id(cursor.lastrowid)

    def obter(self, id: int) -> Pedido:
        linha = self._conexao.execute(
            "SELECT id, status FROM pedido WHERE id = ?", (id,)
        ).fetchone()
        if linha is None:
            raise PedidoNaoEncontradoError(f"Pedido {id} nao encontrado")
        return self._reconstituir(*linha)

    def listar(self) -> list[Pedido]:
        linhas = self._conexao.execute("SELECT id, status FROM pedido ORDER BY id").fetchall()
        return [self._reconstituir(*linha) for linha in linhas]

    def atualizar(self, pedido: Pedido) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "UPDATE pedido SET status = ? WHERE id = ?", (pedido.status, pedido.id)
            )
            if cursor.rowcount == 0:
                raise PedidoNaoEncontradoError("Pedido nunca foi adicionado")
            self._conexao.execute("DELETE FROM item_pedido WHERE pedido_id = ?", (pedido.id,))
            self._gravar_itens(pedido.id, pedido)

    def _gravar_itens(self, pedido_id: int, pedido: Pedido) -> None:
        self._conexao.executemany(
            "INSERT INTO item_pedido (pedido_id, produto_id, quantidade, preco_no_momento) "
            "VALUES (?, ?, ?, ?)",
            [
                (pedido_id, item.produto.id, item.quantidade, item.preco_no_momento)
                for item in pedido.itens
            ],
        )

    def _reconstituir(self, id: int, status: str) -> Pedido:
        linhas = self._conexao.execute(
            "SELECT produto_id, quantidade, preco_no_momento FROM item_pedido "
            "WHERE pedido_id = ?",
            (id,),
        ).fetchall()
        itens = [
            ItemPedido(self._repositorio_produto.obter(produto_id), quantidade, preco)
            for produto_id, quantidade, preco in linhas
        ]
        return Pedido.reconstituir(id, status, itens)


if __name__ == "__main__":
    from ecommerce.dominio.categoria import Categoria
    from ecommerce.infraestrutura.esquema_sqlite import criar_esquema
    from ecommerce.dominio.produto import Produto
    from ecommerce.infraestrutura.repositorio_produto_sqlite import RepositorioProdutoSQLite

    conexao = sqlite3.connect(":memory:")
    criar_esquema(conexao)
    produtos = RepositorioProdutoSQLite(conexao)
    pedidos = RepositorioPedidoSQLite(conexao, produtos)

    mouse = Produto("Mouse", 150.0, 20, Categoria("Informática"))
    produtos.adicionar(mouse)
    pedido = Pedido()
    pedido.adicionar_item(mouse, 2)
    pedidos.adicionar(pedido)
    print(f"Pedido {pedido.id} relido: R$ {pedidos.obter(pedido.id).calcular_total():.2f}")
