from lexer import Lexer
from parser import Parser

with open("tests/example.pocl") as file:
    code = file.read()

lexer = Lexer(code)
lexer.lex()

print("Tokens:")
for token in lexer.tokens:
    print(f"`{token}`, ", end="")
print()


parser = Parser(lexer.tokens)
parsed_output = parser.program()
print(parsed_output)
