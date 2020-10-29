# Emlang attempt 2
The main reason for starting a new attempt is a fairly large break from working on this and I need to re-orient myself with whats going on. 
The other thing is I want to doccument the code in a very verbose maner, including having a dump here on the theory

I will use python3 this time, as its what I am currently most familar with and I want to just be able to focus on the language specific stuff. Once I understand this well enough I can take the lessons learnt and rebuild this in c or c++

## Language Theory
General comments on the different stages and theory of creating a programming language.

### 1. Lexing / Scanning 
Takes the string of characters that is the program and transforms them into tokens. 

For example given the string:
`var potato = (start + 5) / 2;`

This would be broken into tokens as such:
[`var`] [`potato`] [`=`] [`(`] [`start`] [`+`] [`5`] [`)`] [`/`] [`2`] [`;`]

### 2. Parsing
This is the process of taking the squence of tokens from the Lexer and transforming them into an `Abstract Syntax Tree`.

For the same string of code above the Abstract Syntax Tree may look like the following:

```
                       --- start
                       |
               --- + ---
               |       |
potato --- / ---        --- 5
               |
               --- 2
```

Note that the Abstract Syntax Tree creates a representation of the order of operations dictated by the tokens. When the token parsed in from the Lexer would generate an impossible or invlid tree we need to return a syntax error.

### 3. Static Analysis
Static Analysis is the process of looking at all the specific tokens like `potato` or `start` and resolving what they represent as well as confirming there are no illigal actions.

This is where we would also perform type checking. i.e. an `int` cant be added to a `string`. 

### 4. Intermediate Representations
This is a representation of the program in an intermediate way. In the sence that this is a generic representation that can then be taken and comiled down to different archetectures if needed. There are a few generic Intermediate Reprenentations that are well supported, generally it makes the most sense to target one of these.

### 5. Optimisation
At this point we know what the program intends to do, and we can add in optimisations and other tricks to make it more efficiant. 

things like for example if the incoming string is: `speed = (13 + 5) / 2`
We know the math will work out to be `9` so we can optimise this to be `speed = 9`

There are many many other optimisations that can be made, but at the time or writing I do not know what they are yet! This is more of the theoretical learning exercise for me so performance and efficiancy are not a big concern for this project.

### 6. Code Generation
Now we need to turn what we have into something the target machine or runtime can understand and process. In the case of this language we will be targeting a runtime or bytecode representation of our program. 

## Emlang Specification
General notes on what Emlang will look like and what features it will have, this is obviously subject to change at a moments notice.

### Example
```
// This is a comment and the below prints information
print "sup emlang";

// declaring a variable
var potato = "whatttt";

// declaring a function
function start(input)
{
    print "wow its a potato " + input;
    return true;
}

// calling the function
success = start(potato);

// comparison operator
if (success == true)
{
    print "the potato army is victorious";
} else{
    print "the potato has been defeated";
}

// defining a class
class Potato {
    eat() 
    {
        print "yumz";
    }
}
```
Initially I will have the `;` denote the end of a line, but eventually I would like to remove the need for that and treat the `\n` character as the end of a line. This will be a nice to have.

### Supported Datatypes
Emlang will initiall support:
```
Boolean (`True` / `False`)
Numbers (integer and decimals as one type initially, this will change later)
Strings
Null
```

### Supported Expressions
Emlang will initially support:
```
Addition:                   + (also can be used to concatinate 2 strings)
Subtraction:                -
Multiplication:             *
Division:                   /
Negate:                     -value (to invert the value of value)
```
Later on I would like to add Modulo (`%`)

### Supported Comparison Operations
Emlang will initially support:
```
Less Than:                  <
Less than or equal:         <=
Greater than:               >
Greater than or equal:      >=
Equal:                      ==
```
There will be no implicit conversions between different datatypes. Only epxlicit conversion will be allowed.

### Supported Logical Operators
Emlang will initially support:
```
And:                        and
Or:                         or
Not:                        !   (prefixed to any comparison to negate result)
```

### Bitwise and Shift operations
This will not be supported at all initially, but is defiantly something that I want to add as it will be important for the target language use case.

