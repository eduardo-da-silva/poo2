import pytest

from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.observador_de_pagamento import ObservadorDePagamento
from ecommerce.aplicacao.pagar_pedido import PagarPedido
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.categoria import Categoria
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.produto import Produto


class ObservadorEspia(ObservadorDePagamento):
    def __init__(self, nome: str, ordem: list[str]) -> None:
        self.nome = nome
        self.recebidos: list[tuple[object, object]] = []
        self._ordem = ordem

    def atualizar(self, pedido, cliente) -> None:
        self._ordem.append(self.nome)
        self.recebidos.append((pedido, cliente))


class ObservadorQueFalha(ObservadorDePagamento):
    def atualizar(self, pedido, cliente) -> None:
        raise RuntimeError("falhei")


@pytest.fixture
def ordem() -> list[str]:
    return []


@pytest.fixture
def cenario(infra):
    produto = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    infra.produtos.adicionar(produto)
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(produto, 1)
    pedido = FinalizarCompra(infra.pedidos).executar(maria)
    caso = PagarPedido(infra.pedidos, CriadorPagamento())
    return caso, pedido, maria


class TestObservadoresDoPagamento:

    def test_observador_inscrito_recebe_pedido_e_cliente(self, cenario, ordem) -> None:
        caso, pedido, maria = cenario
        espia = ObservadorEspia("a", ordem)
        caso.adicionar_observador(espia)
        caso.executar(pedido.id, maria)
        assert len(espia.recebidos) == 1
        pedido_recebido, cliente_recebido = espia.recebidos[0]
        assert pedido_recebido.id == pedido.id
        assert pedido_recebido.status == "pago"
        assert cliente_recebido is maria

    def test_observadores_sao_avisados_na_ordem_de_inscricao(self, cenario, ordem) -> None:
        caso, pedido, maria = cenario
        caso.adicionar_observador(ObservadorEspia("primeiro", ordem))
        caso.adicionar_observador(ObservadorEspia("segundo", ordem))
        caso.executar(pedido.id, maria)
        assert ordem == ["primeiro", "segundo"]

    def test_observador_removido_nao_e_mais_avisado(self, cenario, ordem) -> None:
        caso, pedido, maria = cenario
        espia = ObservadorEspia("a", ordem)
        caso.adicionar_observador(espia)
        caso.remover_observador(espia)
        caso.executar(pedido.id, maria)
        assert espia.recebidos == []

    def test_sem_observadores_o_pagamento_funciona(self, cenario, infra) -> None:
        caso, pedido, maria = cenario
        caso.executar(pedido.id, maria)
        assert infra.pedidos.obter(pedido.id).status == "pago"

    def test_observador_que_falha_impede_os_seguintes(self, cenario, infra, ordem) -> None:
        # Divida visivel: o Observer simples nao isola uma reacao da outra.
        caso, pedido, maria = cenario
        depois = ObservadorEspia("depois", ordem)
        caso.adicionar_observador(ObservadorQueFalha())
        caso.adicionar_observador(depois)
        with pytest.raises(RuntimeError):
            caso.executar(pedido.id, maria)
        assert depois.recebidos == []
        assert infra.pedidos.obter(pedido.id).status == "pago"
