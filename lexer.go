package main

import (
	"unicode"
)

type TokenType int

const (
	KEYWORD TokenType = iota
	LITERAL
	IDENTIFIER
	OPERATOR
	PAREN
	BRACE
	ERROR
	UNKNOWN
)

func (t TokenType) String() string {
	return [...]string{
		"KEYWORD", "LITERAL", "IDENTIFIER",
		"OPERATOR", "PAREN", "BRACE",
		"ERROR", "UNKNOWN",
	}[t]
}

type Token struct {
	Type     TokenType
	Value    string
	Position int
}

func (t Token) String() string {
	return "<" + t.Type.String() + ": '" + t.Value + "' @ " + string(rune(t.Position)) + ">"
}

type SymbolType int

const (
	Variable SymbolType = iota
	Function
)

type Symbol struct {
	Type SymbolType
}

type SymbolTable map[string]Symbol

type Lexer struct {
	source   string
	position int
	tokens   []Token
	symtable SymbolTable
}

func NewLexer(source string) *Lexer {
	return &Lexer{
		source:   source,
		position: 0,
		tokens:   []Token{},
		symtable: make(SymbolTable),
	}
}

func (l *Lexer) next() rune {
	if l.position >= len(l.source) {
		return 0
	}
	char := rune(l.source[l.position])
	l.position++
	return char
}

func (l *Lexer) peek() rune {
	if l.position >= len(l.source) {
		return 0
	}
	return rune(l.source[l.position])
}

func (l *Lexer) skipWhitespace() {
	for l.peek() != 0 && (l.peek() == ' ' || l.peek() == '\n' || l.peek() == '\t') {
		l.next()
	}
}

func (l *Lexer) Lex() {
	l.tokens = []Token{}

	for {
		l.skipWhitespace()
		char := l.next()

		if char == 0 {
			break
		}

		// lex numbers
		// currently only int
		if unicode.IsDigit(char) {
			num := string(char)
			for l.peek() != 0 && unicode.IsDigit(l.peek()) {
				num += string(l.next())
			}
			l.tokens = append(l.tokens, Token{
				Type:     LITERAL,
				Value:    num,
				Position: l.position,
			})
			continue
		}

		// lex identifiers and keywords
		if unicode.IsLetter(char) {
			word := string(char)
			for l.peek() != 0 && (unicode.IsLetter(l.peek()) || unicode.IsNumber(l.peek())) {
				word += string(l.next())
			}

			switch word {
			case "print":
				// technically print isn't a keyword but who cares for now
				l.tokens = append(l.tokens, Token{
					Type:     KEYWORD,
					Value:    word,
					Position: l.position,
				})
			case "fn", "if", "for", "from", "to":
				l.tokens = append(l.tokens, Token{
					Type:     KEYWORD,
					Value:    word,
					Position: l.position,
				})
			default:
				// l.symtable[identifier] = Symbol{Type: Variable}
				l.tokens = append(l.tokens, Token{
					Type:     IDENTIFIER,
					Value:    word,
					Position: l.position,
				})
			}
			continue
		}

		// lex `..` (operator)
		if char == '.' {
			if l.peek() == '.' {
				l.next()
				l.tokens = append(l.tokens, Token{
					Type:     OPERATOR,
					Value:    "..",
					Position: l.position,
				})
			} else {
				l.tokens = append(l.tokens, Token{
					Type:     ERROR,
					Value:    string(char),
					Position: l.position,
				})
			}
			continue
		}

		// lex operators, parens, and braces
		switch char {
		case '=', '+', '-', '*', '/':
			l.tokens = append(l.tokens, Token{
				Type:     OPERATOR,
				Value:    string(char),
				Position: l.position,
			})
		case '(', ')':
			l.tokens = append(l.tokens, Token{
				Type:     PAREN,
				Value:    string(char),
				Position: l.position,
			})
		case '{', '}':
			l.tokens = append(l.tokens, Token{
				Type:     BRACE,
				Value:    string(char),
				Position: l.position,
			})
		default:
			l.tokens = append(l.tokens, Token{
				Type:     UNKNOWN,
				Value:    string(char),
				Position: l.position,
			})
		}
	}
}
