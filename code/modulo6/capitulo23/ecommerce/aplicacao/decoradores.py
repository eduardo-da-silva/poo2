import time
from typing import Any, Callable

from ecommerce.aplicacao.caso_de_uso import CasoDeUso


class ComLog:
    """Embrulha um caso de uso e registra quando ele comeca, termina ou falha."""

    def __init__(
        self, caso_de_uso: CasoDeUso, nome: str, registrar: Callable[[str], None]
    ) -> None:
        self._caso_de_uso = caso_de_uso
        self._nome = nome
        self._registrar = registrar

    def executar(self, *args: Any, **kwargs: Any) -> Any:
        self._registrar(f"{self._nome}: inicio")
        try:
            resultado = self._caso_de_uso.executar(*args, **kwargs)
        except Exception as erro:
            self._registrar(f"{self._nome}: falhou ({type(erro).__name__}: {erro})")
            raise
        self._registrar(f"{self._nome}: concluido")
        return resultado


class ComTempo:
    """Embrulha um caso de uso e registra quanto tempo ele levou, mesmo se falhar."""

    def __init__(
        self,
        caso_de_uso: CasoDeUso,
        nome: str,
        registrar: Callable[[str], None],
        relogio: Callable[[], float] = time.perf_counter,
    ) -> None:
        self._caso_de_uso = caso_de_uso
        self._nome = nome
        self._registrar = registrar
        self._relogio = relogio

    def executar(self, *args: Any, **kwargs: Any) -> Any:
        inicio = self._relogio()
        try:
            return self._caso_de_uso.executar(*args, **kwargs)
        finally:
            milissegundos = (self._relogio() - inicio) * 1000
            self._registrar(f"{self._nome}: {milissegundos:.1f} ms")


if __name__ == "__main__":

    class Saudar:
        def executar(self, nome: str) -> str:
            return f"Ola, {nome}!"

    caso = ComLog(ComTempo(Saudar(), "Saudar", print), "Saudar", print)
    print(caso.executar("Maria"))
