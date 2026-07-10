from ecommerce.categoria import Categoria


class TestCategoria:

    def test_cria_categoria_com_nome(self) -> None:
        cat = Categoria("Informática")
        assert cat.nome == "Informática"
