import pytest

from ecommerce.aplicacao.cadastrar_produto import CadastrarProduto
from ecommerce.aplicacao.despachar_pedido import DespacharPedido
from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.observadores.notificar_cliente_do_pagamento import (
    NotificarClienteDoPagamento,
)
from ecommerce.aplicacao.pagar_pedido import PagarPedido
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.entrega import Entrega, EntregaCorreios
from ecommerce.dominio.expedidor import Expedidor
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import PedidoNaoEncontradoError
from ecommerce.aplicacao.notificacao import Notificacao


class NotificacaoEspia(Notificacao):
    def __init__(self) -> None:
        self.enviadas: list[tuple[str, str]] = []

    def enviar(self, destinatario: str, mensagem: str) -> None:
        self.enviadas.append((destinatario, mensagem))


class CriadorNotificacaoFake:
    def __init__(self, notificacao: Notificacao) -> None:
        self._notificacao = notificacao

    def criar(self, canal: object) -> Notificacao:
        return self._notificacao


class ExpedidorFake(Expedidor):
    def __init__(self) -> None:
        self.chamado = False

    def criar_entrega(self, pedido: Pedido) -> Entrega:
        self.chamado = True
        return EntregaCorreios(pedido, "FAKE-1")


@pytest.fixture
def espia() -> NotificacaoEspia:
    return NotificacaoEspia()


@pytest.fixture
def servico_notificacao(espia: NotificacaoEspia) -> ServicoNotificacaoPedido:
    return ServicoNotificacaoPedido(CriadorNotificacaoFake(espia))


@pytest.fixture
def maria(infra) -> Cliente:
    notebook = CadastrarProduto(infra.produtos).executar("Notebook", 3500.0, 10, "Informática")
    cliente = Cliente("Maria", "maria@email.com")
    cliente.carrinho = Carrinho()
    cliente.carrinho.adicionar_item(notebook, 1)
    return cliente


class TestCadastrarProduto:

    def test_produto_cadastrado_fica_disponivel_no_repositorio(self, infra) -> None:
        produto = CadastrarProduto(infra.produtos).executar("Mouse", 150.0, 20, "Informática")
        assert infra.produtos.obter(produto.id).nome == "Mouse"


class TestFinalizarCompra:

    def test_guarda_o_pedido_e_esvazia_o_carrinho(self, infra, maria) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        assert infra.pedidos.obter(pedido.id).quantidade_itens() == 1
        assert maria.carrinho.quantidade_itens() == 0


class TestPagarPedido:

    def test_confirma_o_pagamento_e_guarda(self, infra, maria) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        PagarPedido(infra.pedidos, CriadorPagamento()).executar(pedido.id, maria)
        assert infra.pedidos.obter(pedido.id).status == "pago"

    def test_avisa_o_cliente_quando_o_observador_de_notificacao_esta_inscrito(
        self, infra, maria, espia, servico_notificacao
    ) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        caso = PagarPedido(infra.pedidos, CriadorPagamento())
        caso.adicionar_observador(NotificarClienteDoPagamento(servico_notificacao))
        caso.executar(pedido.id, maria)
        assert len(espia.enviadas) == 1

    def test_pedido_inexistente_falha(self, infra, maria) -> None:
        caso = PagarPedido(infra.pedidos, CriadorPagamento())
        with pytest.raises(PedidoNaoEncontradoError):
            caso.executar(99, maria)


class TestDespacharPedido:

    def test_envia_guarda_e_notifica(self, infra, maria, espia, servico_notificacao) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        PagarPedido(infra.pedidos, CriadorPagamento()).executar(pedido.id, maria)
        expedidor = ExpedidorFake()
        DespacharPedido(infra.pedidos, expedidor, servico_notificacao).executar(pedido.id, maria)
        assert expedidor.chamado is True
        assert infra.pedidos.obter(pedido.id).status == "enviado"
        assert len(espia.enviadas) == 1
