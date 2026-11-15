import pytest
from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.produto import EstoqueInsuficienteError, Produto


class TestProduto:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")

    def test_criar_produto(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        assert p.nome == "Notebook"
        assert p.preco == 3500.0
        assert p.quantidade_estoque == 10
        assert p.categoria == self.cat

    def test_produto_disponivel(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        assert p.esta_disponivel() is True

    def test_produto_indisponivel(self) -> None:
        p = Produto("Notebook", 3500.0, 0, self.cat)
        assert p.esta_disponivel() is False

    def test_produto_sem_estoque_negativo(self) -> None:
        p = Produto("Notebook", 3500.0, -1, self.cat)
        assert p.esta_disponivel() is False

    def test_aplicar_desconto_valido(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        p.aplicar_desconto(10)
        assert p.preco == 900.0

    def test_aplicar_desconto_zero(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        p.aplicar_desconto(0)
        assert p.preco == 1000.0

    def test_aplicar_desconto_cem(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        p.aplicar_desconto(100)
        assert p.preco == 0.0

    def test_aplicar_desconto_invalido_negativo(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        with pytest.raises(ValueError):
            p.aplicar_desconto(-1)

    def test_aplicar_desconto_invalido_acima_cem(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        with pytest.raises(ValueError):
            p.aplicar_desconto(101)

    def test_alterar_preco_valido(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        p.alterar_preco(1500.0)
        assert p.preco == 1500.0

    def test_alterar_preco_invalido(self) -> None:
        p = Produto("Notebook", 1000.0, 10, self.cat)
        with pytest.raises(ValueError):
            p.alterar_preco(0)

    def test_dar_baixa_reduz_o_estoque(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        p.dar_baixa(3)
        assert p.quantidade_estoque == 7

    def test_dar_baixa_alem_do_estoque_falha_sem_alterar_nada(self) -> None:
        p = Produto("Notebook", 3500.0, 2, self.cat)
        with pytest.raises(EstoqueInsuficienteError):
            p.dar_baixa(3)
        assert p.quantidade_estoque == 2

    def test_dar_baixa_exige_quantidade_positiva(self) -> None:
        p = Produto("Notebook", 3500.0, 10, self.cat)
        with pytest.raises(ValueError):
            p.dar_baixa(0)
