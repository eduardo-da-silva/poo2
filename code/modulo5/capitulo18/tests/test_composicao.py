from ecommerce.composicao import montar_aplicacao
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente


def test_aplicacao_montada_executa_o_fluxo_completo() -> None:
    app = montar_aplicacao()
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 10, "Informática")
    maria = Cliente("Maria", "maria@email.com")
    maria.carrinho = Carrinho()
    maria.carrinho.adicionar_item(notebook, 1)

    pedido = app.finalizar_compra.executar(maria)
    app.pagar_pedido.executar(pedido.id, maria)
    entrega = app.despachar_pedido.executar(pedido.id, maria)

    assert entrega.pedido.status == "enviado"
