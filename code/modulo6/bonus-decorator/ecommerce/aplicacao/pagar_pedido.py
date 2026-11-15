from ecommerce.aplicacao.barramento_eventos import BarramentoEventos
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.eventos import PedidoPago
from ecommerce.dominio.forma_pagamento import FormaPagamento
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class PagarPedido:
    """Caso de uso: confirmar o pagamento de um pedido e anunciar que ele aconteceu."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        criador_pagamento: CriadorPagamento,
        barramento: BarramentoEventos,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._criador_pagamento = criador_pagamento
        self._barramento = barramento

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
        self._barramento.publicar(PedidoPago(pedido, cliente))
