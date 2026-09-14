from datetime import date, timedelta

from ecommerce.forma_pagamento import FormaPagamento
from ecommerce.pagamento import (
    Pagamento,
    PagamentoBoleto,
    PagamentoCartao,
    PagamentoPix,
)

# Chave Pix de recebimento da loja. E uma configuracao, nao um dado do pedido.
CHAVE_PIX_DA_LOJA = "loja@ecommerce.com"


class CriadorPagamento:

    def criar(
        self,
        forma: FormaPagamento,
        pedido: "Pedido",
        valor: float,
        **dados: object,
    ) -> Pagamento:
        if forma == FormaPagamento.PIX:
            return PagamentoPix(
                pedido, valor, chave=dados.get("chave", CHAVE_PIX_DA_LOJA)
            )
        if forma == FormaPagamento.BOLETO:
            return PagamentoBoleto(
                pedido,
                valor,
                linha_digitavel=dados.get("linha_digitavel", "00000.00000 00000.000000 00000.000000 0 00000000000000"),
                vencimento=dados.get("vencimento", date.today() + timedelta(days=3)),
            )
        if forma == FormaPagamento.CARTAO_CREDITO:
            return PagamentoCartao(
                pedido,
                valor,
                bandeira=dados.get("bandeira", "VISA"),
                parcelas=dados.get("parcelas", 1),
            )
        raise ValueError(f"Forma de pagamento desconhecida: {forma}")


if __name__ == "__main__":
    from ecommerce.categoria import Categoria
    from ecommerce.pedido import Pedido
    from ecommerce.produto import Produto

    cat = Categoria("Informática")
    notebook = Produto("Notebook", 3500.0, 10, cat)
    pedido = Pedido()
    pedido.adicionar_item(notebook, 1)

    criador = CriadorPagamento()
    for forma in FormaPagamento:
        pagamento = criador.criar(forma, pedido, pedido.calcular_total())
        print(f"{forma.name}: {type(pagamento).__name__}")
