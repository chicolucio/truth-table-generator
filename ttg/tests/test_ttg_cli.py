# flake8: noqa

from ttg.ttg_cli import clielement
import sys


def run(variables, propositions, ints, asc, capsys, monkeypatch):
    if propositions is None:
        monkeypatch.setattr(
            sys, 'argv', ['ttg_cly.py', variables, ints, asc])
    else:
        monkeypatch.setattr(
            sys, 'argv', ['ttg_cly.py', variables, propositions, ints, asc])
    clielement()
    out, _ = capsys.readouterr()
    return out


def test_no_props_defaults(capsys, monkeypatch):
    assert run("['p','q','r']", None, "-iTrue", "-aFalse", capsys, monkeypatch) == """
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

"""


def test_no_props_ints_false(capsys, monkeypatch):
    assert run("['p','q','r']", None, "-iFalse", "-aFalse", capsys, monkeypatch) == """
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

"""


def test_no_props_asc_true(capsys, monkeypatch):
    assert run("['p','q','r']", None, "-iTrue", "-aTrue", capsys, monkeypatch) == """
+-----+-----+-----+
|  p  |  q  |  r  |
|-----+-----+-----|
|  0  |  0  |  0  |
|  0  |  0  |  1  |
|  0  |  1  |  0  |
|  0  |  1  |  1  |
|  1  |  0  |  0  |
|  1  |  0  |  1  |
|  1  |  1  |  0  |
|  1  |  1  |  1  |
+-----+-----+-----+

"""


def test_no_props_int_false_asc_true(capsys, monkeypatch):
    assert run("['p','q','r']", None, "-iFalse", "-aTrue", capsys, monkeypatch) == """
+-------+-------+-------+
|   p   |   q   |   r   |
|-------+-------+-------|
| False | False | False |
| False | False | True  |
| False | True  | False |
| False | True  | True  |
| True  | False | False |
| True  | False | True  |
| True  | True  | False |
| True  | True  | True  |
+-------+-------+-------+

"""


def test_all_operators(capsys, monkeypatch):
    assert run("['p','q']", "-p['p and q', 'p or q', 'p => q', 'p = q', 'p xor q', 'p nand q', 'p nor q']", "-iTrue", "-aFalse", capsys, monkeypatch) == """
+-----+-----+-----------+----------+----------+---------+-----------+------------+-----------+
|  p  |  q  |  p and q  |  p or q  |  p => q  |  p = q  |  p xor q  |  p nand q  |  p nor q  |
|-----+-----+-----------+----------+----------+---------+-----------+------------+-----------|
|  1  |  1  |     1     |    1     |    1     |    1    |     0     |     0      |     0     |
|  1  |  0  |     0     |    1     |    0     |    0    |     1     |     1      |     0     |
|  0  |  1  |     0     |    1     |    1     |    0    |     1     |     1      |     0     |
|  0  |  0  |     0     |    0     |    1     |    1    |     0     |     1      |     1     |
+-----+-----+-----------+----------+----------+---------+-----------+------------+-----------+

"""


def test_neg_operators(capsys, monkeypatch):
    assert run("['p', 'q']", "-p['p and (~q)', 'p and (-q)', 'p and (not q)']", "-iTrue", "-aFalse", capsys, monkeypatch) == """
+-----+-----+--------------+--------------+-----------------+
|  p  |  q  |  p and (~q)  |  p and (-q)  |  p and (not q)  |
|-----+-----+--------------+--------------+-----------------|
|  1  |  1  |      0       |      0       |        0        |
|  1  |  0  |      1       |      1       |        1        |
|  0  |  1  |      0       |      0       |        0        |
|  0  |  0  |      0       |      0       |        0        |
+-----+-----+--------------+--------------+-----------------+

"""


def test_xor_operators(capsys, monkeypatch):
    assert run("['p', 'q']", "-p['p xor q', 'p != q']", "-iTrue", "-aFalse", capsys, monkeypatch) == """
+-----+-----+-----------+----------+
|  p  |  q  |  p xor q  |  p != q  |
|-----+-----+-----------+----------|
|  1  |  1  |     0     |    0     |
|  1  |  0  |     1     |    1     |
|  0  |  1  |     1     |    1     |
|  0  |  0  |     0     |    0     |
+-----+-----+-----------+----------+

"""


def test_implies_operators(capsys, monkeypatch):
    assert run("['p', 'q']", "-p['p => q', 'p implies q']", "-iTrue", "-aFalse", capsys, monkeypatch) == """
+-----+-----+----------+---------------+
|  p  |  q  |  p => q  |  p implies q  |
|-----+-----+----------+---------------|
|  1  |  1  |    1     |       1       |
|  1  |  0  |    0     |       0       |
|  0  |  1  |    1     |       1       |
|  0  |  0  |    1     |       1       |
+-----+-----+----------+---------------+

"""


def test_case_01(capsys, monkeypatch):
    assert run("['p', 'q', 'r']", "-p['~p', '~q', '~r', 'p and (~q)', '(~p) or (~q)', '(p and (~q)) or (~r)', '((~p) or q) and r', '((p and (~q)) or (~r)) and (((~p) or q) and r)']", "-iTrue", "-aFalse", capsys, monkeypatch) == """
+-----+-----+-----+------+------+------+--------------+----------------+------------------------+---------------------+--------------------------------------------------+
|  p  |  q  |  r  |  ~p  |  ~q  |  ~r  |  p and (~q)  |  (~p) or (~q)  |  (p and (~q)) or (~r)  |  ((~p) or q) and r  |  ((p and (~q)) or (~r)) and (((~p) or q) and r)  |
|-----+-----+-----+------+------+------+--------------+----------------+------------------------+---------------------+--------------------------------------------------|
|  1  |  1  |  1  |  0   |  0   |  0   |      0       |       0        |           0            |          1          |                        0                         |
|  1  |  1  |  0  |  0   |  0   |  1   |      0       |       0        |           1            |          0          |                        0                         |
|  1  |  0  |  1  |  0   |  1   |  0   |      1       |       1        |           1            |          0          |                        0                         |
|  1  |  0  |  0  |  0   |  1   |  1   |      1       |       1        |           1            |          0          |                        0                         |
|  0  |  1  |  1  |  1   |  0   |  0   |      0       |       1        |           0            |          1          |                        0                         |
|  0  |  1  |  0  |  1   |  0   |  1   |      0       |       1        |           1            |          0          |                        0                         |
|  0  |  0  |  1  |  1   |  1   |  0   |      0       |       1        |           0            |          1          |                        0                         |
|  0  |  0  |  0  |  1   |  1   |  1   |      0       |       1        |           1            |          0          |                        0                         |
+-----+-----+-----+------+------+------+--------------+----------------+------------------------+---------------------+--------------------------------------------------+

"""
