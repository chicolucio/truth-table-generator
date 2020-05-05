# flake8: noqa

from ttg.ttg import Truths
import pytest


def test_no_base_exception():
    with pytest.raises(Exception) as excinfo:
        Truths()
    assert 'Base items are required' in str(excinfo.value)


def test_no_propositions_default():
    table = Truths(['p', 'q', 'r', 's'])
    assert str(table) == \
        ("""+-----+-----+-----+-----+
|  p  |  q  |  r  |  s  |
|-----+-----+-----+-----|
|  1  |  1  |  1  |  1  |
|  1  |  1  |  1  |  0  |
|  1  |  1  |  0  |  1  |
|  1  |  1  |  0  |  0  |
|  1  |  0  |  1  |  1  |
|  1  |  0  |  1  |  0  |
|  1  |  0  |  0  |  1  |
|  1  |  0  |  0  |  0  |
|  0  |  1  |  1  |  1  |
|  0  |  1  |  1  |  0  |
|  0  |  1  |  0  |  1  |
|  0  |  1  |  0  |  0  |
|  0  |  0  |  1  |  1  |
|  0  |  0  |  1  |  0  |
|  0  |  0  |  0  |  1  |
|  0  |  0  |  0  |  0  |
+-----+-----+-----+-----+""")


def test_no_propositions_ints_false():
    table = Truths(['p', 'q', 'r', 's'], ints=False)
    assert str(table) == \
        ("""+-------+-------+-------+-------+
|   p   |   q   |   r   |   s   |
|-------+-------+-------+-------|
| True  | True  | True  | True  |
| True  | True  | True  | False |
| True  | True  | False | True  |
| True  | True  | False | False |
| True  | False | True  | True  |
| True  | False | True  | False |
| True  | False | False | True  |
| True  | False | False | False |
| False | True  | True  | True  |
| False | True  | True  | False |
| False | True  | False | True  |
| False | True  | False | False |
| False | False | True  | True  |
| False | False | True  | False |
| False | False | False | True  |
| False | False | False | False |
+-------+-------+-------+-------+""")


def test_no_propositions_ascending_true():
    table = Truths(['p', 'q', 'r', 's'], ascending=True)
    assert str(table) == \
        ("""+-----+-----+-----+-----+
|  p  |  q  |  r  |  s  |
|-----+-----+-----+-----|
|  0  |  0  |  0  |  0  |
|  0  |  0  |  0  |  1  |
|  0  |  0  |  1  |  0  |
|  0  |  0  |  1  |  1  |
|  0  |  1  |  0  |  0  |
|  0  |  1  |  0  |  1  |
|  0  |  1  |  1  |  0  |
|  0  |  1  |  1  |  1  |
|  1  |  0  |  0  |  0  |
|  1  |  0  |  0  |  1  |
|  1  |  0  |  1  |  0  |
|  1  |  0  |  1  |  1  |
|  1  |  1  |  0  |  0  |
|  1  |  1  |  0  |  1  |
|  1  |  1  |  1  |  0  |
|  1  |  1  |  1  |  1  |
+-----+-----+-----+-----+""")


def test_all_operators():
    table = Truths(['p', 'q'], ['p and q', 'p or q', 'p => q',
                                'p = q', 'p xor q', 'p nand q', 'p nor q'])
    assert str(table) == \
        ("""+-----+-----+-----------+----------+----------+---------+-----------+------------+-----------+
|  p  |  q  |  p and q  |  p or q  |  p => q  |  p = q  |  p xor q  |  p nand q  |  p nor q  |
|-----+-----+-----------+----------+----------+---------+-----------+------------+-----------|
|  1  |  1  |     1     |    1     |    1     |    1    |     0     |     0      |     0     |
|  1  |  0  |     0     |    1     |    0     |    0    |     1     |     1      |     0     |
|  0  |  1  |     0     |    1     |    1     |    0    |     1     |     1      |     0     |
|  0  |  0  |     0     |    0     |    1     |    1    |     0     |     1      |     1     |
+-----+-----+-----------+----------+----------+---------+-----------+------------+-----------+""")


def test_neg_operators():
    table = Truths(['p', 'q'], ['p and (~q)', 'p and (-q)', 'p and (not q)'])
    assert str(table) == \
        ("""+-----+-----+--------------+--------------+-----------------+
|  p  |  q  |  p and (~q)  |  p and (-q)  |  p and (not q)  |
|-----+-----+--------------+--------------+-----------------|
|  1  |  1  |      0       |      0       |        0        |
|  1  |  0  |      1       |      1       |        1        |
|  0  |  1  |      0       |      0       |        0        |
|  0  |  0  |      0       |      0       |        0        |
+-----+-----+--------------+--------------+-----------------+""")


