import sympy
import math
import random

print(sympy.isprime(5))

# Bob Private and Public Key Generation
p = sympy.randprime(1, 1000000)
q = sympy.randprime(1, 1000000)

print(p)
print(q)