import pytest

from main import main
from tests.entrada.roteiro import Roteiro


def _rodar(*argv: str, entrada=None) -> list[str]:
    linhas: list[str] = []
    main(list(argv), entrada=entrada or Roteiro(), saida=linhas.append)
    return linhas


def test_sem_argumentos_roda_todos_os_cenarios() -> None:
    texto = "\n".join(_rodar())
    assert "Cenario 1" in texto
    assert "Cenario 2" in texto


def test_cenario_escolhido_roda_so_ele() -> None:
    texto = "\n".join(_rodar("--cenario", "compra"))
    assert "Cenario 1" in texto
    assert "Cenario 2" not in texto


def test_cenarios_rodam_nas_duas_configuracoes_de_armazenamento() -> None:
    for armazenamento in ("memoria", "sqlite"):
        assert "Status apos despachar: enviado" in _rodar("--armazenamento", armazenamento)


def test_modo_menu_abre_o_menu_com_o_catalogo_inicial() -> None:
    linhas = _rodar("menu", entrada=Roteiro("1"))
    assert "1. Notebook - R$ 3500.00 (estoque 5)" in linhas
    assert linhas[-1] == "Ate logo."


def test_argumento_invalido_e_recusado() -> None:
    with pytest.raises(SystemExit):
        main(["--armazenamento", "nuvem"])
    with pytest.raises(SystemExit):
        main(["tabela"])


def test_menu_com_arquivo_guarda_os_dados_entre_duas_execucoes(tmp_path) -> None:
    banco = str(tmp_path / "loja.db")
    # Primeira execucao: poe um notebook no carrinho e finaliza a compra.
    _rodar("menu", "--banco", banco, entrada=Roteiro("2", "1", "1", "3"))
    # Segunda execucao: o programa e outro, mas o pedido e o catalogo continuam la.
    linhas = _rodar("menu", "--banco", banco, entrada=Roteiro("1", "6", "1"))
    assert "Pedido 1: criado, 1 item(ns), R$ 3500.00" in linhas
    assert len([l for l in linhas if l.endswith(")") and "estoque" in l]) == 3
