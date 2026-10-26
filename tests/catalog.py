"""List every test case with the catastrophe it guards against (its docstring), grouped by file.

Usage: python3 -I tests/catalog.py            Markdown tables, one per test file
       python3 -I tests/catalog.py --count    just the number of test cases per file
"""
import ast
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

total = 0
for path in sorted(HERE.glob("test_*.py")):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    cases = []
    for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
        for fn in (n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")):
            doc = (ast.get_docstring(fn) or "(no docstring)").splitlines()[0]
            cases.append((cls.name, fn.name, doc))
    total += len(cases)
    if "--count" in sys.argv:
        print(f"{len(cases):4d}  tests/{path.name}")
        continue
    module_doc = (ast.get_docstring(tree) or "").splitlines()[0] if ast.get_docstring(tree) else ""
    print(f"### tests/{path.name}\n\n{module_doc}\n\n| Group | Test | Guards against |\n|---|---|---|")
    for cls, name, doc in cases:
        print(f"| {cls} | `{name}` | {doc} |")
    print()
print(f"{total} test cases" if "--count" in sys.argv else f"Total: {total} test cases.")
