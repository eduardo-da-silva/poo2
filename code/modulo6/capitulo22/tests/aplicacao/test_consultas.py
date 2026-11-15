import pytest

from ecommerce.aplicacao.cadastrar_produto import CadastrarProduto
from ecommerce.aplicacao.consultar_pedido import ConsultarPedido
from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.listar_produtos import ListarProdutos
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.repositorio_pedido import PedidoNaoEncontradoError


class TestListarProdutos:

    def test_loja_vazia_devolve_lista_vazia(self, infra) -> None:
        assert ListarProdutos(infra.produtos).executar() == []

    def test_devolve_os_produtos_cadastrados(self, infra) -> None:
        cadastrar = CadastrarProduto(infra.produtos)
        cadastrar.executar("Notebook", 3500.0, 10, "Informática")
        cadastrar.executar("Mouse", 150.0, 20, "Informática")
        nomes = [p.nome for p in ListarProdutos(infra.produtos).executar()]
        assert nomes == ["Notebook", "Mouse"]


class TestConsultarPedido:

    def test_devolve_o_pedido_guardado(self, infra) -> None:
        notebook = CadastrarProduto(infra.produtos).executar("Notebook", 3500.0, 10, "Informática")
        maria = Cliente("Maria", "maria@email.com")
        maria.carrinho = Carrinho()
        maria.carrinho.adicionar_item(notebook, 1)
        pedido = FinalizarCompra(infra.pedidos).executar(maria)
        consultado = ConsultarPedido(infra.pedidos).executar(pedido.id)
        assert consultado.id == pedido.id
        assert consultado.status == "criado"

    def test_pedido_inexistente_falha(self, infra) -> None:
        with pytest.raises(PedidoNaoEncontradoError):
            ConsultarPedido(infra.pedidos).executar(99)
