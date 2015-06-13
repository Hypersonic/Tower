from copy import copy

class TowerString(object):
    def __init__(self, data):
        self.data = data

class TowerNumber(object):
    def __init__(self, data):
        self.data = data

class TowerFunc(object):
    def __init__(self, data):
        self.data = data

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
            tokens.pop(0) # remove end token
# TODO: function optimization?
            funcs[func_name] = func_code
        elif token == '+': # add
            first = stack.pop()
            second = stack.pop()
            stack.append(TowerNumber(first.data + second.data))
        elif token == '-': # sub
            first = stack.pop()
            second = stack.pop()
            stack.append(TowerNumber(second.data - first.data))
        elif token == '*': # mul
            first = stack.pop()
            second = stack.pop()
            stack.append(TowerNumber(first.data * second.data))
        elif token == '/': # div
            first = stack.pop()
            second = stack.pop()
            stack.append(TowerNumber(second.data / first.data))
        elif token == "'": # "quote" operator, pushes the next function to the stack
            func_name = tokens.pop(0)
            stack.append(TowerFunc(func_name))
        elif token == 'dup':
            val = stack.pop()
            stack.append(val)
            stack.append(val)
        elif token == 'pop':
            stack.pop()
        elif token =='call':
            func_name = stack.pop()
            if func_name in funcs: # non-builtin func
                run(copy(funcs[func_name].data), stack, funcs)
            else: # builtin func (or undefined, in which case it'll get caught later)
                run([func_name.data], stack, funcs)
        elif token == 'if':
            cond = stack.pop()
            true_func = stack.pop()
            false_func = stack.pop()
            if cond:
                run(copy(funcs[true_func.data]), stack, funcs)
            else:
                run(copy(funcs[false_func.data]), stack, funcs)
        elif token == '[': # rotate left
            stack.append(stack.pop(0))
        elif token == ']': # rotate right
            stack.insert(0, stack.pop())
        elif token == '.':
            val = stack.pop()
            print str(val.data)
        elif token == '.s':
            print str([x.data for x in stack])
        elif token.isdigit() or (token[1:].isdigit() and token[0] == '-'):
            stack.append(TowerNumber(int(token)))
        elif all(c.isdigit() for c in token if c != '.' and c != '-'):
            if (token.count('-') == 1 and token[0] == '-') or token.count('-') == 0:
                stack.append(TowerNumber(float(token)))
            else:
                raise SyntaxError('- found in the middle of floating point literal: ' + token)
        elif len(token) >= 2 and token[0] == '"' and token[-1] == '"':
            stack.append(TowerString(token[1:-2]))
        elif token in funcs:
            run(copy(funcs[token]), stack, funcs)
        else:
            raise SyntaxError("No such function: " + token)

    return stack

builtin_functions = {
        'noop': [],
        '$': ['call'],
        'recip': [']', '1.0', '[', '/'],
        'neg': ['-1', '*']
        }
        
if __name__ == '__main__':
    program = """
    := f 1 1 + 1 - end
    := ( a b -> a+b ) add + end # this is a comment
    := tf + end
    := ff - end
    ( an inline comment )
    ' f call . 
    1 2 add .
    1 2 3 4 5
    "hello, world" .
    .s [ .s pop .s ] .s
    1.1 1 + .
    -1.2 .
    1 1 ' ff ' tf 1 if .
    10 recip .
    12 neg .
    """
    print "PROGRAM:",program
    tokens = tokenize(program)
    print "TOKENS:",tokens
    from copy import copy
    result = run(tokens, [], copy(builtin_functions))
