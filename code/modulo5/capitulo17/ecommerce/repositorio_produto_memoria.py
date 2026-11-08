from ecommerce.produto import Produto
from ecommerce.repositorio_produto import ProdutoNaoEncontradoError, RepositorioProduto


class RepositorioProdutoMemoria(RepositorioProduto):

    def __init__(self) -> None:
        self._produtos: dict[int, Produto] = {}
        self._proximo_id = 1

    def adicionar(self, produto: Produto) -> None:
        produto.atribuir_id(self._proximo_id)
        self._produtos[self._proximo_id] = produto
        self._proximo_id += 1

    def obter(self, id: int) -> Produto:
        if id not in self._produtos:
            raise ProdutoNaoEncontradoError(f"Produto {id} nao encontrado")
        return self._produtos[id]

    def listar(self) -> list[Produto]:
        return list(self._produtos.values())

    def atualizar(self, produto: Produto) -> None:
        if produto.id is None or produto.id not in self._produtos:
            raise ProdutoNaoEncontradoError("Produto nunca foi adicionado")
        # Guardamos a propria referencia: nao ha nada a copiar.
        self._produtos[produto.id] = produto


if __name__ == "__main__":
    from ecommerce.categoria import Categoria

    repositorio = RepositorioProdutoMemoria()
    notebook = Produto("Notebook", 3500.0, 10, Categoria("Informática"))
    repositorio.adicionar(notebook)
    print(f"Id atribuido: {notebook.id}")
    print(f"Produtos guardados: {len(repositorio.listar())}")
