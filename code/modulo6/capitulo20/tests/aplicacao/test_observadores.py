import pytest

from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.observadores.dar_baixa_no_estoque import DarBaixaNoEstoque
from ecommerce.aplicacao.observadores.notificar_cliente_do_pagamento import (
    NotificarClienteDoPagamento,
)
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.produto import EstoqueInsuficienteError, Produto


def _cliente_com(produto: Produto, *quantidades: int) -> Cliente:
    cliente = Cliente("Maria", "maria@email.com")
    cliente.carrinho = Carrinho()
    for quantidade in quantidades:
        cliente.carrinho.adicionar_item(produto, quantidade)
    return cliente


def _produto(infra, estoque: int = 10) -> Produto:
    produto = Produto("Notebook", 3500.0, estoque, Categoria("Informática"))
    infra.produtos.adicionar(produto)
    return produto


class TestDarBaixaNoEstoque:

    def test_reduz_o_estoque_pela_quantidade_vendida(self, infra) -> None:
        produto = _produto(infra)
        maria = _cliente_com(produto, 3)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        DarBaixaNoEstoque(infra.produtos).atualizar(infra.pedidos.obter(pedido.id), maria)
        assert infra.produtos.obter(produto.id).quantidade_estoque == 7

    def test_dois_itens_do_mesmo_produto_somam_a_baixa(self, infra) -> None:
        produto = _produto(infra)
        maria = _cliente_com(produto, 2, 3)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        DarBaixaNoEstoque(infra.produtos).atualizar(infra.pedidos.obter(pedido.id), maria)
        assert infra.produtos.obter(produto.id).quantidade_estoque == 5

    def test_estoque_insuficiente_falha(self, infra) -> None:
        produto = _produto(infra, estoque=1)
        maria = _cliente_com(produto, 2)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        with pytest.raises(EstoqueInsuficienteError):
            DarBaixaNoEstoque(infra.produtos).atualizar(infra.pedidos.obter(pedido.id), maria)


class TestNotificarClienteDoPagamento:

    def test_envia_a_mensagem_de_pagamento_confirmado(self) -> None:
        from ecommerce.aplicacao.notificacao import Notificacao
        from ecommerce.dominio.criador_pagamento import CriadorPagamento

        enviadas: list[str] = []

        class Espia(Notificacao):
            def enviar(self, destinatario: str, mensagem: str) -> None:
                enviadas.append(mensagem)

        class Fabrica:
            def criar(self, canal: object) -> Notificacao:
                return Espia()

        produto = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
        maria = _cliente_com(produto, 1)
        pedido = maria.finalizar_compra()
        pedido.confirmar_pagamento(CriadorPagamento())

        NotificarClienteDoPagamento(ServicoNotificacaoPedido(Fabrica())).atualizar(pedido, maria)

        assert len(enviadas) == 1
        assert "pagamento" in enviadas[0]
