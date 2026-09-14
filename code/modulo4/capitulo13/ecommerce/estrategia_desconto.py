from abc import ABC, abstractmethod


class EstrategiaDesconto(ABC):

    @abstractmethod
    def calcular(self, total: float) -> float:
        ...


class SemDesconto(EstrategiaDesconto):

    def calcular(self, total: float) -> float:
        return total


class DescontoPercentual(EstrategiaDesconto):

    def __init__(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self._percentual = percentual

    def calcular(self, total: float) -> float:
        return total - (total * self._percentual / 100)
