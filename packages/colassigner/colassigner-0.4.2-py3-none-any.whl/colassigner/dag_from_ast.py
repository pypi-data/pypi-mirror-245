import ast
from importlib import import_module
from itertools import chain
from pathlib import Path
from typing import List, Type

from .core import ColAssigner


class MethodDef:
    def __init__(self, stmt: ast.FunctionDef, bases):
        self.name = stmt.name
        self.bases = set(bases)
        self.uses = set()
        self._adds(*stmt.body)

    def _add(self, elem: ast.AST):
        if isinstance(elem, ast.stmt):
            self._add_stmt(elem)
        elif isinstance(elem, ast.expr):
            self._add_expr(elem)
        else:
            self._add_other(elem)

    def _add_stmt(self, elem: ast.stmt):
        basic_stmts = (ast.Assign, ast.Return, ast.keyword, ast.Expr, ast.Starred)
        sub = ()
        if isinstance(elem, basic_stmts):
            sub = (elem.value,)
        if isinstance(elem, ast.If):
            sub = (elem.test, *elem.body, *elem.orelse)
        if isinstance(elem, ast.For):
            sub = (elem.iter, *elem.body)
        if isinstance(elem, ast.Try):
            sub = (*elem.handlers, *elem.body)
        # ast.Pass, ast.Raise ok
        return self._adds(*sub)

    def _add_expr(self, elem: ast.expr):
        sub = ()
        if isinstance(elem, (ast.List, ast.Tuple)):
            sub = elem.elts
        if isinstance(elem, ast.Lambda):
            sub = [elem.body]
        if isinstance(elem, ast.Slice):
            sub = (elem.lower, elem.upper)
        if isinstance(elem, ast.Attribute):
            base = elem.value
            if isinstance(base, ast.Name) and (base.id in [*self.bases, "self"]):
                return self.uses.add(elem.attr)
            sub = [base]
        if isinstance(elem, ast.Call):
            sub = (elem.func, *elem.args, *elem.keywords)
        if isinstance(elem, ast.BinOp):
            sub = (elem.left, elem.right)
        if isinstance(elem, ast.Subscript):
            sub = (elem.value, elem.slice)
        if isinstance(elem, ast.Compare):
            sub = (elem.left, *elem.comparators)
        # ast.Constant, ast.Name ok
        self._adds(*sub)

    def _add_other(self, elem):
        sub = ()
        if isinstance(elem, ast.ExceptHandler):
            sub = elem.body
        if isinstance(elem, ast.keyword):
            sub = [elem.value]
        self._adds(*sub)

    def _adds(self, *args):
        return list(map(self._add, args))


class ClsParser:
    def __init__(self, stmt: ast.ClassDef) -> None:
        self.name = stmt.name
        self._resolvers = {}
        self._mds: List[MethodDef] = []
        for fundef in stmt.body:
            md = MethodDef(fundef, [self.name])
            if md.name.startswith("_"):
                self._resolvers[md.name] = md.uses
            else:
                self._mds.append(md)

    def get_edges(self):
        return chain(*map(self._iter_mc, self._mds))

    def _iter_mc(self, md: MethodDef):
        for source in md.uses:
            if source.startswith("_"):
                for sub in self._resolve(source):
                    yield (sub, md.name)
            else:
                yield (source, md.name)

    def _resolve(self, source, resolved=()):
        for sub in self._resolvers.get(source, []):
            if sub in [source, *resolved]:
                continue
            resolved = (sub, *resolved)
            if sub.startswith("_"):
                for ssub in self._resolve(sub, resolved):
                    yield ssub
            else:
                yield sub


def get_dag(cls: Type[ColAssigner]):
    """generates a dag of the reliances of columns
    based on the ast of a colassigner

    Parameters
    ----------
    cls : Type[ColAssigner]

    Returns
    -------
    list of edges of a dag

    BETA! - WIP

    rules:
    - explicitly access columns within other functions
    - no external function referencing column (only method of assigner class)
    - no common source in as attributes
    - self should always be named self
    """
    fp = import_module(cls.__module__).__file__
    asm = ast.parse(Path(fp).read_text(), filename=fp)
    for stmt in asm.body:
        if isinstance(stmt, ast.ClassDef) and stmt.name == cls.__name__:
            return [*ClsParser(stmt).get_edges()]
