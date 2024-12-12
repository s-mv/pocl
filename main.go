package main

import (
	"log"
	"os"
)

func main() {
	filePath := "tests/simple.pocl"

	code, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}

	lexer := NewLexer(string(code))
	lexer.Lex()

	parser := NewParser(lexer.tokens)
	parser.Parse()

	PrintAST()
}
