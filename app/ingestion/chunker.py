import ast


def chunk_python_file(file_path: str) -> list[dict]:
    """Parse a Python file and return a list of chunks (functions/classes with their code)."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    chunks = []
    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno
            code = "\n".join(lines[start:end])

            chunks.append({
                "name": node.name,
                "type": type(node).__name__,
                "file": file_path,
                "code": code,
            })

    return chunks