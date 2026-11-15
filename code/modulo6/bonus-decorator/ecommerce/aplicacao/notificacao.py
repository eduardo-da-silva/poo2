from abc import ABC, abstractmethod
from typing import Protocol

from ecommerce.dominio.canal_notificacao import CanalNotificacao


class Notificacao(ABC):
    """Porta de saida: o que a aplicacao precisa para avisar o cliente."""

    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        ...


class FabricaNotificacao(Protocol):
    """O que a aplicacao exige de quem sabe criar a notificacao de um canal."""

    def criar(self, canal: CanalNotificacao) -> Notificacao:
        ...
