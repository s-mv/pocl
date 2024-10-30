from enum import Enum

"""
NOTE:
this is a quick and dirty lexer
in no way is this the most efficient way to do things
if I needed fast, I wouldn't be prototyping...
or using Python for this of all things I guess
"""


class TokenType(Enum):
    KEYWORD = 0
    LITERAL = 1
    IDENTIFIER = 2
    OPERATOR = 3
    ERROR = 4
    UNKNOWN = 5


class Token:
    type: TokenType
    value: any
    position: int

    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return self.value


class Lexer:
    source: str
    position: int
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.tokens = []

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
        while self.peek() and self.peek() in " \n\t":
            self.next()

    def lex(self):
        self.tokens = []

        while True:
            self.skip_whitespace()
            char = self.next()

            if char is None:
                break

            if char.isdigit():
                num = char
                while self.peek() and self.peek().isdigit():
                    num += self.next()
                self.tokens.append(Token(TokenType.LITERAL, num, self.position))

            elif char.isalpha():
                identifier = char
                while self.peek() and self.peek().isalnum():
                    identifier += self.next()
                if identifier == "print":
                    self.tokens.append(
                        Token(TokenType.KEYWORD, identifier, self.position)
                    )
                elif identifier == "for":
                    self.tokens.append(
                        Token(TokenType.KEYWORD, identifier, self.position)
                    )
                else:
                    self.tokens.append(
                        Token(TokenType.IDENTIFIER, identifier, self.position)
                    )

            elif char == "=":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "+":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "-":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "*":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "/":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "{":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == "}":
                self.tokens.append(Token(TokenType.OPERATOR, char, self.position))

            elif char == ".":
                if self.peek() == ".":
                    self.next()
                    self.tokens.append(Token(TokenType.OPERATOR, "..", self.position))
                else:
                    # TODO
                    # maybe add more information?
                    self.tokens.append(Token(TokenType.ERROR, char, self.position))
            else:
                self.tokens.append(Token(TokenType.UNKNOWN, char, self.position))
