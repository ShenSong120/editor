import os
import functools
import configparser

file = 'D:/Code/editor/new.xml'
with open(file, 'r') as  f:
    text = f.read()
    print(text)