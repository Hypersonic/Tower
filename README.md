# Tower

Tower is a simple stack-based language.

Primitives:
-----------

Tower has 4 primitive types:
1. Numbers
2. Strings
3. Booleans
4. Functions

Function literals:
------------------

In Tower, you can push a function onto the stack. The syntax for doing this is `' function_name`.

Thanks to this mechanism, conditionals are merely a pair of functions on the stack, a boolean, and a call to `if`.

In practice, this looks like:

`' truefunc ' falsefunc True if`

This will call truefunc. If the conditional were False, it would call falsefunc.

Using this conditional and recursion, you can accomplish terminatable looping.

Literals:
---------

In addition to function literals, you have:

Boolean literals: True, False

Integer literals: 1, 2, etc.

Float literals: 1.1, .01, etc.

String literals: "hello, world"
