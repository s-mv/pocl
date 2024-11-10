from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from lexer import Token, TokenType

"""
all classes here
nothing much to see
the parser is below
"""


@dataclass
class Node:
    pass


@dataclass
class BinaryOp(Node):
    left: Node
    operator: str
    right: Node


@dataclass
class UnaryOp(Node):
    operator: str
    operand: Node


@dataclass
class Number(Node):
    value: str


@dataclass
class Identifier(Node):
    name: str


@dataclass
class Assignment(Node):
    target: Identifier
    value: Node


@dataclass
class CompoundAssignment(Node):
    target: Identifier
    operator: str
    value: Node


@dataclass
class FunctionCall(Node):
    name: Identifier
    arguments: List[Node]


@dataclass
class FunctionDecl(Node):
    name: str
    parameters: List[str]
    body: List[Node]


@dataclass
class IfStatement(Node):
    condition: Node
    body: List[Node]


@dataclass
class Program(Node):
    statements: List[Node]


"""
this is the real deal
the grammar is in docs/GRAMMAR.md
note that the grammar is extremely simple
the reason is that the point isn't extravagant syntax
the language itself is not even that important honestly...
"""


class Parser:
    tokens: List[Token]
    current: int
    ast: Node

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.ast = None

    def peek(self) -> Optional[Token]:
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]

    def advance(self) -> Optional[Token]:
        if self.current >= len(self.tokens):
            return None
        token = self.tokens[self.current]
        self.current += 1
        return token

    def match(self, token_type: TokenType, value: str = None) -> bool:
        if self.peek() and self.peek().type == token_type:
            if value is None or self.peek().value == value:
                self.advance()
                return True
        return False

    def expect(self, token_type: TokenType, value: str = None) -> Token:
        if self.match(token_type, value):
            return self.tokens[self.current - 1]
        token = self.peek()
        # TODO, panic mode perhaps?
        # highly unneeded in my opinion
        # were it a traditional language I wouldn't even be making it in Python
        # so it seems like a waste of energy to polish the parts that don't matter
        # (at least until the crux of the project is not made)
        raise SyntaxError(
            f"Expected {token_type.name} {f'({value})' if value else ''}, got {token} instead!"
        )

    def parse(self) -> Program:
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        self.ast = Program(statements)
        return self.ast

    def parse_statement(self) -> Node:
        if self.peek().type == TokenType.KEYWORD:
            if self.peek().value == "fn":
                return self.parse_function_declaration()
            elif self.peek().value == "if":
                return self.parse_if_statement()
            elif self.peek().value == "print":
                return self.parse_print_statement()

        if self.peek().type == TokenType.IDENTIFIER:
            return self.parse_assignment_or_call()

        raise SyntaxError(f"Unexpected token: {self.peek()}!")

    def parse_function_declaration(self) -> FunctionDecl:
        self.expect(TokenType.KEYWORD, "fn")
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.PAREN, "(")

        parameters = []
        if self.peek() and self.peek().type == TokenType.IDENTIFIER:
            parameters.append(self.advance().value)
            while self.peek() and self.peek().value == ",":
                self.advance()
                parameters.append(self.expect(TokenType.IDENTIFIER).value)

        self.expect(TokenType.PAREN, ")")
        self.expect(TokenType.BRACE, "{")

        body = []
        while self.peek() and self.peek().value != "}":
            body.append(self.parse_statement())

        self.expect(TokenType.BRACE, "}")
        return FunctionDecl(name, parameters, body)

    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.KEYWORD, "if")
        condition = self.parse_expression()
        self.expect(TokenType.BRACE, "{")

        body = []
        while self.peek() and self.peek().value != "}":
            body.append(self.parse_statement())

        self.expect(TokenType.BRACE, "}")
        return IfStatement(condition, body)

    def parse_print_statement(self) -> FunctionCall:
        self.expect(TokenType.KEYWORD, "print")
        self.expect(TokenType.PAREN, "(")
        arg = self.parse_expression()
        self.expect(TokenType.PAREN, ")")
        return FunctionCall(Identifier("print"), [arg])

    def parse_assignment_or_call(self) -> Node:
        identifier = Identifier(self.expect(TokenType.IDENTIFIER).value)

        if self.match(TokenType.PAREN, "("):
            args = []
            if self.peek() and self.peek().value != ")":
                args.append(self.parse_expression())
                while self.peek() and self.peek().value == ",":
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.PAREN, ")")
            return FunctionCall(identifier, args)

        if self.match(TokenType.OPERATOR, "+="):
            value = self.parse_expression()
            return CompoundAssignment(identifier, "+=", value)

        self.expect(TokenType.OPERATOR, "=")
        value = self.parse_expression()
        return Assignment(identifier, value)

    def parse_expression(self) -> Node:
        return self.parse_additive()

    def parse_additive(self) -> Node:
        left = self.parse_multiplicative()

        while self.peek() and self.peek().value in ["+", "-"]:
            operator = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, operator, right)

        return left

    def parse_multiplicative(self) -> Node:
        left = self.parse_primary()

        while self.peek() and self.peek().value in ["*", "/"]:
            operator = self.advance().value
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)

        return left

    def parse_primary(self) -> Node:
        if self.match(TokenType.LITERAL):
            return Number(self.tokens[self.current - 1].value)

        if self.match(TokenType.IDENTIFIER):
            identifier = Identifier(self.tokens[self.current - 1].value)
            if self.match(TokenType.PAREN, "("):
                args = []
                if self.peek() and self.peek().value != ")":
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().value == ",":
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.PAREN, ")")
                return FunctionCall(identifier, args)
            return identifier

        if self.match(TokenType.PAREN, "("):
            expr = self.parse_expression()
            self.expect(TokenType.PAREN, ")")
            return expr

        raise SyntaxError(f"Unexpected token: {self.peek()}")


