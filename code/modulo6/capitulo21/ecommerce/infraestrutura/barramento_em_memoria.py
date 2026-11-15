from ecommerce.aplicacao.barramento_eventos import BarramentoEventos, Manipulador


class BarramentoEmMemoria(BarramentoEventos):
    """Entrega cada evento, na hora e no mesmo processo, a quem se inscreveu no seu tipo."""

    def __init__(self) -> None:
        self._manipuladores: dict[type, list[Manipulador]] = {}

    def inscrever(self, tipo_evento: type, manipulador: Manipulador) -> None:
        self._manipuladores.setdefault(tipo_evento, []).append(manipulador)

    def publicar(self, evento: object) -> None:
        # Tipo exato: quem se inscreveu em PedidoPago nao recebe outros eventos.
        for manipulador in list(self._manipuladores.get(type(evento), [])):
            manipulador(evento)


if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Ola:
        nome: str

    barramento = BarramentoEmMemoria()
    barramento.inscrever(Ola, lambda evento: print(f"Ola, {evento.nome}!"))
    barramento.publicar(Ola("Maria"))
