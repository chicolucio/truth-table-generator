#!/usr/bin/env python
#
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

import itertools
import re
from prettytable import PrettyTable
import pyparsing
import pandas as pd
import numpy as np
from tabulate import tabulate

# dict of boolean operations
operations = {
    'not':      (lambda x: not x),
    '-':        (lambda x: not x),
    '~':        (lambda x: not x),

    'or':       (lambda x, y: x or y),
    'nor':      (lambda x, y: not (x or y)),
    'xor':      (lambda x, y: x != y),

    'and':      (lambda x, y: x and y),
    'nand':     (lambda x, y: not (x and y)),
    'xand':     (lambda x, y: not (x and y)),

    '=>':       (lambda x, y: (not x) or y),
    'implies':  (lambda x, y: (not x) or y),

    '=':        (lambda x, y: x == y),
    '!=':       (lambda x, y: x != y),
}


def recursive_map(func, data):
    """Recursively applies a map function to a list and all sublists."""
    if isinstance(data, list):
        return [recursive_map(func, elem) for elem in data]
    else:
        return func(data)


def string_to_bool(s):
    """Converts a string to boolean if string is either 'True' or 'False'
    otherwise returns it unchanged.
    """
    if s == 'True':
        return True
    elif s == 'False':
        return False
    return s


def solve_phrase(p):
    """Recursively evaluates a logical phrase that has been grouped into
    sublists where each list is one operation.
    """
    if isinstance(p, bool):
        return p
    if isinstance(p, list):
        # list with just a list in it
        if len(p) == 1:
            return solve_phrase(p[0])
        # single operand operation
        if len(p) == 2:
            return operations[p[0]](solve_phrase(p[1]))
        # double operand operation
        else:
            return operations[p[1]](solve_phrase(p[0]), solve_phrase([p[2]]))


def group_operations(p):
    """Recursively groups logical operations into seperate lists based on
    the order of operations such that each list is one operation.

    Order of operations is:
        not, and, or, implication
    """
    if isinstance(p, list):
        if len(p) == 1:
            return p
        for x in ['not', '~', '-']:
            while x in p:
                index = p.index(x)
                p[index] = [x, group_operations(p[index+1])]
                p.pop(index+1)
        for x in ['and', 'nand', 'xand']:
            while x in p:
                index = p.index(x)
                p[index] = [group_operations(p[index-1]),
                            x,
                            group_operations(p[index+1])]
                p.pop(index+1)
                p.pop(index-1)
        for x in ['or', 'nor', 'xor']:
            while x in p:
                index = p.index(x)
                p[index] = [group_operations(p[index-1]),
                            x,
                            group_operations(p[index+1])]
                p.pop(index+1)
                p.pop(index-1)
    return p


class Truths(object):
    def __init__(self, bases=None, phrases=None, ints=True):
        if not bases:
            raise Exception('Base items are required')
        self.bases = bases
        self.phrases = phrases or []
        self.ints = ints

        # generate the sets of booleans for the bases
        self.base_conditions = list(itertools.product([True, False],
                                                      repeat=len(bases)))

        # regex to match whole words defined in self.bases
        # used to add object context to variables in self.phrases
        self.p = re.compile(r'(?<!\w)(' + '|'.join(self.bases) + r')(?!\w)')

        # uesd for parsing logical operations and parenthesis
        self.to_match = pyparsing.Word(pyparsing.alphanums)
        for item in itertools.chain(self.bases,
                                    [key for key, val in operations.items()]):
            self.to_match |= item
        self.parens = pyparsing.nestedExpr('(', ')', content=self.to_match)

    def calculate(self, *args):
        bools = dict(zip(self.bases, args))

        eval_phrases = []
        for phrase in self.phrases:
            # substitute bases in phrase with boolean values as strings
            phrase = self.p.sub(lambda match: str(bools[match.group(0)]), phrase) # NOQA long line
            # wrap phrase in parens
            phrase = '(' + phrase + ')'
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
            return [int(c) for c in row]
        else:
            return row

    def asPrettyTable(self) -> PrettyTable:
        t = PrettyTable(self.bases + self.phrases)
        for conditions_set in self.base_conditions:
            t.add_row(self.calculate(*conditions_set))
        return t

    def asPandas(self):
        df_columns = self.bases + self.phrases
        df = pd.DataFrame(columns=df_columns)
        for conditions_set in self.base_conditions:
            df.loc[len(df)] = self.calculate(*conditions_set)
        df.index = np.arange(1, len(df) + 1)  # index starting in one
        return df

    def asTabulate(self, index=True, table_format='psql', align='center'):
        t = tabulate(Truths.asPandas(self),
                     headers='keys',
                     tablefmt=table_format,
                     showindex=index,
                     colalign=[align] * (len(Truths.asPandas(self).columns) + index)
                     )
        return t

    def __str__(self):
        t = PrettyTable(self.bases + self.phrases)
        for conditions_set in self.base_conditions:
            t.add_row(self.calculate(*conditions_set))
        return str(t)
