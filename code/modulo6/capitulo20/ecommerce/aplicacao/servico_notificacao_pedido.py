from ecommerce.aplicacao.notificacao import FabricaNotificacao


class ServicoNotificacaoPedido:

    def __init__(self, criador_notificacao: FabricaNotificacao) -> None:
        self._criador_notificacao = criador_notificacao

    def pedido_pago(self, pedido: "Pedido", cliente: "Cliente") -> None:
        mensagem = (
            f"Ola, {cliente.nome}. O pagamento do seu pedido foi confirmado. "
            f"Total: R$ {pedido.calcular_total():.2f}."
        )
        self._notificar(cliente, mensagem)

    def pedido_enviado(self, pedido: "Pedido", cliente: "Cliente") -> None:
        rastreio = pedido.entrega.codigo_rastreio if pedido.entrega is not None else "-"
        mensagem = (
            f"Ola, {cliente.nome}. Seu pedido foi enviado. "
            f"Codigo de rastreio: {rastreio}."
        )
        self._notificar(cliente, mensagem)

    def _notificar(self, cliente: "Cliente", mensagem: str) -> None:
        notificacao = self._criador_notificacao.criar(cliente.canal_preferido)
        notificacao.enviar(cliente.contato, mensagem)


if __name__ == "__main__":
    from ecommerce.aplicacao.notificacao import Notificacao
    from ecommerce.dominio.canal_notificacao import CanalNotificacao
    from ecommerce.dominio.carrinho import Carrinho
    from ecommerce.dominio.categoria import Categoria
    from ecommerce.dominio.cliente import Cliente
    from ecommerce.dominio.criador_pagamento import CriadorPagamento
    from ecommerce.dominio.expedidor import ExpedidorLojaCentral
    from ecommerce.dominio.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)

    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)
    pedido = maria.finalizar_compra()

    # A aplicacao nao conhece a infraestrutura: o demo usa uma notificacao propria.
    class NotificacaoNoConsole(Notificacao):
        def enviar(self, destinatario: str, mensagem: str) -> None:
            print(f"[{destinatario}] {mensagem}")

    class FabricaNoConsole:
        def criar(self, canal: CanalNotificacao) -> Notificacao:
            return NotificacaoNoConsole()

    servico = ServicoNotificacaoPedido(FabricaNoConsole())

    pedido.confirmar_pagamento(CriadorPagamento())
    servico.pedido_pago(pedido, maria)

    ExpedidorLojaCentral().despachar(pedido)
    servico.pedido_enviado(pedido, maria)
