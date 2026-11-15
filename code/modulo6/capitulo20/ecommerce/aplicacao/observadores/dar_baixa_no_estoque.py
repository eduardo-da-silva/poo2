from ecommerce.aplicacao.observador_de_pagamento import ObservadorDePagamento
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_produto import RepositorioProduto


class DarBaixaNoEstoque(ObservadorDePagamento):
    """Tira do estoque as unidades vendidas em um pedido pago."""

    def __init__(self, repositorio_produto: RepositorioProduto) -> None:
        self._repositorio_produto = repositorio_produto

    def atualizar(self, pedido: Pedido, cliente: Cliente) -> None:
        for item in pedido.itens:
            # Buscamos o produto de novo: o do item pode ser uma copia
            # (no SQLite) e dois itens do mesmo produto nao podem se atropelar.
            produto = self._repositorio_produto.obter(item.produto.id)
            produto.dar_baixa(item.quantidade)
            self._repositorio_produto.atualizar(produto)
