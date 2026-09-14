from ecommerce.canal_notificacao import CanalNotificacao
from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.expedidor import ExpedidorLojaCentral
from ecommerce.notificacao import Notificacao
from ecommerce.produto import Produto
from ecommerce.pedido import Pedido
from ecommerce.servico_notificacao_pedido import ServicoNotificacaoPedido


class NotificacaoEspia(Notificacao):
    """Duble: registra o que seria enviado, em vez de enviar de verdade."""

    def __init__(self) -> None:
        self.enviadas: list[tuple[str, str]] = []

    def enviar(self, destinatario: str, mensagem: str) -> None:
        self.enviadas.append((destinatario, mensagem))


class CriadorNotificacaoFake:
    def __init__(self, notificacao: Notificacao) -> None:
        self._notificacao = notificacao
        self.canais_pedidos: list[CanalNotificacao] = []

    def criar(self, canal: CanalNotificacao) -> Notificacao:
        self.canais_pedidos.append(canal)
        return self._notificacao


class TestServicoNotificacaoPedido:

    def setup_method(self) -> None:
        self.cat = Categoria("Informática")
        self.notebook = Produto("Notebook", 3500.0, 10, self.cat)
        self.espia = NotificacaoEspia()
        self.criador_fake = CriadorNotificacaoFake(self.espia)
        self.servico = ServicoNotificacaoPedido(self.criador_fake)

    def _pedido_pago(self) -> Pedido:
        pedido = Pedido()
        pedido.adicionar_item(self.notebook, 1)
        pedido.confirmar_pagamento()
        return pedido

    def test_notifica_pagamento_confirmado(self) -> None:
        cliente = Cliente("Maria", "maria@email.com")
        self.servico.pedido_pago(self._pedido_pago(), cliente)
        destinatario, mensagem = self.espia.enviadas[0]
        assert destinatario == "maria@email.com"
        assert "pagamento" in mensagem.lower()

    def test_usa_o_canal_preferido_do_cliente(self) -> None:
        cliente = Cliente(
            "João", "joao@email.com", telefone="+55 47 90000-0000",
            canal_preferido=CanalNotificacao.SMS,
        )
        self.servico.pedido_pago(self._pedido_pago(), cliente)
        assert self.criador_fake.canais_pedidos == [CanalNotificacao.SMS]
        destinatario, _ = self.espia.enviadas[0]
        assert destinatario == "+55 47 90000-0000"

    def test_notifica_envio_com_codigo_de_rastreio(self) -> None:
        cliente = Cliente("Maria", "maria@email.com")
        pedido = self._pedido_pago()
        entrega = ExpedidorLojaCentral().despachar(pedido)
        self.servico.pedido_enviado(pedido, cliente)
        _, mensagem = self.espia.enviadas[0]
        assert entrega.codigo_rastreio in mensagem
