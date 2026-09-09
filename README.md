GrindLang

A mobile-focused compiled programming language with a custom IDE.

GrindLang is an experimental programming language designed around one idea:

«Programming on mobile shouldn't feel like a compromised version of programming on a PC.»

The project aims to build a compiled language with clean, familiar syntax, native mobile compatibility, and a lightweight custom IDE designed specifically for phones.

Current Status

Very early development.

Right now, GrindLang is in the language development phase.

- [x] Initial language design
- [x] Token definitions
- [x] Lexer development
- [ ] Parser
- [ ] AST
- [ ] Compiler
- [ ] Self-hosting
- [ ] Custom mobile IDE
- [ ] Standard library
- [ ] Mobile-native toolchain

The current implementation is being developed in Python as a bootstrap for the language. The long-term goal is for GrindLang to become self-hosted.

V1 Goal

The first major version of GrindLang is focused on two things:

Mobile compatibility

GrindLang should be able to work naturally on mobile devices instead of treating mobile as an afterthought.

A lightweight custom IDE

The planned IDE will be built specifically for GrindLang and mobile devices.

The goal is no unnecessary bloat.

No huge desktop-style development environment squeezed onto a phone.

Just the tools needed to write, compile, and run GrindLang programs.

Language Philosophy

GrindLang is designed to have syntax that feels familiar to programmers coming from languages like C, while avoiding unnecessary complexity.

Some current keywords include:

if
else
elif

loop
reps
keep
until

func
return
break
continue

class

let
const
sizeof

try
catch
throw

switch
case
default

import

show

The language also has explicit primitive types:

tiny_int
small_int
mid_int
large_int

tiny_flt
small_flt
mid_flt
large_flt

bool
char
str

These currently represent:

tiny_int   -> 8-bit integer
small_int  -> 16-bit integer
mid_int    -> 32-bit integer
large_int  -> 64-bit integer

tiny_flt   -> 16-bit floating point
small_flt  -> 32-bit floating point
mid_flt    -> 64-bit floating point
large_flt  -> 128-bit floating point

The language is still under active design, so syntax and features may change.

Current Lexer

The lexer is currently the most developed part of the project.

It recognizes:

- Keywords
- Identifiers
- Parentheses
- Curly braces
- Square brackets
- Operators
- Comparisons
- Assignment operators
- Comments
- Newlines
- Punctuation

Current operators include:

+   -   *   /
=   &   !
<   >

and:

+=
-=
*=
/=

==
>=
<=
!=

Development

The current bootstrap implementation uses Python.

The planned direction is:

GrindLang source
       |
     Lexer
       |
     Parser
       |
      AST
       |
    Compiler
       |
   Native code

Eventually, GrindLang is intended to become self-hosted, meaning the compiler/toolchain will be written in GrindLang itself.

Mobile First

Mobile isn't simply another supported platform for GrindLang.

It is one of the project's primary design constraints.

The long-term vision is to make it possible to:

Write code
   |
Compile
   |
Run

directly on a mobile device using a purpose-built environment.

The custom IDE is planned around this workflow.

Experimental Project

GrindLang is currently an experiment.

The language architecture, syntax, compiler design, memory model, standard library, and IDE are all subject to change.

Things will probably break.

Features will probably be redesigned.

That's part of the project.

Roadmap

Phase 1: Language Foundation

- [x] Token system
- [x] Keyword definitions
- [x] Operator definitions
- [x] Initial lexer
- [x] Complete lexer
- [ ] Parser
- [ ] AST
- [ ] Error handling

Phase 2: Compiler

- [ ] Code generation
- [ ] Runtime
- [ ] Memory management
- [ ] Standard library
- [ ] Native compilation

Phase 3: Self Hosting

- [ ] Rewrite compiler components in GrindLang
- [ ] Bootstrap compiler
- [ ] Self-hosted toolchain

Phase 4: Mobile IDE

- [ ] Custom editor
- [ ] Compiler integration
- [ ] Project management
- [ ] Run/build system
- [ ] Mobile-friendly UI
- [ ] Debugging tools

Phase 5: V1

GrindLang + native mobile toolchain + custom mobile IDE

Contributing

GrindLang is open source.

The project is currently experimental, so contributions, ideas, bug reports, and discussions are welcome.

License

GrindLang is open source.

License information will be added as the project develops.

---

GrindLang

Code without the desktop dependency.