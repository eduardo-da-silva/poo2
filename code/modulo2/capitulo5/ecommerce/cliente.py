class Cliente:

    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email
        self.carrinho: "Carrinho | None" = None
        self._pedidos: list["Pedido"] = []

    @property
    def pedidos(self) -> list["Pedido"]:
        return list(self._pedidos)

    def possui_carrinho(self) -> bool:
        return self.carrinho is not None

    def adicionar_pedido(self, pedido: "Pedido") -> None:
        self._pedidos.append(pedido)


if __name__ == "__main__":
    c = Cliente("João", "joao@email.com")
    print(f"Cliente: {c.nome}, Email: {c.email}")
    print(f"Possui carrinho: {c.possui_carrinho()}")
