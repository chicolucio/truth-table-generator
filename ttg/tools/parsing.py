import itertools
import pyparsing
import re

from ttg.tools import DOUBLE_OPERAND_OPS, SINGLE_OPERAND_OPS, OPERATIONS


def compile_regular_expressions(bases):
    return re.compile(r"(?<!\w)(" + "|".join(bases) + r")(?!\w)")


def configure_parser(bases):
    to_match = pyparsing.Word(pyparsing.alphanums)
    for item in itertools.chain(bases, [key for key, _ in OPERATIONS.items()]):
        to_match |= item
    return pyparsing.nestedExpr("(", ")", content=to_match)


def group_operations(phrase):
    """
    Groups operations in the phrase.

    Parameters:
        phrase (Union[list, bool]): The phrase to be grouped.

    Returns:
        Union[list, bool]: The grouped phrase.
    """

    if isinstance(phrase, list):
        # Handle inner operations first
        for i, item in enumerate(phrase):
            if isinstance(item, list):
                phrase[i] = group_operations(item)

        group_unary_operations(phrase, SINGLE_OPERAND_OPS)
        group_binary_operations(phrase, DOUBLE_OPERAND_OPS)

    return phrase


def group_unary_operations(phrase, unary_operators):
    i = 0
    while i < len(phrase):
        if phrase[i] in unary_operators:
            # Convert the unary operation into a list
            phrase[i] = [phrase[i], group_operations(phrase[i + 1])]
            del phrase[i + 1]
        i += 1


def group_binary_operations(phrase, binary_operators):
    i = 0
    while i < len(phrase):
        if phrase[i] in binary_operators:
            # Convert the binary operation into a list
            phrase[i] = [
                group_operations(phrase[i - 1]),
                phrase[i],
                group_operations(phrase[i + 1]),
            ]
            # Remove the operands that were just grouped
            del phrase[i + 1]
            del phrase[i - 1]
        i += 1
