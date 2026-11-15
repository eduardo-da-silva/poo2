from ecommerce.aplicacao.observador_de_pagamento import ObservadorDePagamento
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.forma_pagamento import FormaPagamento
from ecommerce.dominio.pedido import Pedido
from ecommerce.dominio.repositorio_pedido import RepositorioPedido


class PagarPedido:
    """Caso de uso: confirmar o pagamento de um pedido e avisar quem se inscreveu."""

    def __init__(
        self,
        repositorio_pedido: RepositorioPedido,
        criador_pagamento: CriadorPagamento,
    ) -> None:
        self._repositorio_pedido = repositorio_pedido
        self._criador_pagamento = criador_pagamento
        self._observadores: list[ObservadorDePagamento] = []

    def adicionar_observador(self, observador: ObservadorDePagamento) -> None:
        self._observadores.append(observador)

    def remover_observador(self, observador: ObservadorDePagamento) -> None:
        self._observadores.remove(observador)

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
        self._avisar_observadores(pedido, cliente)

    def _avisar_observadores(self, pedido: Pedido, cliente: Cliente) -> None:
        for observador in self._observadores:
            observador.atualizar(pedido, cliente)
