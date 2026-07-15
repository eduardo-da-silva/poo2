from datetime import date


class Pagamento:

    def __init__(self, pedido: "Pedido", valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        self._pedido = pedido
        self._valor = valor
        self._data = date.today()
        self._confirmado = False

    @property
    def pedido(self) -> "Pedido":
        return self._pedido

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data(self) -> date:
        return self._data

    @property
    def confirmado(self) -> bool:
        return self._confirmado

    def confirmar(self) -> None:
        if self._confirmado:
            raise ValueError("Pagamento ja foi confirmado")
        self._confirmado = True


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.pedido import Pedido
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    pedido = Pedido()
    pedido.adicionar_item(notebook, 1)

    pagamento = Pagamento(pedido, pedido.calcular_total())
    print(f"Valor: R$ {pagamento.valor}")
    print(f"Confirmado: {pagamento.confirmado}")
    pagamento.confirmar()
    print(f"Confirmado apos confirmar: {pagamento.confirmado}")
