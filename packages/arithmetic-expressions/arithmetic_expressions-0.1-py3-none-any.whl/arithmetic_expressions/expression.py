import ast
from typing import ClassVar, Type, TypeVar

from arithmetic_expressions.engine import ArithmeticEngine

E = TypeVar("E", bound="Expression")


class Expression:
    """
    A class for representation, evaluation, serialization and deserialization of arithmetic expressions.

    The `Expression` class is as a wrapper for expressions in Python's own abstract grammar (using the `ast` module).
    While it supports the creation of arbitrary expressions, it's focus lies on arithmetic expressions composed of
    standard arithmetic operations on numeric constants and variables and it can only evaluate such expressions.

Expressions can be deserialized from strings, but can also be built from scratch with an intuitive API, mirroring
Python's own syntax.

    Example:
    ```python
    expression = Expression("x") * 2 + 1
    print(expression)  # prints "x * 2 + 1"
    print(expression.evaluate(x=3))  # prints "7"
    ```
    """
    engine: ClassVar[ArithmeticEngine] = ArithmeticEngine()

    def __init__(self, value):
        """
        Initializes an Expression object.

        This method creates an Abstract Syntax Tree (AST) node from the given argument. If the argument is already an
        AST node, it is used directly. Numeric values are considered constants in the expression, while strings are
        treated as variables.

        Parameters:
        - value: The initial value for the expression. If a numeric value, it is treated as a constant; if a string,
          it is considered a variable; if an AST node, it is used directly.
        """
        self.ast_expression = self.engine.build_ast_object(value)

    @classmethod
    def parse(cls: Type[E], expression: str) -> E:
        """
        Parses a string expression and returns an Expression object.

        Parameters:
        - expression (str): The expression to be parsed.

        Returns:
        - E: An Expression object representing the parsed expression.

        Raises:
        - ValueError: If the expression is not a single statement.

        """
        parse_result = ast.parse(expression).body
        if len(parse_result) != 1:
            raise ValueError("Expression must be a single statement.")

        return cls(parse_result[0].value)

    def serialize(self) -> str:
        """
        Serializes the expression.

        Returns:
        - A string containing the serialized expression.
        """
        return ast.unparse(self.ast_expression)

    def evaluate(self, **kwargs):
        """
        Evaluates the expression using the provided keyword arguments to substitute variables in the expression with
        concrete values.

        Parameters:
        - **kwargs: All keyword arguments are considered values of variables that will be used in the evaluation.

        Returns:
        - The result of the expression evaluation.

        Raises:
        - UndefinedVariableError: If the expression contains a variable for which no value is given as a keyword
          argument.

        """
        return self.engine.evaluate(node=self.ast_expression, context=kwargs)

    def _binary_op(self: E, other, op: ast.operator, *, reverse: bool = False) -> E:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        if reverse:
            return self.__class__(ast.BinOp(right=self.ast_expression, left=other.ast_expression, op=op))
        else:
            return self.__class__(ast.BinOp(left=self.ast_expression, right=other.ast_expression, op=op))

    def _unary_op(self: E, op) -> E:
        return self.__class__(ast.UnaryOp(operand=self.ast_expression, op=op))

    def _compare(self: E, other, op: ast.cmpop) -> E:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self.__class__(ast.Compare(left=self.ast_expression, comparators=[other.ast_expression], ops=[op]))

    def lower_bound(self: E, other) -> E:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self.__class__(ast.IfExp(
            test=(self > other).ast_expression,
            body=self.ast_expression,
            orelse=other.ast_expression,
        ))

    def upper_bound(self: E, other) -> E:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self.__class__(ast.IfExp(
            test=(self < other).ast_expression,
            body=self.ast_expression,
            orelse=other.ast_expression,
        ))

    def __add__(self, other):
        return self._binary_op(other, ast.Add())

    def __radd__(self, other):
        return self._binary_op(other, ast.Add(), reverse=True)

    def __sub__(self, other):
        return self._binary_op(other, ast.Sub())

    def __rsub__(self, other):
        return self._binary_op(other, ast.Sub(), reverse=True)

    def __mul__(self, other):
        return self._binary_op(other, ast.Mult())

    def __rmul__(self, other):
        return self._binary_op(other, ast.Mult(), reverse=True)

    def __floordiv__(self, other):
        return self._binary_op(other, ast.FloorDiv())

    def __rfloordiv__(self, other):
        return self._binary_op(other, ast.FloorDiv(), reverse=True)

    def __truediv__(self, other):
        return self._binary_op(other, ast.Div())

    def __rtruediv__(self, other):
        return self._binary_op(other, ast.Div(), reverse=True)

    def __mod__(self, other):
        return self._binary_op(other, ast.Mod())

    def __rmod__(self, other):
        return self._binary_op(other, ast.Mod(), reverse=True)

    def __pow__(self, other):
        return self._binary_op(other, ast.Pow())

    def __rpow__(self, other):
        return self._binary_op(other, ast.Pow(), reverse=True)

    def __eq__(self, other):
        return self._compare(other, ast.Eq())

    def __ne__(self, other):
        return self._compare(other, ast.NotEq())

    def __ge__(self, other):
        return self._compare(other, ast.GtE())

    def __gt__(self, other):
        return self._compare(other, ast.Gt())

    def __le__(self, other):
        return self._compare(other, ast.LtE())

    def __lt__(self, other):
        return self._compare(other, ast.Lt())

    def __pos__(self):
        return self._unary_op(ast.UAdd())

    def __neg__(self):
        return self._unary_op(ast.USub())

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return self.serialize()
