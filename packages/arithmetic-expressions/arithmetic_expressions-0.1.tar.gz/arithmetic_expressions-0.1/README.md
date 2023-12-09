# arithmetic-expressions

`arithmetic-expression` is a Python module for symbolic arithmetic expressions. It supports serialization,
deserialization, evaluation with custom variables, and an easy construction interface by combining existing
expressions.

It is built around Python's `ast` module and therefore uses Python syntax when string serializing and deserializing.
However, it only supports single-line expressions and strongly restricts the grammar when evaluating expressions.
This constrained subset of the grammar encompasses variables, numeric constants, unary and binary arithmetic
operators, comparison operators, the ternary if-else operator and selected function calls.

Expressions can be deserialized from strings, but can also be built from scratch with an intuitive API that aligns with
Python's own syntax.

## Example

```python
from arithmetic_expressions import Expression

# Parse an expression
Expression.parse("x * 2 + 1")

# Or create it from scratch
expression = Expression("x") * 2 + 1

# String casting will serialize the expression
print(expression)  # prints "x * 2 + 1"

# Pass variables to evaluate it
print(expression.evaluate(x=3))  # prints "7"
```
