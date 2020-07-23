# NLP toy data generator

This repository contains a utility for generating toy data suitable for development of NLP models.
The idea is to create sequences that satisfy the following properties: 
- vocabulary size is very small and limited (no unknown words to be encountered at test time)
- there is an infinite supply of possible sensible combinations (even with a small vocabulary)
- sequences posses some trivial syntactic rules that the model can learn
- sequences of one language can be translated to other language via a set of not too ambiguous rules

### Setup

1. clone, cd to the directory, install dependencies if you need them (``` pip install requirements.txt ``` only numpy atm)
2. in a python file or a notebook, execute ```import math_expressions as me``` to import the module
3. generate expressions with ```me.generate_nested_expression()```, ```me.generate_simple_expression()```, or translate numbers up to (1e12)-1 in magnitude (billions) to english words with ```me.num2word(x)```

## Math expressions

This module implements a generator of mathematical expressions. There are 2 versions - nested with extended operations and sequential with +,-,\*, and / only.

### Nested expressions usage
Note: prevents most pitfalls such as complex numbers, division by zero, and numerical explosion due to high exponents. However, it still happens sometimes.
```
ex = me.generate_nested_expression()
print("Expression: ", ex)
ex_res = ex.compute()
print("Result: ", ex_res)
print(ex.to_word())
```
Outputs:
```
Expression:  ((-0.57)-((-5.67)/((7.09+(-2.23))+9.1)))
Result:  -0.16383954154727787
minus zero point sixteen
```

### Sequential expressions usage
Note: does not check for division by 0.
```
ex = me.generate_simple_expression()
print("Expression: ", ex)
print("= {}".format(eval(ex)))
print("In words: ", me.num2word(eval(ex)))
```
Outputs:
```
Expression:  5 / -5 / -2 / -8 - 5
= -5.0625
In words:  minus five point zero five
```

## Other generators and plans
I plan to implement some other generators too, e.g. an equation generator, some form of dialogue generator with personas, etc. 
I also want to create the generators for more languages, so that they can be used for machine translation modelling.
