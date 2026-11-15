import pytest

from ecommerce.aplicacao.barramento_eventos import BarramentoEventos, Manipulador
from ecommerce.aplicacao.cadastrar_produto import CadastrarProduto
from ecommerce.aplicacao.despachar_pedido import DespacharPedido
from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.pagar_pedido import PagarPedido
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.entrega import Entrega, EntregaCorreios
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago
from ecommerce.dominio.expedidor import Expedidor
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import PedidoNaoEncontradoError


class BarramentoEspia(BarramentoEventos):
    def __init__(self) -> None:
        self.publicados: list[object] = []

    def inscrever(self, tipo_evento: type, manipulador: Manipulador) -> None:
        raise NotImplementedError

    def publicar(self, evento: object) -> None:
        self.publicados.append(evento)


class ExpedidorFake(Expedidor):
    def __init__(self) -> None:
        self.chamado = False

    def criar_entrega(self, pedido: Pedido) -> Entrega:
        self.chamado = True
        return EntregaCorreios(pedido, "FAKE-1")


@pytest.fixture
def barramento() -> BarramentoEspia:
    return BarramentoEspia()


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

    def test_confirma_o_pagamento_e_guarda(self, infra, maria, barramento) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        PagarPedido(infra.pedidos, CriadorPagamento(), barramento).executar(pedido.id, maria)
        assert infra.pedidos.obter(pedido.id).status == "pago"

    def test_publica_o_fato_depois_de_guardar(self, infra, maria, barramento) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        PagarPedido(infra.pedidos, CriadorPagamento(), barramento).executar(pedido.id, maria)
        assert len(barramento.publicados) == 1
        evento = barramento.publicados[0]
        assert isinstance(evento, PedidoPago)
        assert evento.pedido.id == pedido.id
        assert evento.cliente is maria

    def test_pedido_inexistente_falha_e_nao_publica(self, infra, maria, barramento) -> None:
        caso = PagarPedido(infra.pedidos, CriadorPagamento(), barramento)
        with pytest.raises(PedidoNaoEncontradoError):
            caso.executar(99, maria)
        assert barramento.publicados == []


class TestDespacharPedido:

    def test_envia_guarda_e_publica_o_fato(self, infra, maria, barramento) -> None:
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        PagarPedido(infra.pedidos, CriadorPagamento(), barramento).executar(pedido.id, maria)
        expedidor = ExpedidorFake()
        entrega = DespacharPedido(infra.pedidos, expedidor, barramento).executar(pedido.id, maria)
        assert expedidor.chamado is True
        assert infra.pedidos.obter(pedido.id).status == "enviado"
        evento = barramento.publicados[-1]
        assert isinstance(evento, PedidoDespachado)
        assert evento.entrega is entrega
