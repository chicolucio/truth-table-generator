# truths - auto generate truth tables
truths is a simple tool that allows you to quickly generate a truth table from python variable names and phrases


## install
`pip install truths` or `git clone` and `pip install -e` to play with the code


### use is simple:
start by creating some base variables

```python
import truths
print truths.Truths(['a', 'b', 'x'])
```
```
+---+---+---+
| a | b | x |
+---+---+---+
| 0 | 0 | 0 |
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |
| 1 | 1 | 1 |
+---+---+---+
```


### add some phrases
now let's use those base variables and pass in some phrases!

```python
from truths import Truths
print Truths(['a', 'b', 'x', 'd'], ['(a and b)', 'a and b or x', 'a and (b or x) or d'])
```
```
+---+---+---+---+-----------+--------------+---------------------+
| a | b | x | d | (a and b) | a and b or x | a and (b or x) or d |
+---+---+---+---+-----------+--------------+---------------------+
| 0 | 0 | 0 | 0 |     0     |      0       |          0          |
| 0 | 0 | 0 | 1 |     0     |      0       |          1          |
| 0 | 0 | 1 | 0 |     0     |      1       |          0          |
| 0 | 0 | 1 | 1 |     0     |      1       |          1          |
| 0 | 1 | 0 | 0 |     0     |      0       |          0          |
| 0 | 1 | 0 | 1 |     0     |      0       |          1          |
| 0 | 1 | 1 | 0 |     0     |      1       |          0          |
| 0 | 1 | 1 | 1 |     0     |      1       |          1          |
| 1 | 0 | 0 | 0 |     0     |      0       |          0          |
| 1 | 0 | 0 | 1 |     0     |      0       |          1          |
| 1 | 0 | 1 | 0 |     0     |      1       |          1          |
| 1 | 0 | 1 | 1 |     0     |      1       |          1          |
| 1 | 1 | 0 | 0 |     1     |      1       |          1          |
| 1 | 1 | 0 | 1 |     1     |      1       |          1          |
| 1 | 1 | 1 | 0 |     1     |      1       |          1          |
| 1 | 1 | 1 | 1 |     1     |      1       |          1          |
+---+---+---+---+-----------+--------------+---------------------+
```


### prefer boolean words?
neat eh? if you prefer True/False over the numbers pass `ints=False`:

```python
from truths import Truths
print Truths(['a', 'b', 'x', 'd'], ['(a and b)', 'a and b or x', 'a and (b or x) or d'], ints=False)
```
```
+-------+-------+-------+-------+-----------+--------------+---------------------+
|   a   |   b   |   x   |   d   | (a and b) | a and b or x | a and (b or x) or d |
+-------+-------+-------+-------+-----------+--------------+---------------------+
| False | False | False | False |   False   |    False     |        False        |
| False | False | False |  True |   False   |    False     |         True        |
| False | False |  True | False |   False   |     True     |        False        |
| False | False |  True |  True |   False   |     True     |         True        |
| False |  True | False | False |   False   |    False     |        False        |
| False |  True | False |  True |   False   |    False     |         True        |
| False |  True |  True | False |   False   |     True     |        False        |
| False |  True |  True |  True |   False   |     True     |         True        |
|  True | False | False | False |   False   |    False     |        False        |
|  True | False | False |  True |   False   |    False     |         True        |
|  True | False |  True | False |   False   |     True     |         True        |
|  True | False |  True |  True |   False   |     True     |         True        |
|  True |  True | False | False |    True   |     True     |         True        |
|  True |  True | False |  True |    True   |     True     |         True        |
|  True |  True |  True | False |    True   |     True     |         True        |
|  True |  True |  True |  True |    True   |     True     |         True        |
+-------+-------+-------+-------+-----------+--------------+---------------------+
```


### how it works
check out the code! behind the scenes it's putting the bases in an object context and generating a grid of values for them. then, the phrases are `eval`uated in the object's context against each row in that grid of values
