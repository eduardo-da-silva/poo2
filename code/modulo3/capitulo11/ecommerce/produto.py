from ecommerce.categoria import Categoria


class Produto:

    def __init__(
        self, nome: str, preco: float, quantidade_estoque: int, categoria: Categoria
    ) -> None:
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria

    def esta_disponivel(self) -> bool:
        return self.quantidade_estoque > 0

    def aplicar_desconto(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.preco -= self.preco * (percentual / 100)

    def alterar_preco(self, novo_preco: float) -> None:
        if novo_preco <= 0:
            raise ValueError("Preco deve ser positivo")
        self.preco = novo_preco


if __name__ == "__main__":
    from ecommerce.categoria import Categoria

    cat = Categoria("Informática")
    p = Produto("Notebook", 3500.0, 10, cat)
    print(f"Produto: {p.nome}, Preco: {p.preco}, Disponivel: {p.esta_disponivel()}")

    p.aplicar_desconto(10)
    print(f"Com 10% de desconto: {p.preco}")

    p.alterar_preco(4000.0)
    print(f"Preco reajustado: {p.preco}")
