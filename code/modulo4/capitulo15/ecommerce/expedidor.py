from abc import ABC, abstractmethod

from ecommerce.entrega import Entrega, EntregaCorreios, EntregaTransportadora


class Expedidor(ABC):

    def despachar(self, pedido: "Pedido") -> Entrega:
        # Fluxo comum a toda expedicao. So a criacao da entrega varia.
        entrega = self.criar_entrega(pedido)
        pedido.registrar_entrega(entrega)
        pedido.enviar()
        return entrega

    @abstractmethod
    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        ...


class ExpedidorLojaCentral(Expedidor):

    def __init__(self) -> None:
        self._despachos = 0

    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        self._despachos += 1
        codigo = f"BR{self._despachos:06d}SE"
        return EntregaCorreios(pedido, codigo, modalidade="SEDEX")


class ExpedidorCentroRegional(Expedidor):

    def __init__(self, transportadora: str = "Transportadora Sul") -> None:
        self._transportadora = transportadora
        self._despachos = 0

    def criar_entrega(self, pedido: "Pedido") -> Entrega:
        self._despachos += 1
        codigo = f"TR{self._despachos:06d}"
        return EntregaTransportadora(pedido, codigo, transportadora=self._transportadora)


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.criador_pagamento import CriadorPagamento
    from ecommerce.pedido import Pedido
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    for expedidor in (ExpedidorLojaCentral(), ExpedidorCentroRegional()):
        pedido = Pedido()
        pedido.adicionar_item(notebook, 1)
        pedido.confirmar_pagamento(CriadorPagamento())
        entrega = expedidor.despachar(pedido)
        print(f"{type(expedidor).__name__}: {entrega.etiqueta()} | status {pedido.status}")
