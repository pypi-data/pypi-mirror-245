# pw_gen
## A simple password generator written in Python 3.11
### Usage
#### Options:
```python
pw_length = 16 # Length of the password (integer)
pw_type = "upper,lower,number,symbol,legible" # Type of the password (string)
```
#### Types:
```shell
upper = Uppercase letters
lower = Lowercase letters
number = Numbers
symbol = Symbols
legible = Legible characters (no 0, O, 1, l, I)
```
#### Example:
```python
from pw_gen import Password
pw = Password(pw_length=16, pw_type="upper,lower,number,special,legible")
print(pw.password())
```
#### Output:
```
Xy4@9#3$7%8&1!23
```
