import pytest

from ecommerce.composicao import montar_aplicacao
from ecommerce.entrada.menu import Menu, preparar_produtos


class Roteiro:
    """Uma sessao de terminal escrita de antemao: cada chamada devolve a proxima resposta."""

    def __init__(self, *respostas: str) -> None:
        self._respostas = iter([*respostas, "0"])

    def __call__(self, pergunta: str) -> str:
        return next(self._respostas)


def _rodar(app, *respostas: str) -> list[str]:
    linhas: list[str] = []
    Menu(app, entrada=Roteiro(*respostas), saida=linhas.append).executar()
    return linhas


@pytest.fixture
def app():
    app = montar_aplicacao("memoria", registrar=lambda linha: None)
    preparar_produtos(app)
    return app


def test_sair_encerra_o_menu(app) -> None:
    assert _rodar(app)[-1] == "Ate logo."


def test_listar_produtos_mostra_o_catalogo(app) -> None:
    linhas = _rodar(app, "1")
    assert "1. Notebook - R$ 3500.00 (estoque 5)" in linhas


def test_fluxo_completo_pelo_menu(app) -> None:
    linhas = _rodar(app, "2", "1", "2", "3", "4", "1", "5", "1", "6", "1")
    assert "2 x Notebook no carrinho." in linhas
    assert "Pedido 1 criado: R$ 7000.00" in linhas
    assert "Pagamento do pedido 1 confirmado." in linhas
    assert any(linha.startswith("Pedido 1 enviado. Rastreio:") for linha in linhas)
    assert "Pedido 1: enviado, 1 item(ns), R$ 7000.00" in linhas


def test_pagar_pelo_menu_da_baixa_no_estoque(app) -> None:
    _rodar(app, "2", "1", "2", "3", "4", "1")
    assert app.listar_produtos.executar()[0].quantidade_estoque == 3


def test_opcao_invalida_nao_derruba_o_menu(app) -> None:
    linhas = _rodar(app, "9")
    assert "Opcao invalida." in linhas
    assert linhas[-1] == "Ate logo."


def test_texto_no_lugar_de_numero_vira_mensagem(app) -> None:
    assert "Erro: digite um numero inteiro" in _rodar(app, "4", "abc")


def test_pedido_inexistente_vira_mensagem(app) -> None:
    assert "Erro: Pedido 99 nao encontrado" in _rodar(app, "6", "99")


def test_produto_inexistente_vira_mensagem(app) -> None:
    assert "Erro: Produto 99 nao encontrado" in _rodar(app, "2", "99", "1")


def test_finalizar_com_carrinho_vazio_vira_mensagem(app) -> None:
    assert "Erro: Carrinho vazio" in _rodar(app, "3")


def test_quantidade_invalida_vira_mensagem_do_dominio(app) -> None:
    assert "Erro: Quantidade deve ser positiva" in _rodar(app, "2", "1", "0")


def test_auditoria_aparece_depois_de_pagar(app) -> None:
    linhas = _rodar(app, "2", "1", "1", "3", "4", "1", "7")
    assert "PedidoPago: pedido 1, cliente Maria" in linhas


def test_preparar_produtos_nao_duplica_o_catalogo(app) -> None:
    preparar_produtos(app)
    assert len(app.listar_produtos.executar()) == 3
