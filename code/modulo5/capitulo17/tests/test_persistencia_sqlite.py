import sqlite3

from ecommerce.categoria import Categoria
from ecommerce.esquema_sqlite import criar_esquema
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
from ecommerce.repositorio_pedido_sqlite import RepositorioPedidoSQLite
from ecommerce.repositorio_produto_sqlite import RepositorioProdutoSQLite


def _abrir(caminho: str) -> tuple[RepositorioProdutoSQLite, RepositorioPedidoSQLite, sqlite3.Connection]:
    conexao = sqlite3.connect(caminho)
    criar_esquema(conexao)
    produtos = RepositorioProdutoSQLite(conexao)
    return produtos, RepositorioPedidoSQLite(conexao, produtos), conexao


class TestPersistenciaSQLite:
    """O que so a implementacao em SQLite precisa garantir."""

    def test_os_dados_sobrevivem_ao_reinicio_do_programa(self, tmp_path) -> None:
        arquivo = str(tmp_path / "loja.db")

        produtos, pedidos, conexao = _abrir(arquivo)
        notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
        produtos.adicionar(notebook)
        pedido = Pedido()
        pedido.adicionar_item(notebook, 1)
        pedidos.adicionar(pedido)
        pedido.cancelar()
        pedidos.atualizar(pedido)
        conexao.close()

        _, pedidos_novos, conexao_nova = _abrir(arquivo)
        relido = pedidos_novos.obter(pedido.id)
        assert relido.status == "cancelado"
        assert relido.itens[0].produto.nome == "Notebook"
        conexao_nova.close()

    def test_mudanca_sem_atualizar_nao_e_guardada(self) -> None:
        produtos, _, _ = _abrir(":memory:")
        mouse = Produto("Mouse", 150.0, 20, Categoria("Informática"))
        produtos.adicionar(mouse)
        mouse.alterar_preco(1.0)  # esquecemos o atualizar()
        assert produtos.obter(mouse.id).preco == 150.0

    def test_cada_leitura_devolve_um_objeto_novo(self) -> None:
        produtos, _, _ = _abrir(":memory:")
        mouse = Produto("Mouse", 150.0, 20, Categoria("Informática"))
        produtos.adicionar(mouse)
        assert produtos.obter(mouse.id) is not mouse