def test_xor_operators():
    table = Truths(['p', 'q'], ['p xor q', 'p != q'])
    assert str(table) == \
        ("""+-----+-----+-----------+----------+
|  p  |  q  |  p xor q  |  p != q  |
|-----+-----+-----------+----------|
|  1  |  1  |     0     |    0     |
|  1  |  0  |     1     |    1     |
|  0  |  1  |     1     |    1     |
|  0  |  0  |     0     |    0     |
+-----+-----+-----------+----------+""")


def test_implies_operators():
    table = Truths(['p', 'q'], ['p => q', 'p implies q'])
    assert str(table) == \
        ("""+-----+-----+----------+---------------+
|  p  |  q  |  p => q  |  p implies q  |
|-----+-----+----------+---------------|
|  1  |  1  |    1     |       1       |
|  1  |  0  |    0     |       0       |
|  0  |  1  |    1     |       1       |
|  0  |  0  |    1     |       1       |
+-----+-----+----------+---------------+""")


def test_valuation_tautology():
    table = Truths(['p', 'q'], ['(p and q) => (p or q)'])
    assert str(table) == \
        ("""+-----+-----+-------------------------+
|  p  |  q  |  (p and q) => (p or q)  |
|-----+-----+-------------------------|
|  1  |  1  |            1            |
|  1  |  0  |            1            |
|  0  |  1  |            1            |
|  0  |  0  |            1            |
+-----+-----+-------------------------+""")

    assert table.valuation() == 'Tautology'


def test_valuation_contingency():
    table = Truths(['p', 'q'], ['(p and (~q)) => q'])
    assert str(table) == \
        ("""+-----+-----+---------------------+
|  p  |  q  |  (p and (~q)) => q  |
|-----+-----+---------------------|
|  1  |  1  |          1          |
|  1  |  0  |          0          |
|  0  |  1  |          1          |
|  0  |  0  |          1          |
+-----+-----+---------------------+""")

    assert table.valuation() == 'Contingency'


def test_valuation_contradiction():
    table = Truths(['p'], ['p and (~p)'])
    assert str(table) == \
        ("""+-----+--------------+
|  p  |  p and (~p)  |
|-----+--------------|
|  1  |      0       |
|  0  |      0       |
+-----+--------------+""")
    table.valuation() == 'Contradiction'


def test_valuation_out_of_bounds_exception():
    table = Truths(['p'], ['p and (~p)'])
    with pytest.raises(Exception) as excinfo:
        table.valuation(-3)
    assert 'Indexer is out-of-bounds' in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        table.valuation(3)
    assert 'Indexer is out-of-bounds' in str(excinfo.value)


def test_tautologies_inference_rules():
    proposition01 = '(p and q) => p'
    proposition02 = 'p => (p or q)'
    proposition03 = '(p and (p => q)) => q'  # modus ponens
    proposition04 = '((p => q) and (~q)) => (~p)'  # modus tollens

    table = Truths(['p', 'q'], [proposition01, proposition02,
                                proposition03, proposition04])

    assert str(table) == \
        ("""+-----+-----+------------------+-----------------+-------------------------+-------------------------------+
|  p  |  q  |  (p and q) => p  |  p => (p or q)  |  (p and (p => q)) => q  |  ((p => q) and (~q)) => (~p)  |
|-----+-----+------------------+-----------------+-------------------------+-------------------------------|
|  1  |  1  |        1         |        1        |            1            |               1               |
|  1  |  0  |        1         |        1        |            1            |               1               |
|  0  |  1  |        1         |        1        |            1            |               1               |
|  0  |  0  |        1         |        1        |            1            |               1               |
+-----+-----+------------------+-----------------+-------------------------+-------------------------------+""")

    assert table.valuation(3) == 'Tautology'
    assert table.valuation(4) == 'Tautology'
    assert table.valuation(5) == 'Tautology'
    assert table.valuation(6) == 'Tautology'


def test_equivalence_morgan_01():
    de_morgan_law = Truths(['p', 'q'], ['~(p and q)', '(~p) or (~q)'])

    assert str(de_morgan_law) == \
        ("""+-----+-----+--------------+----------------+
|  p  |  q  |  ~(p and q)  |  (~p) or (~q)  |
|-----+-----+--------------+----------------|
|  1  |  1  |      0       |       0        |
|  1  |  0  |      1       |       1        |
|  0  |  1  |      1       |       1        |
|  0  |  0  |      1       |       1        |
+-----+-----+--------------+----------------+""")

    assert de_morgan_law.as_pandas(
    ).iloc[:, -1].equals(de_morgan_law.as_pandas().iloc[:, -2])


