"""Confere se todo codigo novo ou alterado de cada snapshot (code/) aparece nos blocos de codigo do capitulo.

Uso: python .ai/tools/auditar_codigo_no_texto.py [resumo|detalhe]
Ao criar um capitulo novo, acrescente o par (numero, modulo) em CAPS.
"""
import ast, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
# (doc, snapshot) em ordem de evolucao; o anterior de cada um e o item anterior da lista
CAPS = [(4,"modulo1"),(5,"modulo2"),(6,"modulo2"),(7,"modulo2"),(8,"modulo3"),(9,"modulo3"),(10,"modulo3"),(11,"modulo3"),
        (12,"modulo4"),(13,"modulo4"),(14,"modulo4"),(15,"modulo4"),(16,"modulo5"),(17,"modulo5"),(18,"modulo5"),(19,"modulo5"),
        (20,"modulo6"),(21,"modulo6"),(22,"modulo6")]

def py_files(snap: Path, testes: bool):
    for f in sorted(snap.rglob("*.py")):
        rel = f.relative_to(snap).parts
        eh_teste = rel[0] == "tests" or f.name.startswith("test_") or f.name == "conftest.py"
        if eh_teste == testes and "__pycache__" not in rel:
            yield f

def defs(snap: Path, testes=False):
    """{(qualname): (tipo, arquivo, fonte)}, incluindo metodos e constantes de modulo."""
    out = {}
    for f in py_files(snap, testes):
        texto = f.read_text(encoding="utf-8")
        linhas = texto.splitlines()
        try:
            arvore = ast.parse(texto)
        except SyntaxError:
            continue
        def fonte(no):
            ini = min([no.lineno] + [d.lineno for d in getattr(no, "decorator_list", [])])
            return "\n".join(linhas[ini-1:no.end_lineno])
        for no in arvore.body:
            if isinstance(no, ast.ClassDef):
                out[no.name] = ("class", f.name, fonte(no))
                for sub in no.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        out[f"{no.name}.{sub.name}"] = ("def", f.name, fonte(sub))
            elif isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out[no.name] = ("func", f.name, fonte(no))
            elif isinstance(no, (ast.Assign, ast.AnnAssign)):
                alvo = no.targets[0] if isinstance(no, ast.Assign) else no.target
                if isinstance(alvo, ast.Name):
                    out[alvo.id] = ("const", f.name, fonte(no))
    return out

def blocos(md: str):
    achados = []
    for m in re.finditer(r"```([a-z]*)([^\n]*)\n(.*?)```", md, re.S):
        titulo = re.search(r'title="([^"]*)"', m.group(2))
        achados.append((titulo.group(1) if titulo else "", m.group(3)))
    return achados

def mostrado(tipo, qual, arquivo, bl):
    stem = Path(arquivo).stem
    if tipo == "class":
        return any(f"class {qual}" in c for _, c in bl)
    if tipo == "const":
        return any(re.search(rf"\b{re.escape(qual)}\b\s*[:=]", c) for _, c in bl)
    nome = qual.split(".")[-1]
    cls = qual.split(".")[0] if "." in qual else None
    for t, c in bl:
        if f"def {nome}(" not in c:
            continue
        if cls is None:
            return True
        if f"class {cls}" in c or stem in t:
            return True
    return False

def main():
    anterior = {}
    geral = []
    for cap, mod in CAPS:
        snap = RAIZ / "code" / mod / f"capitulo{cap}"
        doc = RAIZ / "docs" / mod / f"capitulo{cap}.md"
        if not snap.exists():
            continue
        atual = defs(snap)
        bl = blocos(doc.read_text(encoding="utf-8"))
        faltam, novos = [], 0
        for qual, (tipo, arq, src) in atual.items():
            if qual in anterior and anterior[qual][2] == src:
                continue
            if tipo == "def" and "." in qual and qual.split(".")[0] in atual and qual.split(".")[0] in anterior:
                pass  # metodo novo/alterado em classe que ja existia: precisa aparecer
            if tipo == "class" and qual in anterior:
                continue  # classe que ja existia e foi alterada: os metodos alterados e que precisam aparecer
            novos += 1
            if tipo in ("def",) and qual.split(".")[-1].startswith("__") and qual.split(".")[-1] != "__init__":
                continue
            if not mostrado(tipo, qual, arq, bl):
                faltam.append((qual, tipo, arq))
        # testes: so contagem
        t_atual = defs(snap, testes=True)
        t_ant = anterior.get("__testes__", {})
        t_novos = [q for q, (t, a, s) in t_atual.items() if t in ("func","def") and q.split(".")[-1].startswith("test_")
                   and not (q in t_ant and t_ant[q][2] == s)]
        texto_doc = " ".join(c for _, c in bl)
        t_mostrados = [q for q in t_novos if f"def {q.split('.')[-1]}(" in texto_doc]
        geral.append((cap, mod, novos, faltam, len(t_novos), len(t_mostrados)))
        anterior = atual
        anterior["__testes__"] = t_atual
    return geral

if __name__ == "__main__":
    geral = main()
    modo = sys.argv[1] if len(sys.argv) > 1 else "resumo"
    print(f"{'cap':>4} {'defs novas/alteradas':>22} {'faltam no texto':>16} {'testes novos':>13} {'mostrados':>10}")
    for cap, mod, novos, faltam, tn, tm in geral:
        print(f"{cap:>4} {novos:>22} {len(faltam):>16} {tn:>13} {tm:>10}")
    if modo == "detalhe":
        for cap, mod, novos, faltam, tn, tm in geral:
            if faltam:
                print(f"\n--- Cap. {cap} ({mod}) ---")
                for q, t, a in faltam:
                    print(f"  {t:5} {q}   [{a}]")
