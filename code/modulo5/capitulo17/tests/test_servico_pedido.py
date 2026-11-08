import pytest

from ecommerce.carrinho import Carrinho
from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.entrega import Entrega, EntregaCorreios
from ecommerce.expedidor import Expedidor, ExpedidorLojaCentral
from ecommerce.notificacao import Notificacao
from ecommerce.pagamento import PagamentoPix
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
from ecommerce.repositorio_pedido import PedidoNaoEncontradoError
from ecommerce.repositorio_pedido_memoria import RepositorioPedidoMemoria
from ecommerce.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.servico_pedido import ServicoPedido


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


class TestServicoPedido:
    """O servico recebe o repositorio e nao sabe onde os pedidos ficam guardados."""

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.espia = NotificacaoEspia()
        self.repositorio = RepositorioPedidoMemoria()
        self.servico = self._montar(ExpedidorLojaCentral())
        self.cliente = Cliente("Maria", "maria@email.com")
        self.cliente.carrinho = Carrinho()
        self.cliente.carrinho.adicionar_item(self.notebook, 1)

    def _montar(self, expedidor: Expedidor) -> ServicoPedido:
        return ServicoPedido(
            repositorio_pedido=self.repositorio,
            criador_pagamento=CriadorPagamento(),
            expedidor=expedidor,
            servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacaoFake(self.espia)),
        )

    def test_finalizar_compra_guarda_o_pedido_no_repositorio(self) -> None:
        pedido = self.servico.finalizar_compra(self.cliente)
        assert pedido.id is not None
        assert self.repositorio.obter(pedido.id) is pedido

    def test_pagar_confirma_o_pedido_e_notifica(self) -> None:
        pedido = self.servico.finalizar_compra(self.cliente)
        self.servico.pagar(pedido.id, self.cliente)
        guardado = self.repositorio.obter(pedido.id)
        assert guardado.status == "pago"
        assert isinstance(guardado.pagamento, PagamentoPix)
        assert len(self.espia.enviadas) == 1

    def test_despachar_envia_o_pedido_e_notifica(self) -> None:
        pedido = self.servico.finalizar_compra(self.cliente)
        self.servico.pagar(pedido.id, self.cliente)
        entrega = self.servico.despachar(pedido.id, self.cliente)
        assert isinstance(entrega, Entrega)
        assert self.repositorio.obter(pedido.id).status == "enviado"
        assert len(self.espia.enviadas) == 2

    def test_pagar_pedido_inexistente_falha(self) -> None:
        with pytest.raises(PedidoNaoEncontradoError):
            self.servico.pagar(99, self.cliente)

    def test_colaboradores_podem_ser_trocados_sem_tocar_no_servico(self) -> None:
        class ExpedidorFake(Expedidor):
            def __init__(self) -> None:
                self.chamado = False

            def criar_entrega(self, pedido: Pedido) -> Entrega:
                self.chamado = True
                return EntregaCorreios(pedido, "FAKE-1")

        expedidor_fake = ExpedidorFake()
        servico = self._montar(expedidor_fake)
        pedido = servico.finalizar_compra(self.cliente)
        servico.pagar(pedido.id, self.cliente)
        servico.despachar(pedido.id, self.cliente)
        assert expedidor_fake.chamado is True
