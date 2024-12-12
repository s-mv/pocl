package main

type Node interface {
}

type Program struct {
	Statements []Statement
}

type Statement interface {
	Node
}

type Assignment struct {
	Identifier string
	Value      Expression
}

type PrintStatement struct {
	Expression Expression
}

type FunctionDeclaration struct {
	Name       string
	Parameters []string
	Body       []Statement
}

type IfStatement struct {
	Condition Expression
	Body      []Statement
}

type ForStatement struct {
	LoopVariable string
	Start        Expression
	End          Expression
	Body         []Statement
}

type FunctionCall struct {
	FunctionName string
	Arguments    []Expression
}

type Expression interface {
	Node
	expression()
}

type BinaryExpression struct {
	Left  Expression
	Right Expression
}

func (b *BinaryExpression) expression() {}

type NumberLiteral struct {
	Value float64
}

func (n *NumberLiteral) expression() {}

type IdentifierExpression struct {
	Name string
}

func (i *IdentifierExpression) expression() {}

type ParenthesizedExpression struct {
	Inner Expression
}

func (p *ParenthesizedExpression) expression() {}
