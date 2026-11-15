import sqlite3

from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.produto import Produto
from ecommerce.dominio.repositorio_produto import ProdutoNaoEncontradoError, RepositorioProduto


class RepositorioProdutoSQLite(RepositorioProduto):

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def adicionar(self, produto: Produto) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "INSERT INTO produto (nome, preco, quantidade_estoque, categoria) "
                "VALUES (?, ?, ?, ?)",
                (produto.nome, produto.preco, produto.quantidade_estoque, produto.categoria.nome),
            )
        produto.atribuir_id(cursor.lastrowid)

    def obter(self, id: int) -> Produto:
        linha = self._conexao.execute(
            "SELECT id, nome, preco, quantidade_estoque, categoria FROM produto WHERE id = ?",
            (id,),
        ).fetchone()
        if linha is None:
            raise ProdutoNaoEncontradoError(f"Produto {id} nao encontrado")
        return self._reconstituir(linha)

    def listar(self) -> list[Produto]:
        linhas = self._conexao.execute(
            "SELECT id, nome, preco, quantidade_estoque, categoria FROM produto ORDER BY id"
        ).fetchall()
        return [self._reconstituir(linha) for linha in linhas]

    def atualizar(self, produto: Produto) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "UPDATE produto SET nome = ?, preco = ?, quantidade_estoque = ?, categoria = ? "
                "WHERE id = ?",
                (
                    produto.nome,
                    produto.preco,
                    produto.quantidade_estoque,
                    produto.categoria.nome,
                    produto.id,
                ),
            )
        if cursor.rowcount == 0:
            raise ProdutoNaoEncontradoError("Produto nunca foi adicionado")

    @staticmethod
    def _reconstituir(linha: tuple) -> Produto:
        id, nome, preco, quantidade_estoque, categoria = linha
        produto = Produto(nome, preco, quantidade_estoque, Categoria(categoria))
        produto.atribuir_id(id)
        return produto


if __name__ == "__main__":
    from ecommerce.infraestrutura.esquema_sqlite import criar_esquema

    conexao = sqlite3.connect(":memory:")
    criar_esquema(conexao)
    repositorio = RepositorioProdutoSQLite(conexao)
    repositorio.adicionar(Produto("Notebook", 3500.0, 10, Categoria("Informática")))
    print(f"Produtos guardados: {[p.nome for p in repositorio.listar()]}")
