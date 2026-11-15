from enum import Enum


class FormaPagamento(Enum):
    PIX = "pix"
    BOLETO = "boleto"
    CARTAO_CREDITO = "cartao_credito"


if __name__ == "__main__":
    for forma in FormaPagamento:
        print(forma.name, "->", forma.value)