def test_equivalence_morgan_02():
    de_morgan_law = Truths(['p', 'q'], ['~(p or q)', '(~p) and (~q)'])

    assert str(de_morgan_law) == \
        ("""+-----+-----+-------------+-----------------+
|  p  |  q  |  ~(p or q)  |  (~p) and (~q)  |
|-----+-----+-------------+-----------------|
|  1  |  1  |      0      |        0        |
|  1  |  0  |      0      |        0        |
|  0  |  1  |      0      |        0        |
|  0  |  0  |      1      |        1        |
+-----+-----+-------------+-----------------+""")

    assert de_morgan_law.as_pandas(
    ).iloc[:, -1].equals(de_morgan_law.as_pandas().iloc[:, -2])


def test_equivalence_negated_conditional():
    neg_cond = Truths(['p', 'q'], ['~(p => q)', 'p and (~q)'])

    assert str(neg_cond) == \
        ("""+-----+-----+-------------+--------------+
|  p  |  q  |  ~(p => q)  |  p and (~q)  |
|-----+-----+-------------+--------------|
|  1  |  1  |      0      |      0       |
|  1  |  0  |      1      |      1       |
|  0  |  1  |      0      |      0       |
|  0  |  0  |      0      |      0       |
+-----+-----+-------------+--------------+""")

    assert neg_cond.as_pandas(
    ).iloc[:, -1].equals(neg_cond.as_pandas().iloc[:, -2])


def test_prettytable():
    table = Truths(['p', 'q'], ['p => q', 'p = q'])
    assert str(table.as_prettytable()) == \
        ("""+---+---+--------+-------+
| p | q | p => q | p = q |
+---+---+--------+-------+
| 1 | 1 |   1    |   1   |
| 1 | 0 |   0    |   0   |
| 0 | 1 |   1    |   0   |
| 0 | 0 |   1    |   1   |
+---+---+--------+-------+""")


def test_latex():
    table = Truths(['p', 'q'], ['p => q', 'p = q'])
    assert str(table.as_tabulate(index=False, table_format='latex')) == \
        (r"""\begin{tabular}{cccc}
\hline
  p  &  q  &  p =\ensuremath{>} q  &  p = q  \\
\hline
  1  &  1  &    1     &    1    \\
  1  &  0  &    0     &    0    \\
  0  &  1  &    1     &    0    \\
  0  &  0  &    1     &    1    \\
\hline
\end{tabular}""")


def test_case01():
    table = Truths(['p', 'q'], ['(p and q) => (p or q)'])
    assert str(table) == \
        ("""+-----+-----+-------------------------+
|  p  |  q  |  (p and q) => (p or q)  |
|-----+-----+-------------------------|
|  1  |  1  |            1            |
|  1  |  0  |            1            |
|  0  |  1  |            1            |
|  0  |  0  |            1            |
+-----+-----+-------------------------+""")


def test_case02():
    table = Truths(['p', 'q', 'r'], ['(p and q) or r'])
    assert str(table) == \
        ("""+-----+-----+-----+------------------+
|  p  |  q  |  r  |  (p and q) or r  |
|-----+-----+-----+------------------|
|  1  |  1  |  1  |        1         |
|  1  |  1  |  0  |        1         |
|  1  |  0  |  1  |        1         |
|  1  |  0  |  0  |        0         |
|  0  |  1  |  1  |        1         |
|  0  |  1  |  0  |        0         |
|  0  |  0  |  1  |        1         |
|  0  |  0  |  0  |        0         |
+-----+-----+-----+------------------+""")


def test_case03():
    table = Truths(['p', 'q'], ['~p', '~q', '(~p) or (~q)'])
    assert str(table) == \
        ("""+-----+-----+------+------+----------------+
|  p  |  q  |  ~p  |  ~q  |  (~p) or (~q)  |
|-----+-----+------+------+----------------|
|  1  |  1  |  0   |  0   |       0        |
|  1  |  0  |  0   |  1   |       1        |
|  0  |  1  |  1   |  0   |       1        |
|  0  |  0  |  1   |  1   |       1        |
+-----+-----+------+------+----------------+""")


def test_case04():
    table = Truths(['p', 'q', 'r'], ['((~p) nor q) and (q nand (~r))'])
    assert str(table) == \
        ("""+-----+-----+-----+----------------------------------+
|  p  |  q  |  r  |  ((~p) nor q) and (q nand (~r))  |
|-----+-----+-----+----------------------------------|
|  1  |  1  |  1  |                0                 |
|  1  |  1  |  0  |                0                 |
|  1  |  0  |  1  |                1                 |
|  1  |  0  |  0  |                1                 |
|  0  |  1  |  1  |                0                 |
|  0  |  1  |  0  |                0                 |
|  0  |  0  |  1  |                0                 |
|  0  |  0  |  0  |                0                 |
+-----+-----+-----+----------------------------------+""")
