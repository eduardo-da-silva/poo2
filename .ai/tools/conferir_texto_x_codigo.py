"""Confere se o codigo mostrado nos blocos .py dos capitulos bate com o codigo real do snapshot.

Diferencas esperadas: trechos intermediarios, elisoes (...), anotacoes omitidas. Revise-as a mao.
Uso: python .ai/tools/conferir_texto_x_codigo.py
"""
import ast, re, sys, textwrap
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from auditar_codigo_no_texto import CAPS, RAIZ, blocos

def nodes_de(texto):
    """Classes/funcoes de um bloco (tenta com e sem indentacao); devolve {qualname: no}."""
    for tentativa in (textwrap.dedent(texto), "class _X:\n" + texto):
        try:
            arvore = ast.parse(tentativa)
        except SyntaxError:
            continue
        out = {}
        corpo = arvore.body
        if tentativa.startswith("class _X:") and len(corpo) == 1:
            corpo = corpo[0].body
        for no in corpo:
            if isinstance(no, ast.ClassDef):
                out[no.name] = no
                for sub in no.body:
                    if isinstance(sub, ast.FunctionDef):
                        out[f"{no.name}.{sub.name}"] = sub
            elif isinstance(no, ast.FunctionDef):
                out[no.name] = no
        return out
    return None

def dump(no):
    # ignora docstrings e anotacoes de retorno triviais nao: compara estrutura completa
    cp = ast.parse(ast.unparse(no)).body[0]
    if cp.body and isinstance(cp.body[0], ast.Expr) and isinstance(getattr(cp.body[0], "value", None), ast.Constant) and isinstance(cp.body[0].value.value, str):
        cp.body = cp.body[1:] or [ast.Pass()]
    return ast.dump(cp)

def tem_elisao(no):
    return any(isinstance(n, ast.Constant) and n.value is Ellipsis for n in ast.walk(no))

def real_defs(snap):
    out = {}
    for f in sorted(snap.rglob("*.py")):
        if "__pycache__" in f.parts: continue
        arvore = ast.parse(f.read_text(encoding="utf-8"))
        for no in arvore.body:
            if isinstance(no, ast.ClassDef):
                out.setdefault(no.name, []).append((f, no))
                for sub in no.body:
                    if isinstance(sub, ast.FunctionDef):
                        out.setdefault(f"{no.name}.{sub.name}", []).append((f, sub))
            elif isinstance(no, ast.FunctionDef):
                out.setdefault(no.name, []).append((f, no))
    return out

total = 0
for cap, mod in CAPS:
    snap = RAIZ / "code" / mod / f"capitulo{cap}"
    doc = RAIZ / "docs" / mod / f"capitulo{cap}.md"
    reais = real_defs(snap)
    achados = []
    for titulo, codigo in blocos(doc.read_text(encoding="utf-8")):
        if not titulo.endswith(".py"):
            continue
        nos = nodes_de(codigo)
        if not nos:
            continue
        stem = Path(titulo).stem
        for qual, no in nos.items():
            if "." not in qual and isinstance(no, ast.ClassDef):
                pass
            if tem_elisao(no):
                continue
            candidatos = [(f, n) for f, n in reais.get(qual, []) if f.stem == stem] or reais.get(qual, [])
            if not candidatos and "." not in qual:
                candidatos = [(f, n) for k, v in reais.items() if k.endswith("." + qual) for f, n in v if f.stem == stem]
            if not candidatos:
                achados.append((titulo, qual, "nao existe no snapshot"))
                continue
            if isinstance(no, ast.ClassDef):
                # classe excerpt: compara so os metodos mostrados (ja visitados pelo laco)
                continue
            if not any(dump(no) == dump(n) for f, n in candidatos):
                import difflib
                real = ast.unparse(candidatos[0][1]).splitlines()
                mostrado = ast.unparse(no).splitlines()
                d = "\n".join(l for l in difflib.unified_diff(mostrado, real, "TEXTO", "CODIGO", lineterm="", n=0) if not l.startswith(("---","+++","@@")))
                achados.append((titulo, qual, "difere\n" + d))
    if achados:
        print(f"\n--- Cap. {cap} ---")
        for t, q, m in achados:
            print(f"  {t}  {q}: {m}".replace("\n","\n      "))
            total += 1
print("\ntotal de divergencias:", total)
