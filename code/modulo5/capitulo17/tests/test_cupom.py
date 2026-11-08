from datetime import date, timedelta

import pytest
from ecommerce.cupom import Cupom
from ecommerce.estrategia_desconto import DescontoPercentual


class TestCupom:

    def setup_method(self) -> None:
        self.amanha = date.today() + timedelta(days=1)
        self.ontem = date.today() - timedelta(days=1)

    def test_cupom_valido(self) -> None:
        cupom = Cupom("BEMVINDO10", self.amanha, DescontoPercentual(10))
        assert cupom.esta_valido() is True

    def test_cupom_expirado(self) -> None:
        cupom = Cupom("PROMOANTIGA", self.ontem, DescontoPercentual(10))
        assert cupom.esta_valido() is False

    def test_calcular_desconto_cupom_valido(self) -> None:
        cupom = Cupom("BEMVINDO10", self.amanha, DescontoPercentual(10))
        assert cupom.calcular_desconto(1000.0) == 900.0

    def test_calcular_desconto_cupom_expirado_lanca_erro(self) -> None:
        cupom = Cupom("PROMOANTIGA", self.ontem, DescontoPercentual(10))
        with pytest.raises(ValueError):
            cupom.calcular_desconto(1000.0)
