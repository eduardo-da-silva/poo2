import pytest

from ecommerce.categoria import Categoria
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
from ecommerce.repositorio_pedido import PedidoNaoEncontradoError
from ecommerce.repositorio_pedido_memoria import RepositorioPedidoMemoria


@pytest.fixture(params=["memoria"])
def repositorio(request: pytest.FixtureRequest):
    return RepositorioPedidoMemoria()


def _pedido() -> Pedido:
    notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    notebook.atribuir_id(1)
    pedido = Pedido()
    pedido.adicionar_item(notebook, 2)
    return pedido


class TestRepositorioPedido:

    def test_adicionar_atribui_identidade(self, repositorio) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        assert pedido.id is not None

    def test_obter_devolve_itens_e_status(self, repositorio) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        encontrado = repositorio.obter(pedido.id)
        assert encontrado.status == "criado"
        assert encontrado.quantidade_itens() == 1
        assert encontrado.calcular_total() == 7000.0

    def test_obter_inexistente_falha(self, repositorio) -> None:
        with pytest.raises(PedidoNaoEncontradoError):
            repositorio.obter(99)

    def test_atualizar_registra_a_mudanca_de_status(self, repositorio) -> None:
        pedido = _pedido()
        repositorio.adicionar(pedido)
        pedido.cancelar()
        repositorio.atualizar(pedido)
        assert repositorio.obter(pedido.id).status == "cancelado"

    def test_listar_devolve_todos(self, repositorio) -> None:
        repositorio.adicionar(_pedido())
        repositorio.adicionar(_pedido())
        assert len(repositorio.listar()) == 2
