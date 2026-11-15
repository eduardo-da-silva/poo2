import pytest

from ecommerce.aplicacao.decoradores import ComLog, ComTempo


class CasoSoma:
    def executar(self, a: int, b: int = 0) -> int:
        return a + b


class CasoQueFalha:
    def executar(self) -> None:
        raise ValueError("deu ruim")


class RelogioFalso:
    """Devolve 1.0 na primeira leitura e 1.25 na segunda: 250 ms de diferenca."""

    def __init__(self) -> None:
        self._leituras = iter([1.0, 1.25])

    def __call__(self) -> float:
        return next(self._leituras)


class TestComLog:

    def test_registra_inicio_e_fim_e_devolve_o_resultado(self) -> None:
        linhas: list[str] = []
        caso = ComLog(CasoSoma(), "Soma", linhas.append)
        assert caso.executar(2, b=3) == 5
        assert linhas == ["Soma: inicio", "Soma: concluido"]

    def test_registra_a_falha_e_relanca_o_erro(self) -> None:
        linhas: list[str] = []
        caso = ComLog(CasoQueFalha(), "Falha", linhas.append)
        with pytest.raises(ValueError):
            caso.executar()
        assert linhas == ["Falha: inicio", "Falha: falhou (ValueError: deu ruim)"]


class TestComTempo:

    def test_registra_a_duracao_em_milissegundos(self) -> None:
        linhas: list[str] = []
        caso = ComTempo(CasoSoma(), "Soma", linhas.append, relogio=RelogioFalso())
        assert caso.executar(1, 1) == 2
        assert linhas == ["Soma: 250.0 ms"]

    def test_registra_a_duracao_mesmo_quando_falha(self) -> None:
        linhas: list[str] = []
        caso = ComTempo(CasoQueFalha(), "Falha", linhas.append, relogio=RelogioFalso())
        with pytest.raises(ValueError):
            caso.executar()
        assert linhas == ["Falha: 250.0 ms"]


class TestEmpilhando:

    def test_o_de_fora_envolve_o_de_dentro(self) -> None:
        linhas: list[str] = []
        caso = ComLog(
            ComTempo(CasoSoma(), "Soma", linhas.append, relogio=RelogioFalso()),
            "Soma",
            linhas.append,
        )
        assert caso.executar(2, 2) == 4
        assert linhas == ["Soma: inicio", "Soma: 250.0 ms", "Soma: concluido"]

    def test_a_ordem_do_empilhamento_muda_o_resultado(self) -> None:
        linhas: list[str] = []
        caso = ComTempo(
            ComLog(CasoSoma(), "Soma", linhas.append),
            "Soma",
            linhas.append,
            relogio=RelogioFalso(),
        )
        caso.executar(2, 2)
        assert linhas == ["Soma: inicio", "Soma: concluido", "Soma: 250.0 ms"]
