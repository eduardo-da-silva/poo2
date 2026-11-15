import ast
from pathlib import Path

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


def test_aplicacao_nao_conhece_a_infraestrutura() -> None:
    assert "infraestrutura" not in _camadas_importadas("aplicacao")


def test_infraestrutura_so_depende_de_dominio_e_aplicacao() -> None:
    assert _camadas_importadas("infraestrutura") <= {"dominio", "aplicacao", "infraestrutura"}


def test_nao_ha_modulos_soltos_alem_da_raiz_de_composicao() -> None:
    for arquivo in RAIZ.glob("*.py"):
        if arquivo.name in ("__init__.py", "composicao.py"):
            continue
        raise AssertionError(f"Modulo solto fora das camadas: {arquivo.name}")


def test_entrada_nao_conhece_a_infraestrutura() -> None:
    # A entrada usa a raiz de composicao, que e quem conhece as implementacoes.
    assert "infraestrutura" not in _camadas_importadas("entrada")


def test_nenhuma_camada_interna_importa_a_entrada() -> None:
    for camada in ("dominio", "aplicacao", "infraestrutura"):
        assert "entrada" not in _camadas_importadas(camada), camada
