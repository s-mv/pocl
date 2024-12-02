from enum import Enum
from typing import Optional


class TokenType(Enum):
    KEYWORD = 0
    LITERAL = 1
    IDENTIFIER = 2
    OPERATOR = 3
    PAREN = 4
    BRACE = 5
    ERROR = 6
    UNKNOWN = 7


class Token:
    type: TokenType
    value: any
    position: int

    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        return f"<{self.type.name}: '{self.value}' @ {self.position}>"


class Lexer:
    source: str
    position: int
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.tokens = []

    def next(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        char = self.source[self.position]
        self.position += 1
        return char

    def peek(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def skip_whitespace(self) -> None:
        while self.peek() and self.peek() in " \n\t":
            self.next()

    def lex(self) -> None:
        self.tokens = []

        while True:
            self.skip_whitespace()
            char = self.next()

            if char is None:
                break

            """
            lex numbers
            currently only int
            """
            if char.isdigit():
                num = char
                while self.peek() and self.peek().isdigit():
                    num += self.next()
                self.tokens.append(Token(TokenType.LITERAL, num, self.position))

                continue

            """
            lex keywords/identifiers
            """
            if char.isalpha():
                identifier = char
                while self.peek() and self.peek().isalnum():
                    identifier += self.next()

                if identifier == "print":
                    # technically print isn't a keyword but who cares for now
                    self.tokens.append(
                        Token(TokenType.KEYWORD, identifier, self.position)
                    )
                elif identifier in ("fn", "if", "for", "from", "to"):
                    self.tokens.append(
                        Token(TokenType.KEYWORD, identifier, self.position)
                    )
                else:
                    self.tokens.append(
                        Token(TokenType.IDENTIFIER, identifier, self.position)
                    )

                continue

            """
            lex `..` (operator)
            """
            if char == ".":
                if self.peek() == ".":
                    self.next()
                    self.tokens.append(Token(TokenType.OPERATOR, "..", self.position))
                else:
                    self.tokens.append(Token(TokenType.ERROR, char, self.position))

                continue

            """
            lex single char operators
            (and also handle unknown character)
            """
            match char:
                case "=" | "+" | "-" | "*" | "/":
                    self.tokens.append(Token(TokenType.OPERATOR, char, self.position))
                case "(" | ")":
                    self.tokens.append(Token(TokenType.PAREN, char, self.position))
                case "{" | "}":
                    self.tokens.append(Token(TokenType.BRACE, char, self.position))
                case _:
                    self.tokens.append(Token(TokenType.UNKNOWN, char, self.position))
