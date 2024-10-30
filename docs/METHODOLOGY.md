# Methodology: TODO

But since you're here, here's a really badly etched pipeline.

```
         lexing           parsing         semantic analysis
string --------> tokens ----------> AST --------------------> ??? ---> concurrent execution
```

## ???...?
pocl aims to introduce a new step to the traditional pipeline that checks for
dependecies between variables from "state" to "state" (more on this later),
among other things.

Sounds like a rather ambitious project but hey, let me try. :)

TODO: Lots. Too much.
