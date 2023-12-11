import ast

import astor


def remove_docstring(source_code):
    """
    Removes the docstring from the given source code.
    From https://gist.github.com/phpdude/1ae6f19de213d66286c8183e9e3b9ec1

    Args:
        source_code (str): The source code containing the docstring.

    Returns:
        str: The modified source code without the docstring.
    """
    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            continue

        if not len(node.body):
            continue

        if not isinstance(node.body[0], ast.Expr):
            continue

        if not hasattr(node.body[0], "value") or not isinstance(
            node.body[0].value, ast.Str
        ):
            continue

        node.body = node.body[1:]

    return astor.to_source(parsed)
