import pytest

from ecommerce.composicao import montar_aplicacao
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente


@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_aplicacao_montada_executa_o_fluxo_completo(armazenamento: str) -> None:
    app = montar_aplicacao(armazenamento)
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)
    entrega = app.despachar_pedido.executar(pedido.id, maria)

    assert entrega.pedido.status == "enviado"


def test_armazenamento_desconhecido_falha() -> None:
    with pytest.raises(ValueError):
        montar_aplicacao("nuvem")


@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_pagar_da_baixa_no_estoque(armazenamento: str) -> None:
    app = montar_aplicacao(armazenamento)
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 2)

    pedido = app.finalizar_compra.executar(maria)
    assert app.produtos.obter(notebook.id).quantidade_estoque == 10
    app.pagar_pedido.executar(pedido.id, maria)

    assert app.produtos.obter(notebook.id).quantidade_estoque == 8


def test_fluxo_completo_deixa_a_auditoria_registrada() -> None:
    app = montar_aplicacao("memoria")
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)
    app.despachar_pedido.executar(pedido.id, maria)

    assert app.auditoria.entradas() == [
        f"PedidoPago: pedido {pedido.id}, cliente Maria",
        f"PedidoDespachado: pedido {pedido.id}, cliente Maria",
    ]


def test_nova_reacao_entra_sem_tocar_nos_casos_de_uso() -> None:
    # A prova do modulo: so a montagem muda.
    from ecommerce.dominio.eventos import PedidoPago

    app = montar_aplicacao("memoria")
    avisos: list[str] = []
    app.barramento.inscrever(PedidoPago, lambda evento: avisos.append("financeiro avisado"))
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)

    assert avisos == ["financeiro avisado"]


@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_falha_na_baixa_de_estoque_nao_desfaz_o_pagamento_nem_impede_as_outras_reacoes(
    armazenamento: str,
) -> None:
    app = montar_aplicacao(armazenamento, registrar=lambda linha: None)
    ultimo = app.cadastrar_produto.executar("Notebook", 3500.0, 1, "Informática")
    ana = Cliente("Ana", "ana@email.com")
    bia = Cliente("Bia", "bia@email.com")
    for cliente in (ana, bia):
        cliente.carrinho = Carrinho()
        cliente.carrinho.adicionar_item(ultimo, 1)
    pedido_da_ana = app.finalizar_compra.executar(ana)
    pedido_da_bia = app.finalizar_compra.executar(bia)

    app.pagar_pedido.executar(pedido_da_ana.id, ana)
    app.pagar_pedido.executar(pedido_da_bia.id, bia)  # a ultima unidade ja foi

    assert app.produtos.obter(ultimo.id).quantidade_estoque == 0
    entradas = app.auditoria.entradas()
    assert f"PedidoPago: pedido {pedido_da_bia.id}, cliente Bia" in entradas
    falhas = [e for e in entradas if e.startswith("FALHA")]
    assert len(falhas) == 1
    assert "DarBaixaNoEstoque" in falhas[0]
    assert "EstoqueInsuficienteError" in falhas[0]
