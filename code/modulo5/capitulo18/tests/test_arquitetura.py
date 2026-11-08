import ast
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent / "ecommerce"


def _camadas_importadas(camada: str) -> set[str]:
    """Camadas do ecommerce que os arquivos de `camada` importam."""
    importadas: set[str] = set()
    for arquivo in (RAIZ / camada).rglob("*.py"):
        for no in ast.walk(ast.parse(arquivo.read_text())):
            if isinstance(no, ast.ImportFrom) and no.module:
                partes = no.module.split(".")
                if partes[0] == "ecommerce" and len(partes) > 1:
                    importadas.add(partes[1])
    return importadas


def test_dominio_nao_conhece_as_outras_camadas() -> None:
    assert not _camadas_importadas("dominio") & {"aplicacao", "infraestrutura"}


@pytest.mark.xfail(
    strict=True,
    reason="divida visivel: ServicoNotificacaoPedido ainda importa a factory concreta",
)
def test_aplicacao_nao_conhece_a_infraestrutura() -> None:
    assert "infraestrutura" not in _camadas_importadas("aplicacao")
