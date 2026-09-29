# GrindLang

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![C](https://img.shields.io/badge/C-17-blue.svg)](https://en.cppreference.com/w/c/17)

> **Write simple. Build anything.**

GrindLang is a small programming language built from scratch.

It is currently an MVP with a working lexer, parser, AST pipeline, C code generator, and executable generation workflow.

The long-term goal is to create a **fluid programming language** with simple syntax, minimal bloat, and a foundation capable of supporting many different areas of programming.

---

# Quick Start

## Requirements

Currently, GrindLang requires:

* Python 3.8+
* GCC
* A system capable of running the generated executable

The current compiler is written in Python and generates C code.

## Run GrindLang

Run the main compiler:

```bash
python3 main.py
```

The compiler will ask you for the path to a `.grind` file.

Example:

```text
Drag and Drop your file here (or type the content path).
```

After loading the file, GrindLang generates a `.c` file beside the source file.

You can then choose whether to compile the generated C code into an executable using GCC.

The current pipeline is:

```text
program.grind
      ↓
   GrindLang
      ↓
  program.c
      ↓
     GCC
      ↓
  executable
```

---

# Your First GrindLang Program

Create a file called:

```text
hello.grind
```

Put this inside:

```grind
show "Hello, GrindLang";
```

Run:

```bash
python main.py
```

Select your `.grind` file.

GrindLang will generate C code and can compile and run it for you.

---

# Syntax

GrindLang syntax is designed to be simple and familiar while still leaving room for its own identity.

For basic syntax idea check `test.grind`

## Statement Termination

A statement can end with either a semicolon or a newline.

Both are valid:

```grind
show "Hello";
show "World";
```

and:

```grind
show "Hello"
show "World"
```

The lexer converts both into an `END_OF_STATEMENT` token.

---

# Comments

Comments use `//`.

```grind
// This is a comment

show "Hello";
```

---

# Variables

Variables are declared with `let`.

## Integer

```grind
let int age = 15;
```

## Float

```grind
let float speed = 10.5;
```

## String

```grind
let str name = "GrindLang";
```

The currently implemented generator supports integer, float, and string declarations.

Boolean tokens and parser support exist, but boolean C generation is not implemented yet.

---

# Output

GrindLang uses `show` for output.

```grind
show "Hello";
```

Integer:

```grind
show 42;
```

Float:

```grind
show 10.5;
```

The current C generator translates these into C `printf` calls.

For example:

```grind
show "Hello";
```

becomes conceptually:

```c
printf("Hello\n");
```

---

# Conditions

GrindLang uses `if`, `elif`, and `else`.

```grind
if (condition) {
    statement
} elif (condition) {
    statement
} else {
    statement
}
```

Both `elif` and `else` are optional.

Example:

```grind
let int x = 10;

if (x > 5) {
    show "x is greater than 5";
} elif (x == 5) {
    show "x is 5";
} else {
    show "x is smaller than 5";
}
```

The braces define the body of the conditional.

---

# Loops

GrindLang currently provides the `loop` construct.

## Fixed Repetition

Use `reps` to repeat something a defined number of times:

```grind
loop {
    reps: 5

    show "grinding";
}
```

The current C generator translates this into a C `for` loop.

Conceptually:

```c
for (int _grind_loop_0 = 0; _grind_loop_0 < 5; _grind_loop_0++) {
    printf("grinding\n");
}
```

---

# Infinite Loops

Use `keep` for an infinite loop:

```grind
loop {
    reps: keep

    show "running";
}
```

The current generator translates this into:

```c
while (1) {
    ...
}
```

---

# Stopping a Loop

`stop` can be used inside a loop.

```grind
loop {
    reps: keep

    stop
}
```

The current generator translates `stop` into a C `break`.

The parser also checks `keep` loops and warns when an infinite loop does not contain `stop`.

---

# Assignments

Variables can be assigned after declaration.

```grind
let int x = 10;

x = 20;
```

The parser also recognizes compound assignment operators:

```grind
x += 5;
x -= 5;
x *= 2;
x /= 2;
```

Support for these features is still part of the ongoing compiler development.

---

# Types

The current token library defines:

```text
int
float
bool
str
```

The current generator has support for:

```text
int
float
str
```

Boolean generation is not implemented yet.

---

# Operators

The lexer currently recognizes arithmetic operators:

```text
+
-
*
/
```

Comparison operators:

```text
=
==
<
>
<=
>=
```

Compound assignment operators:

```text
+=
-=
*=
/=
```

The expression system is still under development.

---

# Example Program

A small GrindLang program can look like this:

```grind
let int x = 10;
let float speed = 5.5;
let str name = "GrindLang";

show name;

if (x > 5) {
    show "x is greater than 5";
}

loop {
    reps: 3

    show "grinding";
}
```

The important part is that the syntax stays small.

The language should not make the programmer fight the language just to express basic ideas.

---

# Current Features

GrindLang v1 currently contains:

* `.grind` source files
* lexical analysis
* keywords
* identifiers
* integer literals
* floating-point literals
* strings
* comments
* newline statement termination
* semicolon statement termination
* variables
* `let`
* `show`
* `if`
* `elif`
* `else`
* `loop`
* `reps`
* `keep`
* `stop`
* assignments
* arithmetic operators
* comparison operators
* compound assignment tokenization
* AST generation
* C code generation
* GCC compilation
* executable generation

---

# How GrindLang Works

GrindLang currently uses a traditional compilation pipeline.

```text
          .grind source
                |
                v
             Lexer
                |
                v
             Tokens
                |
                v
             Parser
                |
                v
               AST
                |
                v
          C Code Generator
                |
                v
             C source
                |
                v
               GCC
                |
                v
            Executable
```

## 1. Lexer

The lexer reads the `.grind` source code and converts it into tokens.

For example:

```grind
let int x = 10;
```

becomes a sequence containing concepts such as:

```text
LET
INTEGER
IDENTIFIER:x
EQUAL_TO
INTEGER:10
END_OF_STATEMENT
```

The lexer handles:

* keywords
* identifiers
* integers
* floats
* strings
* operators
* comments
* punctuation
* statement endings

---

## 2. Token Library

`TokenLibrary.py` contains the definitions used by the lexer.

It defines:

* keywords
* single-character operators
* double-character operators
* punctuation
* data types

This keeps the lexical definitions separate from the lexer itself.

---

## 3. Parser

The parser consumes the tokens produced by the lexer.

It understands constructs such as:

```text
LET
PRINT
IF
ELIF
ELSE
LOOP
STOP
ASSIGNMENT
TRUE
FALSE
```

It also tracks declared variables and checks whether identifiers have been defined before they are used.

The parser produces GrindLang's current AST representation.

---

## 4. C Generator

The current backend converts the parsed representation into C code.

For example:

```grind
show 42;
```

becomes a C `printf` statement.

A generated program is wrapped in a C `main` function:

```c
#include <stdio.h>

int main() {
    ...
    return 0;
}
```

The current backend therefore looks like:

```text
GrindLang
    ↓
C
    ↓
GCC
    ↓
Machine code
```

GrindLang v1 does not directly generate machine code.

---

# Project Structure

```text
GrindLang/
│
├── main.py
├── NewLexer.py
├── TokenLibrary.py
├── Parser.py
├── Cgen.py
├── test.grind
│
└── README.md
```

## `main.py`

The compiler entry point.

It:

1. Loads the `.grind` file.
2. Generates C code.
3. Writes the generated `.c` file.
4. Optionally invokes GCC.
5. Runs the resulting executable.

## `NewLexer.py`

Responsible for lexical analysis.

It reads source code and produces the token stream.

## `TokenLibrary.py`

Contains the language's:

* keywords
* operators
* punctuation
* types

## `Parser.py`

Consumes tokens and produces the AST.

It handles the language's current statements and structures.

## `Cgen.py`

Converts the parser output into C code.

# `test.grind`
Basic guide file for grind lang syntax.

---

# Current Limitations

GrindLang v1 is an MVP.

It is **not a production-ready programming language**.

Some features are only partially implemented or still being developed.

Current limitations include:

* boolean code generation is not implemented
* expression parsing is being redesigned
* the language currently depends on generated C and GCC
* the compiler is still primarily experimental
* the type system is still developing
* many planned language features do not exist yet
* the current syntax and compiler architecture are subject to change

The current implementation is a foundation, not the final design.

---

# Roadmap

The roadmap is intentionally larger than the current MVP.

Long-term development is expected to include areas such as:

* stronger type checking
* improved expression parsing
* better AST representation
* more complete assignment support
* better error messages
* a proper intermediate representation or compiler backend architecture
* direct low-level targets
* memory and lifetime analysis
* liveness analysis
* safer resource management
* richer standard functionality
* game development support
* mathematical and machine learning functionality
* embedded development support
* a lightweight toolchain
* a custom development environment

The exact implementation may change as the language develops.

---

# Why GrindLang?

Every programming language tends to solve a problem.

Python focuses heavily on simple syntax and productivity.

Lua focuses heavily on portability and embeddability.

C provides low-level control and efficient resource usage.

C++ provides performance and is widely used for games and large systems.

Rust focuses heavily on safety.

Go focuses on simplicity and practical systems programming.

Assembly provides direct control over the machine.

Each approach has strengths.

Each approach also comes with costs.

Python can sacrifice raw execution speed.

Low-level languages can require more work from the programmer.

C++ can become complex.

Rust can require more language knowledge and discipline.

Assembly gives enormous control, but that control comes with a large amount of complexity.

GrindLang is an attempt to find a different point in that space.

## Fluidity

GrindLang is intended to be a **fluid language**.

It does not guarantee that it will be better than C for embedded systems.

It does not guarantee that it will be better than C++ for game development.

It does not guarantee that it will provide stronger safety guarantees than Rust.

It does not guarantee that it will replace Python for machine learning.

That is not the promise.

The promise is **fluidity**.

A C programmer who wants high-level productivity should not have to abandon low-level capabilities.

A Python programmer who wants machine-level performance should not have to completely abandon simple syntax.

A game developer should not need a completely different language just because the project needs lower-level functionality.

A machine learning programmer should not need a completely different language just because they need more control.

The goal is to make those transitions smaller.

---

# Simple Foundations

GrindLang may never provide a thousand things out of the box.

That is intentional.

A huge standard library can be useful, but the language itself should not need thousands of built-in concepts to be useful.

GrindLang aims to provide a **simple foundation capable of creating those things**.

The idea is:

```text
small language
     +
simple syntax
     +
strong foundations
     +
low bloat
     =
many possible applications
```

The goal is not to create a specialized tool.

The goal is to create a foundation.

---

# Simple Does Not Mean Hardcoded

GrindLang's syntax is intentionally simple.

As the language develops, its syntax will become more unique.

But unique does not mean difficult.

The language should be recognizable as GrindLang without becoming a puzzle that programmers have to solve before they can write useful code.

The syntax should stay clean even as the compiler underneath it becomes more capable.

---

# The Direction Matters

One of the biggest lessons from building GrindLang has been that **direction matters**.

Without direction, a codebase can become a mess.

That happened during development.

Some parts of the compiler became unnecessarily complicated because the destination was not clear enough.

Expression parsing was one of the hardest parts of the project.

Eventually, that implementation became unnecessary because the compiler direction changed.

That experience changed the way GrindLang is being developed.

The goal is not to build every interesting idea that appears.

The goal is to build toward the language GrindLang is supposed to become.

---

# From Assembly to C

The original direction was to generate C.

Then came the idea of generating assembly directly.

The idea was simple:

```text
GrindLang
    ↓
x86-64 Assembly
    ↓
Executable
```

That would have been interesting.

But the project eventually returned to C for the current MVP.

The current approach is:

```text
GrindLang
    ↓
C
    ↓
GCC
    ↓
Executable
```

This gives the project a usable backend while leaving room to explore lower-level targets later.

The long-term goal is not limited to C.

I am planning to make all base before making this a self-hosted language.

---

# What GrindLang Is Trying To Become

The long-term vision can be described in one phrase:

> **The water of programming languages.**

Water does not care whether the container is a cup, bottle, pipe, or river.

It flows into different shapes.

GrindLang should work similarly.

The language should be capable of flowing between different areas of software without becoming a specialized language for only one of them.

Game development.

Machine learning.

Systems programming.

Embedded software.

Low-level programming.

High-level application development.

Safety-oriented programming.

The language should provide a common foundation for all of them.

Not by becoming enormous.

By keeping the foundation simple.

---

# What GrindLang Should Feel Like

When someone writes GrindLang, the goal is not for them to constantly think about the language.

The goal is for the language to get out of the way.

The ideal experience is **flow**.

You know what you want to build.

You write it.

The language understands it.

You keep building.

No unnecessary ceremony.

No unnecessary bloat.

No unnecessary fight with the syntax.

Just:

```text
idea
 ↓
code
 ↓
build
 ↓
result
```

---

# GrindLang Is Not Trying To Be Everything

GrindLang is not trying to become a specialized tool.

It is not trying to become:

* only a game language
* only an AI language
* only an embedded language
* only a systems language
* only a safe language
* only a scripting language

The purpose is to create a foundation that can support all of these directions.

That is a much harder problem.

It is also the reason the project exists.

---

# The Goal Is Completion

GrindLang is not being made because it must become famous.

It is not being made because it must replace C.

It is not being made because it must replace Python.

It is not being made because it must defeat Rust.

The goal is much simpler.

**Build it.**

**Finish it.**

See the idea all the way through.

The project started as a language.

Then it became a lexer.

Then a parser.

Then a code generator.

Then an executable.

There is still a long way to go.

But that is the point.

> **GrindLang is being built to be completed.**

---

# Development

GrindLang is currently an experimental project.

The architecture, syntax, compiler pipeline, and language features may change as development continues.

The current implementation is intentionally small so that the foundations can be understood and rebuilt as the language evolves.

---

# License

GrindLang is released under the MIT License.

See [`LICENSE`](LICENSE) for details.