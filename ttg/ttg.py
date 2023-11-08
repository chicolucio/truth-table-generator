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
from prettytable import PrettyTable
import pandas as pd
from tabulate import tabulate

from ttg.tools.evaluation import recursive_map
from ttg.tools.evaluation import string_to_bool
from ttg.tools.evaluation import solve_phrase
from ttg.tools.parsing import (
    compile_regular_expressions,
    configure_parser,
    group_operations,
)


class BaseItemsRequired(Exception):
    """Exception raised when no base items are provided."""

    pass


class InvalidIndex(Exception):
    """Exception raised for out-of-bounds indexer."""

    pass


class Truths:
    """
    Class Truths with modules for table formatting, valuation and CLI
    """

    def __init__(self, bases=None, phrases=None, ints=True, ascending=False):
        self.validate_bases(bases)
        self.initialize_variables(bases, phrases, ints)
        self.set_base_conditions(ascending)

    def validate_bases(self, bases):
        if not bases:
            raise BaseItemsRequired("Base items are required")

    def initialize_variables(self, bases, phrases, ints):
        self.bases = bases
        self.phrases = phrases or []
        self.ints = ints
        self.df = None
        self.p = compile_regular_expressions(self.bases)
        self.parens = configure_parser(self.bases)

    def set_base_conditions(self, ascending):
        order = [False, True] if ascending else [True, False]
        self.base_conditions = list(itertools.product(order, repeat=len(self.bases)))

    def evaluate_phrase(self, phrase, bools):
        """
        Evaluate a single logical phrase based on the boolean values provided.

        Parameters:
            phrase (str): The logical phrase to be evaluated.
            bools (dict): A dictionary containing the boolean values for base variables.

        Returns:
            bool: The result of the logical expression.
        """
        # Substitute bases in phrase with boolean values as strings
        substituted_phrase = self.p.sub(
            lambda match_: str(bools[match_.group(0)]), phrase
        )

        # Wrap phrase in parens
        wrapped_phrase = f"({substituted_phrase})"

        # Parse the expression using pyparsing
        interpreted = self.parens.parseString(wrapped_phrase).asList()[0]

        # Convert any 'True' or 'False' to boolean values
        interpreted = recursive_map(string_to_bool, interpreted)

        # Group operations
        interpreted = group_operations(interpreted)

        # Evaluate the phrase
        return solve_phrase(interpreted)

    def calculate(self, *args):
        """
        Evaluates the logical value for each expression
        """
        bools = dict(zip(self.bases, args))

        # Evaluate each phrase
        eval_phrases = [self.evaluate_phrase(phrase, bools) for phrase in self.phrases]

        # Create a single row with base variables and the evaluated phrases
        row = list(bools.values()) + eval_phrases

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
