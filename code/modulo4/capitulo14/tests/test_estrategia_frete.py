import pytest
from ecommerce.estrategia_frete import FreteFixo, FreteGratisAcimaDe


class TestFreteFixo:

    def test_calcula_valor_fixo(self) -> None:
        estrategia = FreteFixo(25.0)
        assert estrategia.calcular(100.0) == 25.0
        assert estrategia.calcular(1000.0) == 25.0

    def test_valor_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            FreteFixo(-10.0)


class TestFreteGratisAcimaDe:

    def test_frete_gratis_quando_atinge_o_minimo(self) -> None:
        estrategia = FreteGratisAcimaDe(valor_minimo=200.0, valor_frete=30.0)
        assert estrategia.calcular(200.0) == 0.0
        assert estrategia.calcular(500.0) == 0.0

    def test_cobra_frete_abaixo_do_minimo(self) -> None:
        estrategia = FreteGratisAcimaDe(valor_minimo=200.0, valor_frete=30.0)
        assert estrategia.calcular(150.0) == 30.0
