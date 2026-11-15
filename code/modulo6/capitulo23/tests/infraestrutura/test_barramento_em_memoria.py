from dataclasses import dataclass

import pytest

from ecommerce.infraestrutura.barramento_em_memoria import BarramentoEmMemoria


@dataclass(frozen=True)
class EventoA:
    valor: int


@dataclass(frozen=True)
class EventoB:
    valor: int


def test_manipulador_inscrito_recebe_o_evento_publicado() -> None:
    barramento = BarramentoEmMemoria()
    recebidos: list[object] = []
    barramento.inscrever(EventoA, recebidos.append)
    barramento.publicar(EventoA(1))
    assert recebidos == [EventoA(1)]


def test_manipulador_nao_recebe_eventos_de_outro_tipo() -> None:
    barramento = BarramentoEmMemoria()
    recebidos: list[object] = []
    barramento.inscrever(EventoA, recebidos.append)
    barramento.publicar(EventoB(1))
    assert recebidos == []


def test_manipuladores_sao_chamados_na_ordem_de_inscricao() -> None:
    barramento = BarramentoEmMemoria()
    ordem: list[str] = []
    barramento.inscrever(EventoA, lambda e: ordem.append("primeiro"))
    barramento.inscrever(EventoA, lambda e: ordem.append("segundo"))
    barramento.publicar(EventoA(1))
    assert ordem == ["primeiro", "segundo"]


def test_publicar_sem_ninguem_inscrito_nao_faz_nada() -> None:
    BarramentoEmMemoria().publicar(EventoA(1))


def test_um_manipulador_pode_ouvir_tipos_diferentes() -> None:
    barramento = BarramentoEmMemoria()
    recebidos: list[object] = []
    barramento.inscrever(EventoA, recebidos.append)
    barramento.inscrever(EventoB, recebidos.append)
    barramento.publicar(EventoA(1))
    barramento.publicar(EventoB(2))
    assert recebidos == [EventoA(1), EventoB(2)]


def _quebra(evento: object) -> None:
    raise RuntimeError("nao consegui")


def test_sem_ao_falhar_o_erro_sobe_e_os_seguintes_nao_rodam() -> None:
    barramento = BarramentoEmMemoria()
    recebidos: list[object] = []
    barramento.inscrever(EventoA, _quebra)
    barramento.inscrever(EventoA, recebidos.append)
    with pytest.raises(RuntimeError):
        barramento.publicar(EventoA(1))
    assert recebidos == []


def test_com_ao_falhar_os_seguintes_continuam() -> None:
    barramento = BarramentoEmMemoria(ao_falhar=lambda evento, manipulador, erro: None)
    recebidos: list[object] = []
    barramento.inscrever(EventoA, _quebra)
    barramento.inscrever(EventoA, recebidos.append)
    barramento.publicar(EventoA(1))
    assert recebidos == [EventoA(1)]


def test_ao_falhar_recebe_o_evento_o_manipulador_e_o_erro() -> None:
    falhas: list[tuple[object, object, Exception]] = []
    barramento = BarramentoEmMemoria(
        ao_falhar=lambda evento, manipulador, erro: falhas.append((evento, manipulador, erro))
    )
    barramento.inscrever(EventoA, _quebra)
    barramento.publicar(EventoA(7))
    evento, manipulador, erro = falhas[0]
    assert evento == EventoA(7)
    assert manipulador is _quebra
    assert str(erro) == "nao consegui"


def test_manipuladores_anteriores_a_falha_ja_rodaram() -> None:
    barramento = BarramentoEmMemoria()
    recebidos: list[object] = []
    barramento.inscrever(EventoA, recebidos.append)
    barramento.inscrever(EventoA, _quebra)
    with pytest.raises(RuntimeError):
        barramento.publicar(EventoA(1))
    assert recebidos == [EventoA(1)]
