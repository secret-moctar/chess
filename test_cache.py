import sys
from functools import lru_cache
from abc import ABC, abstractmethod

@lru_cache(maxsize=None)
def fib(n: int):
    if n < 0: raise TypeError("Fib of a negative number is fucked up")
    if n < 2: return 1
    return fib(n - 1) + fib(n - 2)


def fib_me(n: int, memo={}):
    if n < 0: raise TypeError("Fib of a negative number is fucked up")
    if n < 2: return 1
    if n in memo: return memo[n]
    memo[n] = fib_me(n - 1, memo=memo) + fib_me(n - 2, memo=memo)
    return memo[n]

print(fib(int(sys.argv[1])))
print("############ Another answer ###########")
print(fib_me(int(sys.argv[1])))
