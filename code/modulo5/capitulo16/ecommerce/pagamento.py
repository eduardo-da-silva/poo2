from abc import ABC, abstractmethod
from datetime import date

from ecommerce.situacao_pagamento import SituacaoPagamento


class Pagamento(ABC):

    def __init__(self, pedido: "Pedido", valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        self._pedido = pedido
        self._valor = valor
        self._data = date.today()
        self._situacao = SituacaoPagamento.PENDENTE

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
    def situacao(self) -> SituacaoPagamento:
        return self._situacao

    @property
    def confirmado(self) -> bool:
        return self._situacao == SituacaoPagamento.CONFIRMADO

    def confirmar(self) -> None:
        if self._situacao == SituacaoPagamento.CONFIRMADO:
            raise ValueError("Pagamento ja foi confirmado")
        self._situacao = self._processar()

    @abstractmethod
    def _processar(self) -> SituacaoPagamento:
        ...


class PagamentoPix(Pagamento):

    def __init__(self, pedido: "Pedido", valor: float, chave: str) -> None:
        super().__init__(pedido, valor)
        self._chave = chave

    @property
    def chave(self) -> str:
        return self._chave

    def _processar(self) -> SituacaoPagamento:
        # A compensacao do Pix e imediata: nada mais precisa acontecer.
        return SituacaoPagamento.CONFIRMADO


class PagamentoBoleto(Pagamento):

    def __init__(
        self, pedido: "Pedido", valor: float, linha_digitavel: str, vencimento: date
    ) -> None:
        super().__init__(pedido, valor)
        self._linha_digitavel = linha_digitavel
        self._vencimento = vencimento

    @property
    def linha_digitavel(self) -> str:
        return self._linha_digitavel

    @property
    def vencimento(self) -> date:
        return self._vencimento

    def _processar(self) -> SituacaoPagamento:
        if date.today() > self._vencimento:
            return SituacaoPagamento.RECUSADO
        return SituacaoPagamento.CONFIRMADO


class PagamentoCartao(Pagamento):

    def __init__(
        self, pedido: "Pedido", valor: float, bandeira: str, parcelas: int = 1
    ) -> None:
        super().__init__(pedido, valor)
        if parcelas < 1:
            raise ValueError("Numero de parcelas deve ser no minimo 1")
        self._bandeira = bandeira
        self._parcelas = parcelas

    @property
    def bandeira(self) -> str:
        return self._bandeira

    @property
    def parcelas(self) -> int:
        return self._parcelas

    def valor_parcela(self) -> float:
        return self._valor / self._parcelas

    def _processar(self) -> SituacaoPagamento:
        return SituacaoPagamento.CONFIRMADO


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.pedido import Pedido
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    pedido = Pedido()
    pedido.adicionar_item(notebook, 1)

    pagamento = PagamentoPix(pedido, pedido.calcular_total(), chave="loja@ecommerce.com")
    print(f"Situacao: {pagamento.situacao}")
    pagamento.confirmar()
    print(f"Situacao apos confirmar: {pagamento.situacao}")
