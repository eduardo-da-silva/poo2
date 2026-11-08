import pytest

from ecommerce.categoria import Categoria
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
from ecommerce.repositorio_pedido import PedidoNaoEncontradoError


@pytest.fixture
def repositorio(infra):
    return infra.pedidos


@pytest.fixture
def _pedido(infra):
    # Os itens apontam para produtos, que precisam existir no repositorio.
    notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    infra.produtos.adicionar(notebook)

    def criar() -> Pedido:
        pedido = Pedido()
        pedido.adicionar_item(notebook, 2)
        return pedido

    return criar


class TestRepositorioPedido:

    def test_adicionar_atribui_identidade(self, repositorio, _pedido) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        assert pedido.id is not None

    def test_obter_devolve_itens_e_status(self, repositorio, _pedido) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        encontrado = repositorio.obter(pedido.id)
        assert encontrado.status == "criado"
        assert encontrado.quantidade_itens() == 1
        assert encontrado.calcular_total() == 7000.0

    def test_obter_inexistente_falha(self, repositorio, _pedido) -> None:
        with pytest.raises(PedidoNaoEncontradoError):
            repositorio.obter(99)

    def test_atualizar_registra_a_mudanca_de_status(self, repositorio, _pedido) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        pedido.cancelar()
        repositorio.atualizar(pedido)
        assert repositorio.obter(pedido.id).status == "cancelado"

    def test_listar_devolve_todos(self, repositorio, _pedido) -> None:
        repositorio.adicionar(_pedido())
        repositorio.adicionar(_pedido())
        assert len(repositorio.listar()) == 2

    def test_itens_guardam_o_preco_do_momento_da_compra(self, repositorio, infra, _pedido) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        produto = infra.produtos.listar()[0]
        produto.alterar_preco(9999.0)
        infra.produtos.atualizar(produto)
        item = repositorio.obter(pedido.id).itens[0]
        assert item.preco_no_momento == 3500.0
        assert item.produto.preco == 9999.0
