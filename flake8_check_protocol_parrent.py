from __future__ import annotations

import ast
from typing import Any, Generator
import importlib.metadata as importlib_metadata


TRA01 = 'TRA01 Protocol children need to be started with `I`'


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[tuple[int, int, str]] = []
        self._from_imports: dict[str, str] = {}

    def visit_ClassDef(self, node) -> None:
        base_nodes = node.bases
        for base_node in base_nodes:
            if base_node.id == 'Protocol' and node.name[0] != 'I':
                self.errors.append((
                    node.lineno, node.col_offset, TRA01,
                ))
                break
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
