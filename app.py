"""Normal baseline for the EvalAgent webhook demonstration."""


def calculate(expression):
    """Return the input as data without evaluating it as Python code."""
    return {"expression": expression}
