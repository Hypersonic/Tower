def tokenize(program):
    tokens = []
    curr_token = ""
    it = iter(program)
    for c in it:
        if c == '"': # strings are a single token
            curr_token += '"'
            curr = ''
            while curr != '"':
                curr = it.next()
                if curr == '\\':
                    curr_token += it.next()
                else:
                    curr_token += curr
            curr_token += '"'
        elif c == '(': # remove inline comments
            curr = ''
            while curr != ')':
                curr = it.next()
        elif c == '#': # remove until-EOL comments
            curr = ''
            while curr != '\n':
                curr = it.next()
        elif c in [' ', '\n']: # whitespace terminates a token
            if curr_token:
                tokens.append(curr_token)
                curr_token = ''
        else:
            curr_token += c
    return tokens

def run(tokens, stack, funcs):
    while tokens:
        token = tokens.pop(0)
        if token == ':=': # the "define" token
            func_name = tokens.pop(0)
            func_code = []
            while tokens[0] != 'end':
                func_code.append(tokens.pop(0))
            funcs[func_name] = func_code
        elif token == '+': # add
            first = stack.pop()
            second = stack.pop()
            stack.append(first + second)
        elif token == '-': # sub
            first = stack.pop()
            second = stack.pop()
            stack.append(second - first)
        elif token == '*': # mul
            first = stack.pop()
            second = stack.pop()
            stack.append(first * second)
        elif token == '/': # div
            first = stack.pop()
            second = stack.pop()
            stack.append(second / first)
        elif token == "'": # "quote" operator, pushes the next function to the stack
            func_name = tokens.pop(0)
            stack.append(func_name)
        elif token == 'noop':
            pass
        elif token == 'dup':
            val = stack.pop()
            stack.append(val)
            stack.append(val)
        elif token == 'pop':
            stack.pop()
        elif token in ['call', '$']:
            func_name = stack.pop()
            run(funcs[func_name], stack, funcs)
        elif token == 'if':
            cond = stack.pop()
            true_func = stack.pop()
            false_func = stack.pop()
            if cond:
                run(funcs[true_func], stack, funcs)
            else:
                run(funcs[false_func], stack, funcs)
        elif token == '[': # rotate left
            stack.append(stack.pop(0))
        elif token == ']': # rotate right
            stack.insert(0, stack.pop())
        elif token == '.':
            val = stack.pop()
            print str(val)
        elif token == '.s':
            print str(stack)
        elif token == '(':
            while not ')' in tokens.pop(0):
                pass
        elif token.isdigit():
            stack.append(int(token))
        elif len(token) >= 2 and token[0] == '"' and token[-1] == '"':
            stack.append(token[1:-2])
        elif token in funcs:
            run(funcs[token], stack, funcs)

    return stack
        
if __name__ == '__main__':
    program = """
    := f 1 1 + 1 - end
    := ( a b -> a+b ) add + end # this is a comment
    ( an inline comment )
    ' f call . 
    1 2 add .
    1 2 3 4 5
    "hello, world" .
    .s [ .s pop .s ] .s
    """
    print "PROGRAM:",program
    tokens = tokenize(program)
    print "TOKENS:",tokens
    result = run(tokens, [], {})
