"""Ponto de partida do programa: `python main.py` roda tudo.

    python main.py                         todos os cenarios, com dados fixos
    python main.py --cenario compra        so o cenario da compra
    python main.py menu                    menu de terminal
    python main.py menu --banco loja.db    menu com os dados guardados em arquivo
"""

import argparse
from typing import Callable

from ecommerce.composicao import montar_aplicacao
from ecommerce.entrada.cenario import CENARIOS
from ecommerce.entrada.menu import Menu, preparar_produtos


def main(
    argv: list[str] | None = None,
    entrada: Callable[[str], str] = input,
    saida: Callable[[str], None] = print,
) -> None:
    parser = argparse.ArgumentParser(description="E-Commerce: cenarios fixos ou menu de terminal.")
    parser.add_argument(
        "modo", nargs="?", choices=["cenario", "menu"], default="cenario",
        help="o que executar (padrao: cenario)",
    )
    parser.add_argument("--armazenamento", choices=["memoria", "sqlite"], default="sqlite")
    parser.add_argument("--banco", default=":memory:", help="arquivo SQLite (padrao: memoria)")
    parser.add_argument("--cenario", choices=[*CENARIOS, "todos"], default="todos")
    args = parser.parse_args(argv)

    if args.modo == "menu":
        app = montar_aplicacao(args.armazenamento, args.banco)
        preparar_produtos(app)
        Menu(app, entrada, saida).executar()
        return

    nomes = list(CENARIOS) if args.cenario == "todos" else [args.cenario]
    for nome in nomes:
        # Cada cenario recebe um sistema novo, montado do zero.
        app = montar_aplicacao(args.armazenamento, args.banco)
        CENARIOS[nome](app, saida)
        saida("")


if __name__ == "__main__":
    main()
