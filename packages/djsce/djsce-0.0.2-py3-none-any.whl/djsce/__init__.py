from dsa import *
from python import *

def dsa():
    for filename, content in dsa_exp.items():
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")

def python():
    for filename, content in python_exp.items():
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")