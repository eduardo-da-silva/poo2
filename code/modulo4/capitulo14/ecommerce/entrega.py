from abc import ABC, abstractmethod


class Entrega(ABC):

    def __init__(self, pedido: "Pedido", codigo_rastreio: str) -> None:
        self._pedido = pedido
        self._codigo_rastreio = codigo_rastreio

    @property
    def pedido(self) -> "Pedido":
        return self._pedido

    @property
    def codigo_rastreio(self) -> str:
        return self._codigo_rastreio

    @abstractmethod
    def prazo_estimado(self) -> int:
        """Numero de dias uteis previstos ate a entrega."""
        ...

    def etiqueta(self) -> str:
        return (
            f"{type(self).__name__} | rastreio {self._codigo_rastreio} "
            f"| prazo {self.prazo_estimado()} dias uteis"
        )


class EntregaCorreios(Entrega):

    def __init__(self, pedido: "Pedido", codigo_rastreio: str, modalidade: str = "PAC") -> None:
        super().__init__(pedido, codigo_rastreio)
        self._modalidade = modalidade

    @property
    def modalidade(self) -> str:
        return self._modalidade

    def prazo_estimado(self) -> int:
        return 3 if self._modalidade == "SEDEX" else 8


class EntregaTransportadora(Entrega):

    def __init__(self, pedido: "Pedido", codigo_rastreio: str, transportadora: str) -> None:
        super().__init__(pedido, codigo_rastreio)
        self._transportadora = transportadora

    @property
    def transportadora(self) -> str:
        return self._transportadora

    def prazo_estimado(self) -> int:
        return 5


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.pedido import Pedido
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    pedido = Pedido()
    pedido.adicionar_item(notebook, 1)

    correios = EntregaCorreios(pedido, "BR000001SE", modalidade="SEDEX")
    parceira = EntregaTransportadora(pedido, "TR000001", transportadora="Transportadora Sul")
    print(correios.etiqueta())
    print(parceira.etiqueta())
