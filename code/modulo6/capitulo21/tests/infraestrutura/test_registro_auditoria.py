from ecommerce.infraestrutura.registro_auditoria_em_memoria import RegistroAuditoriaEmMemoria


def test_registra_as_entradas_na_ordem() -> None:
    registro = RegistroAuditoriaEmMemoria()
    registro.registrar("a")
    registro.registrar("b")
    assert registro.entradas() == ["a", "b"]


def test_entradas_devolve_uma_copia() -> None:
    registro = RegistroAuditoriaEmMemoria()
    registro.registrar("a")
    registro.entradas().append("intruso")
    assert registro.entradas() == ["a"]
