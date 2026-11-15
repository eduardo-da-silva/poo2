from typing import Callable

from ecommerce.composicao import Aplicacao
from ecommerce.dominio.carrinho import Carrinho
from ecommerce.dominio.cliente import Cliente
from ecommerce.dominio.repositorio_pedido import PedidoNaoEncontradoError
from ecommerce.dominio.repositorio_produto import ProdutoNaoEncontradoError

OPCOES = """
1. Listar produtos
2. Colocar produto no carrinho
3. Finalizar compra
4. Pagar pedido
5. Despachar pedido
6. Consultar pedido
7. Ver auditoria
0. Sair"""


class Menu:
    """Menu de terminal: traduz o que a pessoa digita em chamadas aos casos de uso.

    `entrada` e `saida` chegam de fora, como qualquer outra dependencia:
    nos testes, uma sessao roteirizada; no terminal, `input` e `print`.
    """

    def __init__(
        self,
        app: Aplicacao,
        entrada: Callable[[str], str] = input,
        saida: Callable[[str], None] = print,
    ) -> None:
        self._app = app
        self._entrada = entrada
        self._saida = saida
        self._cliente = Cliente("Maria", "maria@email.com")
        self._cliente.carrinho = Carrinho()
        self._acoes = {
            "1": self._listar_produtos,
            "2": self._colocar_no_carrinho,
            "3": self._finalizar_compra,
            "4": self._pagar_pedido,
            "5": self._despachar_pedido,
            "6": self._consultar_pedido,
            "7": self._ver_auditoria,
        }

    def executar(self) -> None:
        while True:
            self._saida(OPCOES)
            opcao = self._entrada("Opcao: ").strip()
            if opcao == "0":
                self._saida("Ate logo.")
                return
            acao = self._acoes.get(opcao)
            if acao is None:
                self._saida("Opcao invalida.")
                continue
            self._executar_com_seguranca(acao)

    def _executar_com_seguranca(self, acao: Callable[[], None]) -> None:
        # Fronteira do sistema: as excecoes viram mensagens na linguagem do terminal.
        try:
            acao()
        except (ValueError, PedidoNaoEncontradoError, ProdutoNaoEncontradoError) as erro:
            self._saida(f"Erro: {erro}")

    def _ler_inteiro(self, pergunta: str) -> int:
        texto = self._entrada(pergunta).strip()
        try:
            return int(texto)
        except ValueError:
            raise ValueError("digite um numero inteiro") from None

    def _listar_produtos(self) -> None:
        produtos = self._app.listar_produtos.executar()
        if not produtos:
            self._saida("Nenhum produto cadastrado.")
        for produto in produtos:
            self._saida(
                f"{produto.id}. {produto.nome} - R$ {produto.preco:.2f} "
                f"(estoque {produto.quantidade_estoque})"
            )

    def _colocar_no_carrinho(self) -> None:
        produto_id = self._ler_inteiro("Id do produto: ")
        quantidade = self._ler_inteiro("Quantidade: ")
        produtos = {p.id: p for p in self._app.listar_produtos.executar()}
        if produto_id not in produtos:
            raise ProdutoNaoEncontradoError(f"Produto {produto_id} nao encontrado")
        self._cliente.carrinho.adicionar_item(produtos[produto_id], quantidade)
        self._saida(f"{quantidade} x {produtos[produto_id].nome} no carrinho.")

    def _finalizar_compra(self) -> None:
        pedido = self._app.finalizar_compra.executar(self._cliente)
        self._saida(f"Pedido {pedido.id} criado: R$ {pedido.calcular_total():.2f}")

    def _pagar_pedido(self) -> None:
        pedido_id = self._ler_inteiro("Id do pedido: ")
        self._app.pagar_pedido.executar(pedido_id, self._cliente)
        self._saida(f"Pagamento do pedido {pedido_id} confirmado.")

    def _despachar_pedido(self) -> None:
        pedido_id = self._ler_inteiro("Id do pedido: ")
        entrega = self._app.despachar_pedido.executar(pedido_id, self._cliente)
        self._saida(f"Pedido {pedido_id} enviado. Rastreio: {entrega.codigo_rastreio}")

    def _consultar_pedido(self) -> None:
        pedido = self._app.consultar_pedido.executar(self._ler_inteiro("Id do pedido: "))
        self._saida(
            f"Pedido {pedido.id}: {pedido.status}, "
            f"{pedido.quantidade_itens()} item(ns), R$ {pedido.calcular_total():.2f}"
        )

    def _ver_auditoria(self) -> None:
        entradas = self._app.auditoria.entradas()
        if not entradas:
            self._saida("Nenhuma entrada de auditoria.")
        for entrada in entradas:
            self._saida(entrada)


def preparar_produtos(app: Aplicacao) -> None:
    """Cadastra o catalogo inicial, mas so se a loja ainda estiver vazia."""
    if app.listar_produtos.executar():
        return
    app.cadastrar_produto.executar("Notebook", 3500.0, 5, "Informática")
    app.cadastrar_produto.executar("Mouse", 150.0, 20, "Informática")
    app.cadastrar_produto.executar("Teclado", 250.0, 10, "Informática")
