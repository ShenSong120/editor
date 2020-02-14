import os
import functools
import configparser

def add(a, b, c):
    return a+b+c

p = functools.partial(add, 12)