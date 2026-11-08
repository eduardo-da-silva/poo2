import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade_estoque INTEGER NOT NULL,
    categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_pedido (
    pedido_id INTEGER NOT NULL REFERENCES pedido(id),
    produto_id INTEGER NOT NULL REFERENCES produto(id),
    quantidade INTEGER NOT NULL,
    preco_no_momento REAL NOT NULL
);
"""


def criar_esquema(conexao: sqlite3.Connection) -> None:
    conexao.executescript(ESQUEMA)


if __name__ == "__main__":
    conexao = sqlite3.connect(":memory:")
    criar_esquema(conexao)
    tabelas = conexao.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tabelas:", sorted(nome for (nome,) in tabelas if not nome.startswith("sqlite_")))
