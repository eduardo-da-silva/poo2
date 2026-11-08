from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.forma_pagamento import FormaPagamento
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class PagarPedido:
    """Caso de uso: confirmar o pagamento de um pedido e avisar o cliente."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        criador_pagamento: CriadorPagamento,
        servico_notificacao: ServicoNotificacaoPedido,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._criador_pagamento = criador_pagamento
        self._servico_notificacao = servico_notificacao

    def executar(
        self,
        pedido_id: int,
        cliente: Cliente,
        forma: FormaPagamento = FormaPagamento.PIX,
        **dados: object,
    ) -> None:
        pedido = self._repositorio_pedido.obter(pedido_id)
        pedido.confirmar_pagamento(self._criador_pagamento, forma, **dados)
        self._repositorio_pedido.atualizar(pedido)
        self._servico_notificacao.pedido_pago(pedido, cliente)
