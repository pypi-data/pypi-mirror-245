import ast
import math
import numbers
import operator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, TypeVar

if TYPE_CHECKING:
    from arithmetic_expressions.expression import Expression

T = TypeVar("T")

DEFAULT_FUNCTIONS = (min, max, abs, round, math.exp, math.log, math.log2, math.log10)


class ArithmeticEngine:
    def __init__(self, *, register_default_functions: bool = True):
        self._functions: dict[str, Callable] = {}
        self._custom_types : dict[str, tuple[Type, Callable[[Any], tuple[list, dict]]]] = {}
        self._default_context: dict[str, Callable] = {}

        if register_default_functions:
            self.add_default_functions()

    def register_function(
            self,
            function: Callable,
            *,
            name: Optional[str] = None,
    ) -> None:
        if name is None:
            name = function.__name__

        if name in self._functions:
            raise ValueError()

        self._functions[name] = function

    def add_default_functions(self):
        for func in DEFAULT_FUNCTIONS:
            self.register_function(func)

    def register_custom_type(
            self,
            custom_type: Type[T],
            deconstructor: Callable[[T], tuple[list, dict]],
            *,
            name: Optional[str] = None,
    ) -> None:
        if name is None:
            name = custom_type.__name__

        self.register_function(custom_type, name=name)
        self._custom_types[name] = custom_type, deconstructor

    def update_default_context(self, **kwargs):
        self._default_context.update(kwargs)

    def build_expression_type(self) -> Type['Expression']:
        from arithmetic_expressions.expression import Expression

        class _Expression(Expression):
            engine = self

        return _Expression

    def build_ast_object(self, value):
        if isinstance(value, ast.AST):
            return value
        elif isinstance(value, str):
            return ast.Name(value)
        elif isinstance(value, numbers.Number):
            return ast.Constant(value)
        else:
            for name, (custom_type, deconstructor) in self._custom_types.items():
                if isinstance(value, custom_type):
                    args, keywords = deconstructor(value)
                    return ast.Call(
                        func=ast.Name(id=name),
                        args=[ast.Constant(obj) for obj in args],
                        keywords={key: ast.Constant(value) for key, value in keywords.items()},
                    )
            else:
                raise ValueError(f"Unsupported value type: {type(value).__name__}")

    def build_evaluator(self, context) -> 'Evaluator':
        return Evaluator(self, context)

    def evaluate(self, node, context: Optional[dict] = None):
        custom_context = self._default_context
        if context is not None:
            custom_context |= context

        return self.build_evaluator(custom_context).evaluate(node)


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY_OPERATORS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
COMPARATORS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
}


@dataclass
class IllegalFunctionCallError(Exception):
    function_name: str

    def __str__(self):
        return f"Illegal function call: {self.function_name}"


@dataclass
class UndefinedVariableError(NameError):
    variable_name: str

    def __str__(self):
        return f"Undefined variable name: {self.variable_name}"


@dataclass
class Evaluator:
    engine: ArithmeticEngine
    context: dict

    def evaluate(self, node):
        if isinstance(node, ast.Constant):
            return node.value

        elif isinstance(node, ast.Name):
            try:
                return self.context[node.id]
            except KeyError as err:
                raise UndefinedVariableError(node.id) from err

        elif isinstance(node, ast.BinOp):
            return BINARY_OPERATORS[type(node.op)](
                self.evaluate(node.left),
                self.evaluate(node.right),
            )

        elif isinstance(node, ast.UnaryOp):
            return UNARY_OPERATORS[type(node.op)](self.evaluate(node.operand))

        elif isinstance(node, ast.Compare):
            return_value = True
            left = node.left
            for op, right in zip(node.ops, node.comparators):
                return_value &= COMPARATORS[type(op)](self.evaluate(left), self.evaluate(right))
                left = right

            return return_value

        elif isinstance(node, ast.IfExp):
            if self.evaluate(node.test):
                return self.evaluate(node.body)
            else:
                return self.evaluate(node.orelse)

        elif isinstance(node, ast.Call):
            try:
                func = self.engine._functions[node.func.id]
                return func(
                    *(self.evaluate(arg) for arg in node.args),
                    **{keyword: self.evaluate(keyword) for keyword in node.keywords},
                )
            except KeyError as err:
                raise IllegalFunctionCallError(node.func.id) from err

        else:
            raise TypeError(node)
