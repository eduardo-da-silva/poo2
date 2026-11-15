import argparse
from typing import Callable

from ecommerce.composicao import Aplicacao, montar_aplicacao
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.produto import Produto

Saida = Callable[[str], None]


def _cliente_com(nome: str, email: str, *itens: tuple[Produto, int]) -> Cliente:
    cliente = Cliente(nome, email)
    cliente.carrinho = Carrinho()
    for produto, quantidade in itens:
        cliente.carrinho.adicionar_item(produto, quantidade)
    return cliente


def _mostrar_estoque(app: Aplicacao, saida: Saida, titulo: str) -> None:
    saida(f"{titulo}:")
    for produto in app.listar_produtos.executar():
        saida(f"  {produto.nome}: {produto.quantidade_estoque}")


def _mostrar_auditoria(app: Aplicacao, saida: Saida) -> None:
    saida("Auditoria:")
    for entrada in app.auditoria.entradas():
        saida(f"  {entrada}")


def cenario_compra(app: Aplicacao, saida: Saida = print) -> None:
    """Uma compra do inicio ao fim, com dados fixos."""
    saida("== Cenario 1: uma compra do inicio ao fim ==")
    notebook = app.cadastrar_produto.executar("Notebook", 3500.0, 5, "Informática")
    mouse = app.cadastrar_produto.executar("Mouse", 150.0, 20, "Informática")
    _mostrar_estoque(app, saida, "Estoque antes")

    maria = _cliente_com("Maria", "maria@email.com", (notebook, 1), (mouse, 2))
    pedido = app.finalizar_compra.executar(maria)
    saida(f"Maria finalizou a compra: pedido {pedido.id}, R$ {pedido.calcular_total():.2f}")

    app.pagar_pedido.executar(pedido.id, maria)
    saida(f"Status apos pagar: {app.consultar_pedido.executar(pedido.id).status}")
    app.despachar_pedido.executar(pedido.id, maria)
    saida(f"Status apos despachar: {app.consultar_pedido.executar(pedido.id).status}")

    _mostrar_estoque(app, saida, "Estoque depois")
    _mostrar_auditoria(app, saida)


def cenario_ultima_unidade(app: Aplicacao, saida: Saida = print) -> None:
    """Duas pessoas compram a ultima unidade: a segunda paga, e a baixa falha."""
    saida("== Cenario 2: duas pessoas, uma unica unidade ==")
    ultimo = app.cadastrar_produto.executar("Notebook", 3500.0, 1, "Informática")
    ana = _cliente_com("Ana", "ana@email.com", (ultimo, 1))
    bia = _cliente_com("Bia", "bia@email.com", (ultimo, 1))
    pedido_da_ana = app.finalizar_compra.executar(ana)
    pedido_da_bia = app.finalizar_compra.executar(bia)
    saida("Ana e Bia finalizaram a compra do mesmo notebook. Estoque: 1.")

    app.pagar_pedido.executar(pedido_da_ana.id, ana)
    app.pagar_pedido.executar(pedido_da_bia.id, bia)
    for pedido_id, nome in ((pedido_da_ana.id, "Ana"), (pedido_da_bia.id, "Bia")):
        saida(f"Pedido de {nome}: {app.consultar_pedido.executar(pedido_id).status}")

    _mostrar_estoque(app, saida, "Estoque depois")
    _mostrar_auditoria(app, saida)


CENARIOS = {"compra": cenario_compra, "ultima-unidade": cenario_ultima_unidade}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Roda cenarios fixos do E-Commerce.")
    parser.add_argument("--armazenamento", choices=["memoria", "sqlite"], default="sqlite")
    parser.add_argument("--banco", default=":memory:", help="arquivo SQLite (padrao: memoria)")
    parser.add_argument("--cenario", choices=[*CENARIOS, "todos"], default="todos")
    args = parser.parse_args(argv)

    nomes = list(CENARIOS) if args.cenario == "todos" else [args.cenario]
    for nome in nomes:
        app = montar_aplicacao(args.armazenamento, args.banco)
        CENARIOS[nome](app)
        print()


if __name__ == "__main__":
    main()
