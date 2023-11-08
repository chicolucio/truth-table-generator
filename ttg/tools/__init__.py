BASE_OPERATIONS = {
    "not": lambda x: not x,
    "or": lambda x, y: x or y,
    "nor": lambda x, y: not (x or y),
    "xor": lambda x, y: x != y,
    "and": lambda x, y: x and y,
    "nand": lambda x, y: not (x and y),
    "implies": lambda x, y: not x or y,
    "equals": lambda x, y: x == y,
}

OPERATION_ALIASES = {
    "not": ["not", "-", "~"],
    "or": ["or"],
    "nor": ["nor"],
    "xor": ["xor", "!="],
    "and": ["and"],
    "nand": ["nand"],
    "implies": ["=>", "implies"],
    "equals": ["="],
}

SINGLE_OPERAND_OPS = ("not", "~", "-")

DOUBLE_OPERAND_OPS = ("and", "nand", "or", "nor", "xor", "=>", "implies", "=", "!=")


def build_operations_dict(base_operations, operation_aliases):
    operations = {}
    for base_op, func in base_operations.items():
        for alias in operation_aliases.get(base_op, []):
            operations[alias] = func
    return operations


OPERATIONS = build_operations_dict(BASE_OPERATIONS, OPERATION_ALIASES)
