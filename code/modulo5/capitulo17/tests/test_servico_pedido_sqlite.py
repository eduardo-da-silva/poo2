import sqlite3

from ecommerce.carrinho import Carrinho
from ecommerce.categoria import Categoria
from ecommerce.cliente import Cliente
from ecommerce.criador_pagamento import CriadorPagamento
from ecommerce.esquema_sqlite import criar_esquema
from ecommerce.expedidor import ExpedidorLojaCentral
from ecommerce.produto import Produto
from ecommerce.repositorio_pedido_sqlite import RepositorioPedidoSQLite
from ecommerce.repositorio_produto_sqlite import RepositorioProdutoSQLite
from ecommerce.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.servico_pedido import ServicoPedido
from tests.test_servico_pedido import CriadorNotificacaoFake, NotificacaoEspia


def test_mesmo_servico_funciona_com_sqlite_sem_nenhuma_mudanca() -> None:
    conexao = sqlite3.connect(":memory:")
    criar_esquema(conexao)
    produtos = RepositorioProdutoSQLite(conexao)
    pedidos = RepositorioPedidoSQLite(conexao, produtos)
    espia = NotificacaoEspia()
    servico = ServicoPedido(
        repositorio_pedido=pedidos,
        criador_pagamento=CriadorPagamento(),
        expedidor=ExpedidorLojaCentral(),
        servico_notificacao=ServicoNotificacaoPedido(CriadorNotificacaoFake(espia)),
    )

    notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    produtos.adicionar(notebook)
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = servico.finalizar_compra(maria)
    servico.pagar(pedido.id, maria)
    servico.despachar(pedido.id, maria)

    assert pedidos.obter(pedido.id).status == "enviado"
    assert len(espia.enviadas) == 2
