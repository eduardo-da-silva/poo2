from ecommerce.aplicacao.registro_auditoria import RegistroAuditoria
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago


class RegistrarAuditoria:
    """Reage a qualquer evento de pedido deixando uma linha no registro de auditoria."""

    def __init__(self, registro: RegistroAuditoria) -> None:
        self._registro = registro

    def __call__(self, evento: PedidoPago | PedidoDespachado) -> None:
        self._registro.registrar(
            f"{type(evento).__name__}: pedido {evento.pedido.id}, cliente {evento.cliente.nome}"
        )
