import sqlite3
from dataclasses import dataclass

import pytest

from ecommerce.esquema_sqlite import criar_esquema
from ecommerce.repositorio_pedido import RepositorioPedido
from ecommerce.repositorio_pedido_memoria import RepositorioPedidoMemoria
from ecommerce.repositorio_pedido_sqlite import RepositorioPedidoSQLite
from ecommerce.repositorio_produto import RepositorioProduto
from ecommerce.repositorio_produto_memoria import RepositorioProdutoMemoria
from ecommerce.repositorio_produto_sqlite import RepositorioProdutoSQLite


@dataclass
class Infra:
    produtos: RepositorioProduto
    pedidos: RepositorioPedido


@pytest.fixture(params=["memoria", "sqlite"])
def infra(request: pytest.FixtureRequest) -> Infra:
    """Um unico contrato, varias implementacoes: os testes rodam em todas."""
    if request.param == "memoria":
        return Infra(RepositorioProdutoMemoria(), RepositorioPedidoMemoria())
    conexao = sqlite3.connect(":memory:")
    criar_esquema(conexao)
    produtos = RepositorioProdutoSQLite(conexao)
    return Infra(produtos, RepositorioPedidoSQLite(conexao, produtos))
