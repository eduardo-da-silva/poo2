from abc import ABC, abstractmethod


class EstrategiaFrete(ABC):

    @abstractmethod
    def calcular(self, total_pedido: float) -> float:
        ...


class FreteFixo(EstrategiaFrete):

    def __init__(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("Valor do frete nao pode ser negativo")
        self._valor = valor

    def calcular(self, total_pedido: float) -> float:
        return self._valor


class FreteGratisAcimaDe(EstrategiaFrete):

    def __init__(self, valor_minimo: float, valor_frete: float) -> None:
        self._valor_minimo = valor_minimo
        self._valor_frete = valor_frete

    def calcular(self, total_pedido: float) -> float:
        if total_pedido >= self._valor_minimo:
            return 0.0
        return self._valor_frete
