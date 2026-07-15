class Categoria:

    def __init__(self, nome: str) -> None:
        self.nome = nome


if __name__ == "__main__":
    cat = Categoria("Informática")
    print(f"Categoria: {cat.nome}")
