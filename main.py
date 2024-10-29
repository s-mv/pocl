from lexer import Lexer

with open("tests/example.pocl") as file:
    code = file.read()

lexer = Lexer(code)
tokens = lexer.lex()

for token in tokens:
    print(token)
