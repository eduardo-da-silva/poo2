from abc import ABC, abstractmethod


class RegistroAuditoria(ABC):
    """Porta: onde ficam guardadas as linhas de auditoria."""

    @abstractmethod
    def registrar(self, entrada: str) -> None:
        ...

    @abstractmethod
    def entradas(self) -> list[str]:
        ...
