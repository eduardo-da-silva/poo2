import sqlite3
from dataclasses import dataclass

from ecommerce.aplicacao.cadastrar_produto import CadastrarProduto
from ecommerce.aplicacao.despachar_pedido import DespacharPedido
from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.observadores.dar_baixa_no_estoque import DarBaixaNoEstoque
from ecommerce.aplicacao.observadores.notificar_cliente_do_pagamento import (
    NotificarClienteDoPagamento,
)
from ecommerce.aplicacao.pagar_pedido import PagarPedido
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.expedidor import ExpedidorLojaCentral
from ecommerce.dominio.repositorio_produto import RepositorioProduto
from ecommerce.infraestrutura.criador_notificacao import CriadorNotificacao
from ecommerce.infraestrutura.esquema_sqlite import criar_esquema
from ecommerce.infraestrutura.repositorio_pedido_memoria import RepositorioPedidoMemoria
from ecommerce.infraestrutura.repositorio_pedido_sqlite import RepositorioPedidoSQLite
from ecommerce.infraestrutura.repositorio_produto_memoria import RepositorioProdutoMemoria
from ecommerce.infraestrutura.repositorio_produto_sqlite import RepositorioProdutoSQLite


@dataclass
class Aplicacao:
    produtos: RepositorioProduto
    cadastrar_produto: CadastrarProduto
    finalizar_compra: FinalizarCompra
    pagar_pedido: PagarPedido
    despachar_pedido: DespacharPedido


def montar_aplicacao(armazenamento: str = "sqlite", caminho_banco: str = ":memory:") -> Aplicacao:
    """Raiz de composicao: o unico lugar que conhece as tres camadas.

    Escolher onde os dados ficam e uma decisao de montagem, nao de dominio.
    """
    if armazenamento == "memoria":
        repositorio_produto = RepositorioProdutoMemoria()
        repositorio_pedido = RepositorioPedidoMemoria()
    elif armazenamento == "sqlite":
        conexao = sqlite3.connect(caminho_banco)
        criar_esquema(conexao)
        repositorio_produto = RepositorioProdutoSQLite(conexao)
        repositorio_pedido = RepositorioPedidoSQLite(conexao, repositorio_produto)
    else:
        raise ValueError(f"Armazenamento desconhecido: {armazenamento}")
    servico_notificacao = ServicoNotificacaoPedido(CriadorNotificacao())

    # Quem reage a um pagamento e decidido aqui, na montagem, e nao dentro do caso de uso.
    pagar_pedido = PagarPedido(repositorio_pedido, CriadorPagamento())
    pagar_pedido.adicionar_observador(NotificarClienteDoPagamento(servico_notificacao))
    pagar_pedido.adicionar_observador(DarBaixaNoEstoque(repositorio_produto))

    return Aplicacao(
        produtos=repositorio_produto,
        cadastrar_produto=CadastrarProduto(repositorio_produto),
        finalizar_compra=FinalizarCompra(repositorio_pedido),
        pagar_pedido=pagar_pedido,
        despachar_pedido=DespacharPedido(
            repositorio_pedido, ExpedidorLojaCentral(), servico_notificacao
        ),
    )


if __name__ == "__main__":
    from ecommerce.dominio.carrinho import Carrinho
    from ecommerce.dominio.cliente import Cliente

    app = montar_aplicacao()
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")

    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)
    app.despachar_pedido.executar(pedido.id, maria)
    print(f"Pedido {pedido.id} despachado.")
