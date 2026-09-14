from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.entrega import Entrega
from ecommerce.expedidor import Expedidor, ExpedidorLojaCentral
from ecommerce.notificacao import Notificacao
from ecommerce.pagamento import PagamentoPix
from ecommerce.pedido import Pedido
from ecommerce.produto import Produto
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
    """Com tudo injetado, o servico e testavel sem colaboradores reais."""

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.espia = NotificacaoEspia()
        self.servico = ServicoPedido(
            criador_pagamento=CriadorPagamento(),
            expedidor=ExpedidorLojaCentral(),
            servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacaoFake(self.espia)),
        )
        self.cliente = Cliente("Maria", "maria@email.com")

    def _pedido(self) -> Pedido:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        return pedido

    def test_pagar_confirma_o_pedido_e_notifica(self) -> None:
        pedido = self._pedido()
        self.servico.pagar(pedido, self.cliente)
        assert pedido.status == "pago"
        assert isinstance(pedido.pagamento, PagamentoPix)
        assert len(self.espia.enviadas) == 1

    def test_despachar_envia_o_pedido_e_notifica(self) -> None:
        pedido = self._pedido()
        self.servico.pagar(pedido, self.cliente)
        entrega = self.servico.despachar(pedido, self.cliente)
        assert isinstance(entrega, Entrega)
        assert pedido.status == "enviado"
        assert len(self.espia.enviadas) == 2

    def test_colaboradores_podem_ser_trocados_sem_tocar_no_servico(self) -> None:
        class ExpedidorFake(Expedidor):
            def __init__(self) -> None:
                self.chamado = False

            def criar_entrega(self, pedido: Pedido) -> Entrega:
                from ecommerce.entrega import EntregaCorreios

                self.chamado = True
                return EntregaCorreios(pedido, "FAKE-1")

        expedidor_fake = ExpedidorFake()
        servico = ServicoPedido(
            criador_pagamento=CriadorPagamento(),
            expedidor=expedidor_fake,
            servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacaoFake(self.espia)),
        )
        pedido = self._pedido()
        servico.pagar(pedido, self.cliente)
        servico.despachar(pedido, self.cliente)
        assert expedidor_fake.chamado is True
