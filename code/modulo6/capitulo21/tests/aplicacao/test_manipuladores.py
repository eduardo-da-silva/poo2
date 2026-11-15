import pytest

from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.manipuladores.dar_baixa_no_estoque import DarBaixaNoEstoque
from ecommerce.aplicacao.manipuladores.notificar_cliente import (
    NotificarClienteDoEnvio,
    NotificarClienteDoPagamento,
)
from ecommerce.aplicacao.manipuladores.registrar_auditoria import RegistrarAuditoria
from ecommerce.aplicacao.notificacao import Notificacao
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago
from ecommerce.dominio.expedidor import ExpedidorLojaCentral
from ecommerce.dominio.produto import EstoqueInsuficienteError, Produto
from ecommerce.infraestrutura.registro_auditoria_em_memoria import RegistroAuditoriaEmMemoria


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


class _NotificacaoEspia(Notificacao):
    def __init__(self) -> None:
        self.mensagens: list[str] = []

    def enviar(self, destinatario: str, mensagem: str) -> None:
        self.mensagens.append(mensagem)


class _Fabrica:
    def __init__(self, notificacao: Notificacao) -> None:
        self._notificacao = notificacao

    def criar(self, canal: object) -> Notificacao:
        return self._notificacao


@pytest.fixture
def espia() -> _NotificacaoEspia:
    return _NotificacaoEspia()


@pytest.fixture
def servico(espia: _NotificacaoEspia) -> ServicoNotificacaoPedido:
    return ServicoNotificacaoPedido(_Fabrica(espia))


@pytest.fixture
def pedido_pago():
    maria = _cliente_com(Produto("Notebook", 3500.0, 10, Categoria("Informática")), 1)
    pedido = maria.finalizar_compra()
    pedido.confirmar_pagamento(CriadorPagamento())
    return pedido, maria


class TestDarBaixaNoEstoque:

    def test_reduz_o_estoque_pela_quantidade_vendida(self, infra) -> None:
        produto = _produto(infra)
        maria = _cliente_com(produto, 3)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        DarBaixaNoEstoque(infra.produtos)(PedidoPago(infra.pedidos.obter(pedido.id), maria))
        assert infra.produtos.obter(produto.id).quantidade_estoque == 7

    def test_dois_itens_do_mesmo_produto_somam_a_baixa(self, infra) -> None:
        produto = _produto(infra)
        maria = _cliente_com(produto, 2, 3)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        DarBaixaNoEstoque(infra.produtos)(PedidoPago(infra.pedidos.obter(pedido.id), maria))
        assert infra.produtos.obter(produto.id).quantidade_estoque == 5

    def test_estoque_insuficiente_falha(self, infra) -> None:
        produto = _produto(infra, estoque=1)
        maria = _cliente_com(produto, 2)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        with pytest.raises(EstoqueInsuficienteError):
            DarBaixaNoEstoque(infra.produtos)(PedidoPago(infra.pedidos.obter(pedido.id), maria))


class TestNotificarCliente:

    def test_avisa_do_pagamento(self, servico, espia, pedido_pago) -> None:
        pedido, maria = pedido_pago
        NotificarClienteDoPagamento(servico)(PedidoPago(pedido, maria))
        assert len(espia.mensagens) == 1
        assert "pagamento" in espia.mensagens[0]

    def test_avisa_do_envio_com_o_rastreio(self, servico, espia, pedido_pago) -> None:
        pedido, maria = pedido_pago
        entrega = ExpedidorLojaCentral().despachar(pedido)
        NotificarClienteDoEnvio(servico)(PedidoDespachado(pedido, maria, entrega))
        assert len(espia.mensagens) == 1
        assert entrega.codigo_rastreio in espia.mensagens[0]


class TestRegistrarAuditoria:

    def test_registra_o_evento_de_pagamento(self, pedido_pago) -> None:
        pedido, maria = pedido_pago
        registro = RegistroAuditoriaEmMemoria()
        RegistrarAuditoria(registro)(PedidoPago(pedido, maria))
        assert registro.entradas() == [f"PedidoPago: pedido {pedido.id}, cliente Maria"]

    def test_o_mesmo_manipulador_serve_a_mais_de_um_tipo_de_evento(self, pedido_pago) -> None:
        pedido, maria = pedido_pago
        entrega = ExpedidorLojaCentral().despachar(pedido)
        registro = RegistroAuditoriaEmMemoria()
        registrar = RegistrarAuditoria(registro)
        registrar(PedidoPago(pedido, maria))
        registrar(PedidoDespachado(pedido, maria, entrega))
        assert [e.split(":")[0] for e in registro.entradas()] == ["PedidoPago", "PedidoDespachado"]
