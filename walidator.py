from scanner import *
from parser import *


with open("correct.txt", "r") as file:
    input_string = file.read()

scanner = Scanner(input_string)
for t in scanner.tokens:
    print(t)

parser = Parser(scanner)
parser.parse()
