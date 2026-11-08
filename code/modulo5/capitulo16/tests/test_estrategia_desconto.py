import pytest
from ecommerce.estrategia_desconto import DescontoPercentual, SemDesconto


class TestSemDesconto:

    def test_nao_altera_o_total(self) -> None:
        estrategia = SemDesconto()
        assert estrategia.calcular(1000.0) == 1000.0


class TestDescontoPercentual:

    def test_calcula_desconto_de_dez_por_cento(self) -> None:
        estrategia = DescontoPercentual(10)
        assert estrategia.calcular(1000.0) == 900.0

    def test_calcula_desconto_de_cem_por_cento(self) -> None:
        estrategia = DescontoPercentual(100)
        assert estrategia.calcular(1000.0) == 0.0

    def test_percentual_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            DescontoPercentual(-1)

    def test_percentual_acima_de_cem_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            DescontoPercentual(101)
