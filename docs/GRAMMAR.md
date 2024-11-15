# Grammar
The grammar is not _that_ relevant, due to the nature of this project.  
But here's the basic overview anyway...

```
program => statement*

statement => assignment 
          | print_statement
          | function_declaration
          | if_statement
          | function_call

assignment => identifier '=' expression

print_statement => 'print' '(' expression ')'

function_declaration => 'fn' identifier '(' parameters? ')' '{' statement* '}'

parameters => parameter (',' parameter)*

parameter => identifier

if_statement => 'if' expression '{' statement* '}' 

function_call => identifier '(' arguments? ')'

arguments => expression (',' expression)*

expression => term (('+' | '-') term)*

term => factor (('*' | '/') factor)*

factor => number | identifier | '(' expression ')'

identifier => letter (letter | digit)*

number => digit+

letter => [a-zA-Z]

digit => [0-9]
```
