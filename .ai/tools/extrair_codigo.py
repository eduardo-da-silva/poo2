"""Extrai o codigo-fonte exato de classes/funcoes de um arquivo, para colar nos capitulos sem redigitar."""
import ast
from pathlib import Path

def seg(arquivo: str, *nomes: str) -> str:
    """Devolve o codigo-fonte exato de classes/funcoes (ou Classe.metodo) de um arquivo."""
    texto = Path(arquivo).read_text(encoding="utf-8")
    linhas = texto.splitlines()
    arvore = ast.parse(texto)
    pedacos = []
    for nome in nomes:
        partes = nome.split(".")
        no = None
        corpo = arvore.body
        for parte in partes:
            no = next(n for n in corpo if getattr(n, "name", None) == parte)
            corpo = getattr(no, "body", [])
        inicio = min([no.lineno] + [d.lineno for d in getattr(no, "decorator_list", [])])
        pedacos.append("\n".join(linhas[inicio - 1:no.end_lineno]))
    return "\n\n".join(pedacos)

def trecho(arquivo: str, inicio: str, fim: str) -> str:
    """Linhas de `inicio` ate (e incluindo) a linha que contem `fim`."""
    linhas = Path(arquivo).read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(linhas) if inicio in l)
    j = next(k for k in range(i, len(linhas)) if fim in linhas[k])
    return "\n".join(linhas[i:j + 1])

def ate_linha(arquivo: str, inicio: str, linha_final: str) -> str:
    """Da primeira linha que comeca com `inicio` ate a primeira linha igual a `linha_final`."""
    linhas = Path(arquivo).read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(linhas) if l.startswith(inicio))
    j = next(k for k in range(i, len(linhas)) if linhas[k] == linha_final)
    return "\n".join(linhas[i:j + 1])
