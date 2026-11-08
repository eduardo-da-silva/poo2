class StatusPedido:
    CRIADO = "criado"
    PAGO = "pago"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

    _TRANSIcoES_VALIDAS = {
        CRIADO: [PAGO, CANCELADO],
        PAGO: [ENVIADO, CANCELADO],
        ENVIADO: [ENTREGUE],
        ENTREGUE: [],
        CANCELADO: [],
    }

    @classmethod
    def transicao_valida(cls, de: str, para: str) -> bool:
        return para in cls._TRANSIcoES_VALIDAS.get(de, [])


if __name__ == "__main__":
    print(f"Status criado: {StatusPedido.CRIADO}")
    print(f"CRIADO -> PAGO: {StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.PAGO)}")
    print(f"CRIADO -> ENTREGUE: {StatusPedido.transicao_valida(StatusPedido.CRIADO, StatusPedido.ENTREGUE)}")
