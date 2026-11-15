from abc import ABC, abstractmethod
from typing import Any, Callable

Manipulador = Callable[[Any], None]


class BarramentoEventos(ABC):
    """Porta: por onde a aplicacao anuncia fatos e por onde quem se interessa se inscreve."""

    @abstractmethod
    def inscrever(self, tipo_evento: type, manipulador: Manipulador) -> None:
        ...

    @abstractmethod
    def publicar(self, evento: object) -> None:
        ...
