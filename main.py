from lexer import Lexer
from parser import Parser, print_ast

with open("tests/example_for.pocl") as file:
    code = file.read()

lexer = Lexer(code)
lexer.lex()

print("Tokens:")
for token in lexer.tokens:
    print(f"`{token}`, ", end="")
print()

parser = Parser(lexer.tokens)
parser.parse()
print_ast(parser.ast)
