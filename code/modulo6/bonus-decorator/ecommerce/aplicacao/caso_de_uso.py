from typing import Any, Protocol


class CasoDeUso(Protocol):
    """O formato comum dos casos de uso: algo que se executa e devolve um resultado."""

    def executar(self, *args: Any, **kwargs: Any) -> Any:
        ...