### Control Flow
Emlang will initially support the following control flow operators:
```
if:                         if (condition){ }
else:                       else { }
while:                      while (condition){ }
for:                        for (var a = 0; a < 10; a = a + 1) { }
```
Later I would like to support some form of `foreach` loop type.

### Functions
Functions in Emlang:
```
Declare a Function:         function cookPotato(parameter1, parameter2, ...) { }
Call a Function:            cookPotato(5, 2);
Function Return:            return("cooked");
```

### Closures
Initially Emlang will support closures as this will be an interesting thing to learn how to implement. But I suspect I will want to take that out and have strict scoping rules.

### Clases
Emlang will support classes, this may be removed in the future but will most likely just be a neglected feature.
```
Definig a class:            class Potato { }
Defining inheritance:       class Mash < Potato { }
Defining an initializer:    init(paremeter1, parameter2, ...) { }
Creating an instance:       var food = potato();
Add/Modify Property:        food.color = "grey";
Calling a method:           food.eat();
```

### Dynamically Typed
emlang will initially be dynamically typed. But the end goal will be to have it staticly typed, this is due to the intial implementation and learning ramp up. But statically typed will suit the goad of the language a lot better and the chagne will be made once I understand a lot more what I am doing.

### Memory Management
This will be done by the language... Think this is called `Garbage Collection`. I need to update this bit later when I understand it a bit better.

### Grammar Rules
**Terminal**: A letter from the Grammars alphabet, where the letters are the tokens output from the Lexer. This are the end point of the grammar as they are not expanded futhur.

**NonTerminal**: This is a refference to another rule in the grammar that then need to also be defined.

This will be based on the `Backus-Naur form` of notation, we have a couple of key symbols defined as below:
```
→    defines the produciton of a rule        <rule> → <production>
;    End of a sequence                       <rule> → <production> ;
|    Allows multiple producitons in a rule   <rule> → <production> | <produciton> ;
( )  Allows options mid production           <rule> → (<production> | <produciton>) | <production> ;
*    Repeat 0 or more times                  <rule> → <produciton> <production>* ;
+    Repeat 1 or more tiems                  <rule> → <production>+ ;
?    Optional, can appear 0 or 1 times       <rule> → <production> (<production>)? ;
```

Preccedence rules for the emlang grammar are important as they remove ambiguity where a string of tokens could be built into multiple syntax trees. Take for example:
`1 + 3 * 6`. Without precedence this could become `(1 + 3) * 6` or `1 + (3 * 6)`. This becomes part of the emlang grammar definition. The precedence rules are as follows:
```
1. Equality                                  == !=
2. Comparison                                > < >= <=
3. Term                                      + -
4. Factor                                    / *
5. Unary                                     ! -
6. Primary                                   Number String "true" "false" "Null" "(" ")"
```

The grammar definition for emlang is as follows (Note: this only implmements a subset for now and will be expanded on):
```
__VERSION 1__ (NO PRECEDENCE)

expression     → literal
                 | unary
                 | binary
                 | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+"  | "-"  | "*" | "/" ;
```

```
__VERSION 2__ (WITH PRECEDENCE)

expression     → equality
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```

```
___VERSION 3___ (WITH INITIAL STATEMENTS)
program        → statement* EOF

statement      → exprStmt | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
yeetStmt       → "YEET" expression ";" ;

expression     → equality
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```

```
___VERSION 4___ (WITH DECLERATIONS FOR VARIABLES AND ASSIGNMENT)
program        → declaration* EOF

declaration    → varDecl | statement ;

statement      → exprStmt | printStmt ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
yeetStmt       → "YEET" expression ";" ;

expression     → assignment ;
assignment     → IDENTIFIER "=" assignment | equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER ;
```

```
___VERSION 5___ (WITH BLOCKS!)
program        → declaration* EOF

declaration    → varDecl | statement ;

statement      → exprStmt | printStmt | block ;

block          → "{" declaration* "}" ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
yeetStmt       → "YEET" expression ";" ;

expression     → assignment ;
assignment     → IDENTIFIER "=" assignment | equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER ;
```