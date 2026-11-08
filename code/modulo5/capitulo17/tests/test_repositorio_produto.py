import pytest

from ecommerce.categoria import Categoria
from ecommerce.produto import Produto
from ecommerce.repositorio_produto import ProdutoNaoEncontradoError


@pytest.fixture
def repositorio(infra):
    return infra.produtos


def _notebook() -> Produto:
    return Produto("Notebook", 3500.0, 10, Categoria("Informática"))


class TestRepositorioProduto:

    def test_adicionar_atribui_identidade(self, repositorio) -> None:
        produto = _notebook()
        repositorio.adicionar(produto)
        assert produto.id is not None

    def test_obter_devolve_o_produto_guardado(self, repositorio) -> None:
        produto = _notebook()
        repositorio.adicionar(produto)
        encontrado = repositorio.obter(produto.id)
        assert encontrado.nome == "Notebook"
        assert encontrado.preco == 3500.0
        assert encontrado.categoria.nome == "Informática"

    def test_obter_inexistente_falha(self, repositorio) -> None:
        with pytest.raises(ProdutoNaoEncontradoError):
            repositorio.obter(99)

    def test_listar_devolve_todos(self, repositorio) -> None:
        repositorio.adicionar(_notebook())
        repositorio.adicionar(Produto("Mouse", 150.0, 20, Categoria("Informática")))
        assert [p.nome for p in repositorio.listar()] == ["Notebook", "Mouse"]

    def test_atualizar_registra_as_mudancas(self, repositorio) -> None:
        produto = _notebook()
        repositorio.adicionar(produto)
        produto.alterar_preco(4000.0)
        repositorio.atualizar(produto)
        assert repositorio.obter(produto.id).preco == 4000.0

    def test_atualizar_produto_nunca_adicionado_falha(self, repositorio) -> None:
        with pytest.raises(ProdutoNaoEncontradoError):
            repositorio.atualizar(_notebook())

    def test_identidade_so_pode_ser_atribuida_uma_vez(self) -> None:
        produto = _notebook()
        produto.atribuir_id(1)
        with pytest.raises(ValueError):
            produto.atribuir_id(2)
