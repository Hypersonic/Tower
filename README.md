# Tower

Tower is a simple stack-based language.

Primitives
-----------

Tower has 4 primitive types:

1. Numbers

2. Strings

3. Booleans

4. Functions

Defining functions
-------------------

A function is defined by a `:=`, followed by a space, then a name for the function, and then the operations to perform, separated by spaces. An operation of `end` terminates the function defininiton.

For example, to define a function called `square` that squares the top number on the stack, you might do:

`:= square dup * end`

Function literals
------------------

In Tower, you can push a function onto the stack. The syntax for doing this is `' function_name`.

Thanks to this mechanism, conditionals are merely a pair of functions on the stack, a boolean, and a call to `if`.

In practice, this looks like:

`' truefunc ' falsefunc True if`

This will call truefunc. If the conditional were False, it would call falsefunc.

Using this conditional and recursion, you can accomplish terminatable looping.

Literals
---------

In addition to function literals, you have:

Boolean literals: `True`, `False`

Integer literals: `1`, `2`, etc.

Float literals: `1.1`, `.01`, etc.

String literals: `"hello, world"`

Builtin Functions
------------------

Arithmetic Operations: `+`,`-`,`\*`,`/`

Stack operations: `pop`, `dup`, `[`, `]`

Printing operations: `.`, `.s`

Logical operations: `=`, `<`, `>`, `>=`, `<=`, `or`, `!`

Function operatons: `'`, `call`, `if`

Comments
--------

There are two types of comments in Tower: inline comments and until-end-of-line comments

An inline comment begins with the character `(` and continues until it reaches a `)`.

An until-end-of-line comment begins with the character `#` and continues until the end of the line.
