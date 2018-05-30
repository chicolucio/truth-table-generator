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
from prettytable import PrettyTable
import re


class Truths(object):
    def __init__(self, bases=None, phrases=None, ints=True):
        if not bases:
            raise Exception('Base items are required')
        self.bases = bases
        self.phrases = phrases or []
        self.ints = ints

        # generate the sets of booleans for the bases
        self.base_conditions = list(itertools.product([False, True],
                                                      repeat=len(bases)))

        # regex to match whole words defined in self.bases
        # used to add object context to variables in self.phrases
        self.p = re.compile(r'(?<!\w)(' + '|'.join(self.bases) + ')(?!\w)')

    def calculate(self, *args):
        bools = dict(zip(self.bases, args))
        # substitute bases with boolean values in self.phrases then evaluate
        # each phrase
        eval_phrases = []
        for phrase in self.phrases:
            phrase = self.p.sub(lambda match: str(bools[match.group(0)]), phrase)
            eval_phrases.append(eval(phrase))

        # add the bases and evaluated phrases to create a single row
        row = [val for key, val in bools.items()] + eval_phrases
        if self.ints:
            return [int(c) for c in row]
        else:
            return row

    def __str__(self):
        t = PrettyTable(self.bases + self.phrases)
        for conditions_set in self.base_conditions:
            t.add_row(self.calculate(*conditions_set))
        return str(t)
