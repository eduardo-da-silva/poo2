from enum import Enum


class SituacaoPagamento(Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    RECUSADO = "recusado"


if __name__ == "__main__":
    print(f"Situacao inicial: {SituacaoPagamento.PENDENTE}")
    print(f"Confirmado: {SituacaoPagamento.CONFIRMADO.value}")
