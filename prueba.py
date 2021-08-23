#!/usr/bin/python3

from component import process
print("Module ", __name__)

file = process.load_file("COD.txt")
print(file)

def test(*args):
	print(args[0], args[1])
test(1, 2)
