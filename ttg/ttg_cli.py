#!/usr/bin/env python

"""
CLI for the truth_table_generator package.
"""

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

import argparse
import ast

import ttg


def str2bool(value):
    """Convert a string representation of a boolean to a boolean type."""
    if isinstance(value, bool):
        return value
    if value.lower() in {"yes", "true", "t", "y", "1"}:
        return True
    elif value.lower() in {"no", "false", "f", "n", "0"}:
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def clielement():
    """
    Command Line Interface (CLI) for the truth_table_generator package.
    """
    parser = argparse.ArgumentParser(description="Generate truth tables.")
    parser.add_argument(
        "variables", type=str, help="List of variables e.g., \"['p', 'q']\""
    )
    parser.add_argument(
        "-p",
        "--propositions",
        type=str,
        default="[]",
        help="List of propositions e.g., \"['p or q', 'p and q']\"",
    )
    parser.add_argument(
        "-i",
        "--ints",
        type=str2bool,
        default=True,
        help="Use integers for boolean values. True for 0 and 1; False for words.",
    )
    parser.add_argument(
        "-a",
        "--ascending",
        type=str2bool,
        default=False,
        help="Sort output in ascending order. True for reverse output (False before True).",  # noqa: E501
    )

    args = parser.parse_args()

    try:
        variables = ast.literal_eval(args.variables)
        propositions = ast.literal_eval(args.propositions)
    except Exception as e:
        print(f"Error: {e}")
        return

    print()
    print(ttg.Truths(variables, propositions, args.ints, args.ascending))
    print()


if __name__ == "__main__":
    clielement()
