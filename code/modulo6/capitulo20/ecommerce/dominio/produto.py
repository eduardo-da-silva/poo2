from ecommerce.dominio.categoria import Categoria


class EstoqueInsuficienteError(Exception):
    pass


class Produto:

    def __init__(
        self, nome: str, preco: float, quantidade_estoque: int, categoria: Categoria
    ) -> None:
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria
        self._id: int | None = None

    @property
    def id(self) -> int | None:
        return self._id

    def atribuir_id(self, id: int) -> None:
        # A identidade e definida uma unica vez, por quem guarda o produto.
        if self._id is not None:
            raise ValueError("Produto ja possui identidade")
        self._id = id

    def esta_disponivel(self) -> bool:
        return self.quantidade_estoque > 0

    def dar_baixa(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if quantidade > self.quantidade_estoque:
            raise EstoqueInsuficienteError(
                f"Estoque de {self.nome}: restam {self.quantidade_estoque}, solicitado {quantidade}"
            )
        self.quantidade_estoque -= quantidade

    def aplicar_desconto(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.preco -= self.preco * (percentual / 100)

    def alterar_preco(self, novo_preco: float) -> None:
        if novo_preco <= 0:
            raise ValueError("Preco deve ser positivo")
        self.preco = novo_preco


if __name__ == "__main__":
    from ecommerce.dominio.categoria import Categoria

    cat = Categoria("Informática")
    p = Produto("Notebook", 3500.0, 10, cat)
    print(f"Produto: {p.nome}, Preco: {p.preco}, Disponivel: {p.esta_disponivel()}")

    p.aplicar_desconto(10)
    print(f"Com 10% de desconto: {p.preco}")

    p.alterar_preco(4000.0)
    print(f"Preco reajustado: {p.preco}")
