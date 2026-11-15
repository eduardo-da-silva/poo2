from typing import Callable

from ecommerce.aplicacao.barramento_eventos import BarramentoEventos, Manipulador

AoFalhar = Callable[[object, Manipulador, Exception], None]


class BarramentoEmMemoria(BarramentoEventos):
    """Entrega cada evento, na hora e no mesmo processo, a quem se inscreveu no seu tipo.

    Sem `ao_falhar`, o erro de um manipulador sobe para quem publicou e os manipuladores
    seguintes nao rodam. Com `ao_falhar`, o erro e entregue a essa funcao e os
    seguintes continuam: uma reacao que falha nao derruba as outras.
    """

    def __init__(self, ao_falhar: AoFalhar | None = None) -> None:
        self._manipuladores: dict[type, list[Manipulador]] = {}
        self._ao_falhar = ao_falhar

    def inscrever(self, tipo_evento: type, manipulador: Manipulador) -> None:
        self._manipuladores.setdefault(tipo_evento, []).append(manipulador)

    def publicar(self, evento: object) -> None:
        # Tipo exato: quem se inscreveu em PedidoPago nao recebe outros eventos.
        for manipulador in list(self._manipuladores.get(type(evento), [])):
            try:
                manipulador(evento)
            except Exception as erro:
                if self._ao_falhar is None:
                    raise
                self._ao_falhar(evento, manipulador, erro)


if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Ola:
        nome: str

    def quebra(evento: Ola) -> None:
        raise RuntimeError("nao consegui")

    def registrar(evento: object, manipulador: Manipulador, erro: Exception) -> None:
        print(f"Falha em {manipulador.__name__}: {erro}")

    barramento = BarramentoEmMemoria(ao_falhar=registrar)
    barramento.inscrever(Ola, quebra)
    barramento.inscrever(Ola, lambda evento: print(f"Ola, {evento.nome}!"))
    barramento.publicar(Ola("Maria"))
