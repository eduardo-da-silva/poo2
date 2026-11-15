from ecommerce.aplicacao.registro_auditoria import RegistroAuditoria


class RegistroAuditoriaEmMemoria(RegistroAuditoria):

    def __init__(self) -> None:
        self._entradas: list[str] = []

    def registrar(self, entrada: str) -> None:
        self._entradas.append(entrada)

    def entradas(self) -> list[str]:
        return list(self._entradas)


if __name__ == "__main__":
    registro = RegistroAuditoriaEmMemoria()
    registro.registrar("PedidoPago: pedido 1")
    print(registro.entradas())
