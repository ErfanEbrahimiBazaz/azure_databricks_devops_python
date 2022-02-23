# From the following source:
# https://www.realpythonproject.com/how-to-create-a-wheel-file-for-your-python-package-and-import-it-in-another-project/
from makeWheelSample.__init__ import *

def func_test():
    print("Successfully Imported test.py file")

def print_name(name):
    print(f'Hello {name}')

def print_test_age(age):
    print_age(age)