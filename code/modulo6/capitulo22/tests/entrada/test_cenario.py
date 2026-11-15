import pytest

from ecommerce.composicao import montar_aplicacao
from ecommerce.entrada.cenario import cenario_compra, cenario_ultima_unidade, main


@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_cenario_compra_conta_a_historia_do_inicio_ao_fim(armazenamento: str) -> None:
    linhas: list[str] = []
    cenario_compra(montar_aplicacao(armazenamento), linhas.append)
    texto = "\n".join(linhas)
    assert "Status apos pagar: pago" in texto
    assert "Status apos despachar: enviado" in texto
    assert "  Notebook: 4" in linhas  # estoque depois: 5 - 1
    assert "  Mouse: 18" in linhas  # estoque depois: 20 - 2
    assert "  PedidoPago: pedido 1, cliente Maria" in linhas


@pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
def test_cenario_ultima_unidade_mostra_a_falha_sem_derrubar_o_pagamento(
    armazenamento: str,
) -> None:
    linhas: list[str] = []
    app = montar_aplicacao(armazenamento, registrar=lambda linha: None)
    cenario_ultima_unidade(app, linhas.append)
    assert "Pedido de Ana: pago" in linhas
    assert "Pedido de Bia: pago" in linhas
    assert "  Notebook: 0" in linhas
    assert any(linha.startswith("  FALHA: DarBaixaNoEstoque") for linha in linhas)


def test_main_roda_todos_os_cenarios(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--armazenamento", "memoria", "--cenario", "compra"])
    assert "Cenario 1" in capsys.readouterr().out


def test_main_recusa_armazenamento_desconhecido() -> None:
    with pytest.raises(SystemExit):
        main(["--armazenamento", "nuvem"])
