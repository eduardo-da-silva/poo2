class Roteiro:
    """Uma sessao de terminal escrita de antemao: cada chamada devolve a proxima resposta."""

    def __init__(self, *respostas: str) -> None:
        self._respostas = iter([*respostas, "0"])

    def __call__(self, pergunta: str) -> str:
        return next(self._respostas)
