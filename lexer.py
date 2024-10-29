"""
NOTE:
this is a quick and dirty lexer
in no way is this the most efficient way to do things
if I needed fast, I wouldn't be prototyping...
or using Python for this of all things I guess
"""


class Lexer:
    source: str
    position: int

    def __init__(self, source: str):
        self.source = source
        self.position = 0

    def next(self):
        if self.position >= len(self.source):
            return None
        char = self.source[self.position]
        self.position += 1
        return char

    def peek(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def skip_whitespace(self):
        while self.peek() and self.peek() in " \t":
            self.next()

    def lex(self):
        tokens = []

        while True:
            self.skip_whitespace()
            char = self.next()

            if char is None:
                break

            if char.isdigit():
                num = char
                while self.peek() and self.peek().isdigit():
                    num += self.next()
                tokens.append(("NUMBER", num))

            elif char.isalpha():
                identifier = char
                while self.peek() and self.peek().isalnum():
                    identifier += self.next()
                if identifier == "print":
                    tokens.append(("PRINT", identifier))
                elif identifier == "for":
                    tokens.append(("FOR", identifier))
                else:
                    tokens.append(("IDENTIFIER", identifier))

            elif char == "=":
                tokens.append(("ASSIGN", char))

            elif char == "+":
                tokens.append(("PLUS", char))

            elif char == "-":
                tokens.append(("MINUS", char))

            elif char == "*":
                tokens.append(("MULTIPLY", char))

            elif char == "/":
                tokens.append(("DIVIDE", char))

            elif char == "{":
                tokens.append(("LBRACE", char))

            elif char == "}":
                tokens.append(("RBRACE", char))

            elif char == ".":
                if self.peek() == ".":
                    self.next()
                    tokens.append(("RANGE", ".."))
                else:
                    # TODO
                    # maybe add more information?
                    tokens.append(("ERROR", char))

            elif char == "\n":
                tokens.append(("NEWLINE", char))

            else:
                tokens.append(("UNKNOWN", char))

        return tokens
