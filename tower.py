def tokenize(program):
    return program.split()

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
        elif token == 'noop':
            pass
        elif token == 'dup':
            val = stack.pop()
            stack.append(val)
            stack.append(val)
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
        elif token.isdigit():
            stack.append(int(token))
        elif len(token) > 0 and token[0] == '"' and token[-1] == '"':
            stack.append(token[1:-1])
        elif token in funcs:
            stack.append(token)

    return stack
        
if __name__ == '__main__':
    program = """
    := f 1 1 + 1 - end
    f call
    """
    print "PROGRAM:",program
    tokens = tokenize(program)
    result = run(tokens, [], {})
    print "RESULT:",result
