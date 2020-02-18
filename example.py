import os
import functools
import configparser

file = 'D:/Code/editor/new-.xml'
if os.path.exists(file):
    print('yes')
else:
    print('no')