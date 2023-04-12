import ast
import logging

from typing import Set

from dogpt.exceptions import InvalidProgramException, UnsafeSyntaxError


logger = logging.getLogger(__name__)


class ProgramValidator:
    def validate(self, text: str) -> bool:
        """Check if text is a valid Python program"""
        try:
            ast.parse(text)
        except SyntaxError as error:
            raise InvalidProgramException(str(error))


class SyntaxSafetyValidator(ast.NodeVisitor):
    """
    Abstract syntax tree visitor that checks for syntax safety.
    """

    _safe_func_ids: Set[str]

    _has_import: bool
    _has_unsafe_call: bool

    def __init__(self, safe_func_ids: Set[str]):
        self._safe_func_ids = safe_func_ids

        self._has_import = False
        self._has_unsafe_call = False

    def visit_Import(self, node: ast.Import):
        self._has_import = True

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self._has_import = True

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id not in self._safe_func_ids:
                self._has_unsafe_call = True

    def validate(self, tree: ast.Module):
        # Visit the tree with the SyntaxSafetyValidator
        self.visit(tree)

        # Check if the code is valid
        if self._has_import:
            raise UnsafeSyntaxError("Syntax contains imports")
        elif self._has_unsafe_call:
            raise UnsafeSyntaxError("Syntax contains unsafe function calls")
        else:
            logger.info("Syntax is safe")
