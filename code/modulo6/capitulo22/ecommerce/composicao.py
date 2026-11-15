import logging
import sqlite3
from dataclasses import dataclass
from typing import Callable

from ecommerce.aplicacao.cadastrar_produto import CadastrarProduto
from ecommerce.aplicacao.caso_de_uso import CasoDeUso
from ecommerce.aplicacao.decoradores import ComLog, ComTempo
from ecommerce.aplicacao.barramento_eventos import BarramentoEventos
from ecommerce.aplicacao.despachar_pedido import DespacharPedido
from ecommerce.aplicacao.finalizar_compra import FinalizarCompra
from ecommerce.aplicacao.manipuladores.dar_baixa_no_estoque import DarBaixaNoEstoque
from ecommerce.aplicacao.manipuladores.notificar_cliente import (
    NotificarClienteDoEnvio,
    NotificarClienteDoPagamento,
)
from ecommerce.aplicacao.manipuladores.registrar_auditoria import RegistrarAuditoria
from ecommerce.aplicacao.pagar_pedido import PagarPedido
from ecommerce.aplicacao.registro_auditoria import RegistroAuditoria
from ecommerce.aplicacao.servico_notificacao_pedido import ServicoNotificacaoPedido
from ecommerce.dominio.criador_pagamento import CriadorPagamento
from ecommerce.dominio.eventos import PedidoDespachado, PedidoPago
from ecommerce.dominio.expedidor import ExpedidorLojaCentral
from ecommerce.dominio.repositorio_produto import RepositorioProduto
from ecommerce.infraestrutura.barramento_em_memoria import BarramentoEmMemoria
from ecommerce.infraestrutura.criador_notificacao import CriadorNotificacao
from ecommerce.infraestrutura.esquema_sqlite import criar_esquema
from ecommerce.infraestrutura.repositorio_pedido_memoria import RepositorioPedidoMemoria
from ecommerce.infraestrutura.repositorio_pedido_sqlite import RepositorioPedidoSQLite
from ecommerce.infraestrutura.repositorio_produto_memoria import RepositorioProdutoMemoria
from ecommerce.infraestrutura.registro_auditoria_em_memoria import RegistroAuditoriaEmMemoria
from ecommerce.infraestrutura.repositorio_produto_sqlite import RepositorioProdutoSQLite


@dataclass
class Aplicacao:
    produtos: RepositorioProduto
    cadastrar_produto: CasoDeUso
    finalizar_compra: CasoDeUso
    pagar_pedido: CasoDeUso
    despachar_pedido: CasoDeUso
    barramento: BarramentoEventos
    auditoria: RegistroAuditoria


def _observado(caso_de_uso: CasoDeUso, nome: str, registrar: Callable[[str], None]) -> CasoDeUso:
    """Embrulha o caso de uso com log e medicao de tempo, sem que ele saiba."""
    return ComLog(ComTempo(caso_de_uso, nome, registrar), nome, registrar)


def montar_aplicacao(
    armazenamento: str = "sqlite",
    caminho_banco: str = ":memory:",
    registrar: Callable[[str], None] | None = None,
) -> Aplicacao:
    """Raiz de composicao: o unico lugar que conhece as tres camadas.

    Escolher onde os dados ficam e uma decisao de montagem, nao de dominio.
    """
    if registrar is None:
        registrar = logging.getLogger("ecommerce").info
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
    barramento = BarramentoEmMemoria()
    auditoria = RegistroAuditoriaEmMemoria()

    # Quem reage a cada fato e decidido aqui, na montagem. Os casos de uso so anunciam.
    barramento.inscrever(PedidoPago, NotificarClienteDoPagamento(servico_notificacao))
    barramento.inscrever(PedidoPago, DarBaixaNoEstoque(repositorio_produto))
    barramento.inscrever(PedidoPago, RegistrarAuditoria(auditoria))
    barramento.inscrever(PedidoDespachado, NotificarClienteDoEnvio(servico_notificacao))
    barramento.inscrever(PedidoDespachado, RegistrarAuditoria(auditoria))

    return Aplicacao(
        produtos=repositorio_produto,
        cadastrar_produto=_observado(
            CadastrarProduto(repositorio_produto), "CadastrarProduto", registrar
        ),
        finalizar_compra=_observado(
            FinalizarCompra(repositorio_pedido), "FinalizarCompra", registrar
        ),
        pagar_pedido=_observado(
            PagarPedido(repositorio_pedido, CriadorPagamento(), barramento),
            "PagarPedido",
            registrar,
        ),
        despachar_pedido=_observado(
            DespacharPedido(repositorio_pedido, ExpedidorLojaCentral(), barramento),
            "DespacharPedido",
            registrar,
        ),
        barramento=barramento,
        auditoria=auditoria,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
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
    print("Auditoria:", app.auditoria.entradas())
