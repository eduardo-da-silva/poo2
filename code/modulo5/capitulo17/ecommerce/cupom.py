from datetime import date

from ecommerce.estrategia_desconto import EstrategiaDesconto


class Cupom:

    def __init__(self, codigo: str, validade: date, estrategia_desconto: EstrategiaDesconto) -> None:
        self._codigo = codigo
        self._validade = validade
        self._estrategia_desconto = estrategia_desconto

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def validade(self) -> date:
        return self._validade

    def esta_valido(self, hoje: date | None = None) -> bool:
        hoje = hoje if hoje is not None else date.today()
        return hoje <= self._validade

    def calcular_desconto(self, total: float) -> float:
        if not self.esta_valido():
            raise ValueError(f"Cupom {self._codigo} esta expirado")
        return self._estrategia_desconto.calcular(total)
