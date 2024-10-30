# TODO
The grammar is not _that_ relevant, due to the nature of this project.  
But here's the basic overview anyway...

```
program => statement*
statement => assignment | print | loop
assignment => identifier '=' expression
print => 'print' '(' expression ')'
loop => 'for' identifier 'in' expression '..' expression '{' statement* '}'
expression => term (('+' | '-') term)*
term => factor (('*' | '/') factor)*
factor => number | identifier
identifier => letter (letter | digit)*
number => digit+
letter => [a-zA-Z]
digit => [0-9]
```
