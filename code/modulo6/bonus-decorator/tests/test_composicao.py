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


def test_casos_de_uso_montados_deixam_log_sem_saber_disso() -> None:
    linhas: list[str] = []
    app = montar_aplicacao("memoria", registrar=linhas.append)
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)

    assert "PagarPedido: inicio" in linhas
    assert "PagarPedido: concluido" in linhas
    assert any(linha.startswith("PagarPedido: ") and linha.endswith(" ms") for linha in linhas)


def test_log_de_caso_de_uso_que_falha_registra_o_erro() -> None:
    linhas: list[str] = []
    app = montar_aplicacao("memoria", registrar=linhas.append)
    maria = Cliente("Maria", "maria@email.com")

    with pytest.raises(Exception):
        app.pagar_pedido.executar(99, maria)

    assert any(linha.startswith("PagarPedido: falhou") for linha in linhas)
