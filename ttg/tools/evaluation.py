from ttg.tools import DOUBLE_OPERAND_OPS, SINGLE_OPERAND_OPS
from ttg.tools import OPERATIONS


def recursive_map(func, data):
    """Recursively applies a map function to a list and all sublists."""
    if isinstance(data, list):
        return [recursive_map(func, elem) for elem in data]
    else:
        return func(data)


def string_to_bool(string):
    if string == "True":
        return True
    if string == "False":
        return False
    return string


def solve_phrase(phrase):
    """Recursively evaluates a logical phrase that has been grouped into
    sublists where each list is one operation.
    """
    if isinstance(phrase, bool):
        return phrase

    if isinstance(phrase, list):
        n = len(phrase)

        # List with just a list in it
        if n == 1:
            return solve_phrase(phrase[0])

        # Single operand operation
        if n == 2 and phrase[0] in SINGLE_OPERAND_OPS:
            return OPERATIONS[phrase[0]](solve_phrase(phrase[1]))

        # Double operand operation
        if n >= 3 and phrase[1] in DOUBLE_OPERAND_OPS:
            return OPERATIONS[phrase[1]](
                solve_phrase(phrase[0]), solve_phrase(phrase[2])
            )

        raise ValueError("Invalid expression")
