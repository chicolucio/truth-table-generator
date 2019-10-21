# truth-table-generator

**truth-table-generator** is a tool that allows to generate a truth table.
It is a fork of *truths* by [tr3buchet](https://github.com/tr3buchet/truths).

![Multiple outputs](https://raw.githubusercontent.com/chicolucio/truth-table-generator/master/images/ttg_small.png)

It merges some of the pull requests in the original and other external helpers.
The following are some of the changes and enhancements from the original:

- [tabulate](https://github.com/astanin/python-tabulate) instead of obsolete
[prettytable](https://code.google.com/archive/p/prettytable/) as main tool to
represent tabular data in ASCII tables (PrettyTable version is still available).
    - so there are many table formats available as such LaTeX, Org Tables, HTML
    and all others cited on [tabulate docs](https://github.com/astanin/python-tabulate)
- the table is now a Pandas DataFrame so you can make the output more visually
appealing with [Pandas Styling](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html).
See examples below.
- new function `valuation` that eval a proposition as a tautology, contradiction
or contingency.
- new command line interface (CLI) for printing a truth table from terminal.

## Installation

`pip install truth-table-generator`


## Usage

### Importing and syntax

First, let's import the package. `ttg` stands for *truth-table-generator*.

```python
import ttg
```

A truth table has one column for each input variable (for example, *p* and *q*),
and one final column showing all of the possible results of the logical
operation that the table represents. If the input has only one list of strings,
each string is considered an input variable:

```python
print(ttg.Truths(['p', 'q', 'r']))
```
```
+-----+-----+-----+
|  p  |  q  |  r  |
|-----+-----+-----|
|  1  |  1  |  1  |
|  1  |  1  |  0  |
|  1  |  0  |  1  |
|  1  |  0  |  0  |
|  0  |  1  |  1  |
|  0  |  1  |  0  |
|  0  |  0  |  1  |
|  0  |  0  |  0  |
+-----+-----+-----+
```

A second list of strings can be passed with propositional expressions created
with logical operators.

```python
print(ttg.Truths(['p', 'q', 'r'], ['p and q and r', 'p or q or r', '(p or (~q)) => r']))
```
```
+-----+-----+-----+-----------------+---------------+--------------------+
|  p  |  q  |  r  |  p and q and r  |  p or q or r  |  (p or (~q)) => r  |
|-----+-----+-----+-----------------+---------------+--------------------|
|  1  |  1  |  1  |        1        |       1       |         1          |
|  1  |  1  |  0  |        0        |       1       |         0          |
|  1  |  0  |  1  |        0        |       1       |         1          |
|  1  |  0  |  0  |        0        |       1       |         0          |
|  0  |  1  |  1  |        0        |       1       |         1          |
|  0  |  1  |  0  |        0        |       1       |         1          |
|  0  |  0  |  1  |        0        |       1       |         1          |
|  0  |  0  |  0  |        0        |       0       |         0          |
+-----+-----+-----+-----------------+---------------+--------------------+
```

### Operators and their representations:

- *negation*: `'not'`, `'-'`, `'~'`
- *logical disjunction*: `'or'`
- *logical nor*: `'nor'`
- *exclusive disjunction*: `'xor'`, `'!='`
- *logical conjunction*:  `'and'`
- *logical NAND*: `'nand'`
- *material implication*: `'=>'`, `'implies'`
- *logical biconditional*: `'='`

**Note**: Use parentheses! Especially with the negation operator. Use tables
above and below as reference. Although precedence rules are used, sometimes
precedence between conjunction and disjunction is unspecified requiring to
 provide it explicitly in given formula with parentheses.

### Showing words (True / False)

If you prefer the words True and False instead of numbers 0 and 1, there is a
third parameter, boolean type, `ints` that can be set to `False`:

```python
print(ttg.Truths(['p', 'q'], ['p and q', 'p or q', '(p or (~q)) => (~p)'], ints=False))
```
```
+-------+-------+-----------+----------+-----------------------+
|   p   |   q   |  p and q  |  p or q  |  (p or (~q)) => (~p)  |
|-------+-------+-----------+----------+-----------------------|
| True  | True  |   True    |   True   |         False         |
| True  | False |   False   |   True   |         False         |
| False | True  |   False   |   True   |         True          |
| False | False |   False   |  False   |         True          |
+-------+-------+-----------+----------+-----------------------+
```

### Formatting options with PrettyTable and Tabulate

For more formatting options, let's create a truth table variable:
```python
table = ttg.Truths(['p', 'q'], ['p => q', 'p = q'])
```
The command `print(table)` renders the standard table as seen on above examples:
```
+-----+-----+----------+---------+
|  p  |  q  |  p => q  |  p = q  |
|-----+-----+----------+---------|
|  1  |  1  |    1     |    1    |
|  1  |  0  |    0     |    0    |
|  0  |  1  |    1     |    0    |
|  0  |  0  |    1     |    1    |
+-----+-----+----------+---------+
```
The command `print(table.as_prettytable())` renders the table with PrettyTable
package as on the original version of this package:
```
+---+---+--------+-------+
| p | q | p => q | p = q |
+---+---+--------+-------+
| 1 | 1 |   1    |   1   |
| 1 | 0 |   0    |   0   |
| 0 | 1 |   1    |   0   |
| 0 | 0 |   1    |   1   |
+---+---+--------+-------+
```
As can be seen, the PrettyTable output has less blank spaces. However, the
PrettyTable package has much less output options and it is deprecated. So I
decided to use the Tabulate package as standard.

The command `print(table.as_tabulate())` renders the table with Tabulate
package. The first column presents line numbers (that can be disabled with
the parameter `index=False`):
```
+----+-----+-----+----------+---------+
|    |  p  |  q  |  p => q  |  p = q  |
|----+-----+-----+----------+---------|
| 1  |  1  |  1  |    1     |    1    |
| 2  |  1  |  0  |    0     |    0    |
| 3  |  0  |  1  |    1     |    0    |
| 4  |  0  |  0  |    1     |    1    |
+----+-----+-----+----------+---------+
```

Using Tabulate, we can use any of the formats available. Let's output a LaTeX
table without the line number column:

```python
print(table.as_tabulate(index=False, table_format='latex'))
```
```
\begin{tabular}{cccc}
\hline
  p  &  q  &  p =\ensuremath{>} q  &  p = q  \\
\hline
  1  &  1  &    1     &    1    \\
  1  &  0  &    0     &    0    \\
  0  &  1  &    1     &    0    \\
  0  &  0  &    1     &    1    \\
\hline
\end{tabular}
```

### Formatting options with Pandas

With an IPython terminal or a Jupyter Notebook, it is possible to render a Pandas
DataFrame with `table.as_pandas()`:

![pandas01](https://raw.githubusercontent.com/chicolucio/truth-table-generator/master/images/pandas01.png)

And this output can be modified with Pandas Styling

![pandas02](https://raw.githubusercontent.com/chicolucio/truth-table-generator/master/images/pandas02.png)

More advanced modifications can be done with functions that apply styling changes.
See the [styles tutorial notebook](styling_tutorial.ipynb) for examples.
See the image below for a fancy example with two lines and two columns
highlighted with yellow background and different colors for True and False.

![pandas03](https://raw.githubusercontent.com/chicolucio/truth-table-generator/master/images/pandas03.png)

### The `valuation` function

Let's see the how to use the `valuation` function with a new truth table:
```python
table_val = ttg.Truths(['p', 'q'], ['p = q', 'p and (~p)', '(p and q) => p'])
print(table_val)
```
```
+-----+-----+---------+--------------+------------------+
|  p  |  q  |  p = q  |  p and (~p)  |  (p and q) => p  |
|-----+-----+---------+--------------+------------------|
|  1  |  1  |    1    |      0       |        1         |
|  1  |  0  |    0    |      0       |        1         |
|  0  |  1  |    0    |      0       |        1         |
|  0  |  0  |    1    |      0       |        1         |
+-----+-----+---------+--------------+------------------+
```
Without arguments, the `valuation` function classifies the *last column* as a
tautology, a contradiction or a contingency:
```python
table_val.valuation()
```
```
'Tautology'
```
If a integer is used as argument, the function classifies the correspondent
column:
```python
table_val.valuation(3)
```
```
'Contingency'
```
```python
table_val.valuation(4)
```
```
'Contradiction'
```

### CLI utility

For those who work in the terminal there is a simple command line interface
(CLI) for printing tables. The script name is `ttg_cly.py` and it accepts
the following syntax according to its `--help`:

```
usage: ttg_cli.py [-h] [-p PROPOSITIONS] [-i INTS] variables

positional arguments:
  variables             List of variables e. g. "['p', 'q']"

optional arguments:
  -h, --help            show this help message and exit
  -p PROPOSITIONS, --propositions PROPOSITIONS
                        List of propositions e. g. "['p or q', 'p and q']"
  -i INTS, --ints INTS  True for 0 and 1; False for words
```

As seen, the list of variables is mandatory. Note that the lists must be between
`"`.

```bash
$ ttg_cli.py "['p', 'q', 'r']"
```
```
+-----+-----+-----+
|  p  |  q  |  r  |
|-----+-----+-----|
|  1  |  1  |  1  |
|  1  |  1  |  0  |
|  1  |  0  |  1  |
|  1  |  0  |  0  |
|  0  |  1  |  1  |
|  0  |  1  |  0  |
|  0  |  0  |  1  |
|  0  |  0  |  0  |
+-----+-----+-----+
```

The CLI utility also has an option, `-i`, to show words instead of numbers:
```bash
$ ttg_cli.py "['p', 'q', 'r']" -i False
```
```
+-------+-------+-------+
|   p   |   q   |   r   |
|-------+-------+-------|
| True  | True  | True  |
| True  | True  | False |
| True  | False | True  |
| True  | False | False |
| False | True  | True  |
| False | True  | False |
| False | False | True  |
| False | False | False |
+-------+-------+-------+
```

A `-p` parameter must be before the propositions list:
```bash
$ ttg_cli.py "['p', 'q', 'r']" -p "['p or q', 'p and q or r']"
```
```
+-----+-----+-----+----------+----------------+
|  p  |  q  |  r  |  p or q  |  p and q or r  |
|-----+-----+-----+----------+----------------|
|  1  |  1  |  1  |    1     |       1        |
|  1  |  1  |  0  |    1     |       1        |
|  1  |  0  |  1  |    1     |       1        |
|  1  |  0  |  0  |    1     |       0        |
|  0  |  1  |  1  |    1     |       1        |
|  0  |  1  |  0  |    1     |       0        |
|  0  |  0  |  1  |    0     |       1        |
|  0  |  0  |  0  |    0     |       0        |
+-----+-----+-----+----------+----------------+
```

With words instead of numbers:

```bash
$ ttg_cli.py "['p', 'q', 'r']" -p "['p or q', 'p and q or r']" -i False
```
```
+-------+-------+-------+----------+----------------+
|   p   |   q   |   r   |  p or q  |  p and q or r  |
|-------+-------+-------+----------+----------------|
| True  | True  | True  |   True   |      True      |
| True  | True  | False |   True   |      True      |
| True  | False | True  |   True   |      True      |
| True  | False | False |   True   |     False      |
| False | True  | True  |   True   |      True      |
| False | True  | False |   True   |     False      |
| False | False | True  |  False   |      True      |
| False | False | False |  False   |     False      |
+-------+-------+-------+----------+----------------+
```

The real look of the table depends on your terminal appearance configuration.
The green on black background screenshots from the first picture of this README
are from my terminal.

## Contributing

All contributions are welcome.

**Issues**

Feel free to submit issues regarding:

- recommendations
- more examples for the tutorial
- enhancement requests and new useful features
- code bugs

**Pull requests**

- before starting to work on your pull request, please submit an issue first
- fork the repo
- clone the project to your own machine
- commit changes to your own branch
- push your work back up to your fork
- submit a pull request so that your changes can be reviewed


## License

Apache 2.0, see [LICENSE](LICENSE)

## Citing

If you use *truth-table-generator* in a scientific publication or in classes,
please consider citing as

F. L. S. Bustamante, *truth-table-generator* - generating truth tables., 2019 -
Available at: https://github.com/chicolucio/truth-table-generator

## Funding

If you enjoy this project and would like to see many more math and science
related programming projects, I would greatly appreciate any assistance. Send me
an e-mail to know how to assist. Many more projects are to come and your support
will be rewarded with more STEM coding projects :-)