def print_ast(node: Node, indent: int = 0) -> None:
    indent_str = "    " * indent

    if isinstance(node, Program):
        print(f"{indent_str}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, BinaryOp):
        print(f"{indent_str}BinaryOp '{node.operator}'")
        print(f"{indent_str}  Left:")
        print_ast(node.left, indent + 2)
        print(f"{indent_str}  Right:")
        print_ast(node.right, indent + 2)

    elif isinstance(node, UnaryOp):
        print(f"{indent_str}UnaryOp '{node.operator}'")
        print(f"{indent_str}  Operand:")
        print_ast(node.operand, indent + 2)

    elif isinstance(node, Number):
        print(f"{indent_str}Number: {node.value}")

    elif isinstance(node, Identifier):
        print(f"{indent_str}Identifier: {node.name}")

    elif isinstance(node, Assignment):
        print(f"{indent_str}Assignment")
        print(f"{indent_str}  Target:")
        print_ast(node.target, indent + 2)
        print(f"{indent_str}  Value:")
        print_ast(node.value, indent + 2)

    elif isinstance(node, CompoundAssignment):
        print(f"{indent_str}CompoundAssignment '{node.operator}'")
        print(f"{indent_str}  Target:")
        print_ast(node.target, indent + 2)
        print(f"{indent_str}  Value:")
        print_ast(node.value, indent + 2)

    elif isinstance(node, FunctionCall):
        print(f"{indent_str}FunctionCall")
        print(f"{indent_str}  Name:")
        print_ast(node.name, indent + 2)
        print(f"{indent_str}  Arguments:")
        for arg in node.arguments:
            print_ast(arg, indent + 2)

    elif isinstance(node, FunctionDecl):
        print(f"{indent_str}FunctionDecl '{node.name}'")
        print(f"{indent_str}  Parameters: {', '.join(node.parameters)}")
        print(f"{indent_str}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

    elif isinstance(node, IfStatement):
        print(f"{indent_str}IfStatement")
        print(f"{indent_str}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{indent_str}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

    else:
        print(f"{indent_str}Unknown node type: {type(node)}")
