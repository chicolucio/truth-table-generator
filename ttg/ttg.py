#!/usr/bin/env python

# Copyright 2019 Francisco Bustamante
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Package forked from truths, a module by Trey Morris

# Copyright 2016 Trey Morris
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""
truth-table-generator main file
"""

import itertools
import re
from prettytable import PrettyTable
import pyparsing
import pandas as pd
from tabulate import tabulate

# dict of boolean operations
OPERATIONS = {
    "not": (lambda x: not x),
    "-": (lambda x: not x),
    "~": (lambda x: not x),
    "or": (lambda x, y: x or y),
    "nor": (lambda x, y: not (x or y)),
    "xor": (lambda x, y: x != y),
    "and": (lambda x, y: x and y),
    "nand": (lambda x, y: not (x and y)),
    "=>": (lambda x, y: (not x) or y),
    "implies": (lambda x, y: (not x) or y),
    "=": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
}

# Lookup table for single-operand operations
SINGLE_OPERAND_OPS = ("not", "~", "-")

# Lookup table for double-operand operations
DOUBLE_OPERAND_OPS = ("and", "nand", "or", "nor", "xor", "=>", "implies", "=", "!=")


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


class BaseItemsRequired(Exception):
    """Exception raised when no base items are provided."""

    pass


class InvalidIndex(Exception):
    """Exception raised for out-of-bounds indexer."""

    pass


class Truths:
    """
    Class Truhts with modules for table formatting, valuation and CLI
    """

    def __init__(self, bases=None, phrases=None, ints=True, ascending=False):
        self.validate_bases(bases)
        self.initialize_variables(bases, phrases, ints)
        self.set_base_conditions(ascending)
        self.compile_regular_expressions()
        self.configure_parser()

    def validate_bases(self, bases):
        if not bases:
            raise BaseItemsRequired("Base items are required")

    def initialize_variables(self, bases, phrases, ints):
        self.bases = bases
        self.phrases = phrases or []
        self.ints = ints
        self.df = None

    def set_base_conditions(self, ascending):
        order = [False, True] if ascending else [True, False]
        self.base_conditions = list(itertools.product(order, repeat=len(self.bases)))

    def compile_regular_expressions(self):
        self.p = re.compile(r"(?<!\w)(" + "|".join(self.bases) + r")(?!\w)")

    def configure_parser(self):
        self.to_match = pyparsing.Word(pyparsing.alphanums)
        for item in itertools.chain(
            self.bases, [key for key, val in OPERATIONS.items()]
        ):
            self.to_match |= item
        self.parens = pyparsing.nestedExpr("(", ")", content=self.to_match)

    def calculate(self, *args):
        """
        Evaluates the logical value for each expression
        """
        bools = dict(zip(self.bases, args))

        eval_phrases = []
        for phrase in self.phrases:
            # substitute bases in phrase with boolean values as strings
            phrase = self.p.sub(
                lambda match_: str(bools[match_.group(0)]), phrase
            )  # NOQA long line
            # wrap phrase in parens
            phrase = "(" + phrase + ")"
            # parse the expression using pyparsing
            interpreted = self.parens.parseString(phrase).asList()[0]
            # convert any 'True' or 'False' to boolean values
            interpreted = recursive_map(string_to_bool, interpreted)
            # group operations
            interpreted = group_operations(interpreted)
            # evaluate the phrase
            eval_phrases.append(solve_phrase(interpreted))

        # add the bases and evaluated phrases to create a single row
        row = [val for key, val in bools.items()] + eval_phrases
        if self.ints:
            row = [int(c) for c in row]
        return row

    def as_prettytable(self):
        """
        Returns table using PrettyTable package
        """
        table = PrettyTable(self.bases + self.phrases)
        for conditions_set in self.base_conditions:
            table.add_row(self.calculate(*conditions_set))
        return table

    @property
    def as_pandas(self):
        """
        Table as Pandas DataFrame
        """
        if self.df is None:  # Only generate DataFrame if it hasn't been generated yet
            df_columns = self.bases + self.phrases
            self.df = pd.DataFrame(columns=df_columns)
            for conditions_set in self.base_conditions:
                self.df.loc[len(self.df)] = self.calculate(*conditions_set)
            self.df.index = range(1, len(self.df) + 1)  # index starting in one
        return self.df

    def as_tabulate(self, index=True, table_format="psql", align="center"):
        """
        Returns table using tabulate package
        """
        df = self.as_pandas
        table = tabulate(
            df,
            headers="keys",
            tablefmt=table_format,
            showindex=index,
            colalign=[align] * (len(df.columns) + index),
            disable_numparse=True,
        )
        return table

    def valuation(self, col_number=-1):
        """
        Evaluates an expression in a table column as a tautology, a
        contradiction or a contingency
        """

        df = self.as_pandas
        if col_number == -1:
            pass
        elif col_number not in range(1, len(df.columns) + 1):
            raise InvalidIndex("Indexer is out-of-bounds")
        else:
            col_number = col_number - 1

        if sum(df.iloc[:, col_number]) == len(df):
            val = "Tautology"
        elif sum(df.iloc[:, col_number]) == 0:
            val = "Contradiction"
        else:
            val = "Contingency"
        return val

    def __str__(self):
        table = Truths.as_tabulate(self, index=False)
        return str(table)


def main():
    table = Truths(["p"], ints=False)
    print(table)

    # criando um dataframe com uma coluna com True e False
    df = pd.DataFrame({"p": [True, False]})
    print(df)

    print(
        tabulate(
            df, headers="keys", tablefmt="psql", showindex=False, disable_numparse=True
        )
    )

    print(table.as_prettytable())


if __name__ == "__main__":
    main()
