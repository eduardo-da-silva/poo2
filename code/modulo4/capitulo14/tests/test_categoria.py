from ecommerce.categoria import Categoria


class TestCategoria:

    def test_criar_categoria(self) -> None:
        cat = Categoria("Informática")
        assert cat.nome == "Informática"

    def test_categoria_com_nome_vazio(self) -> None:
        cat = Categoria("")
        assert cat.nome == ""
