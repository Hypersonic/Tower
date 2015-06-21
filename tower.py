from copy import copy
import sys

class TowerString(object):
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return 'TowerString(%r)'%self.data

class TowerNumber(object):
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return 'TowerNumber(%r)'%self.data

class TowerFunc(object):
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return 'TowerFunc(%r)'%self.data

TOKEN_STATE_BEGIN = 0x1
TOKEN_STATE_END = 0x2
TOKEN_STATE_QUOTE = 0x3
TOKEN_STATE_QUOTE_ESCAPE = 0x4
TOKEN_STATE_INLINE_COMMENT = 0x5
TOKEN_STATE_COMMENT = 0x6
TOKEN_STATE_SYMBOL = 0x7

def lex(program):
    tokens = []
    curr_token = ""
    it = iter(program)
    state = TOKEN_STATE_BEGIN
    for c in it:
        if state == TOKEN_STATE_BEGIN:
            if c == '"': # strings are a single token
                curr_token += '"'
                state = TOKEN_STATE_QUOTE
            elif c == '(': # remove inline comments
                state = TOKEN_STATE_INLINE_COMMENT
            elif c == '#': # remove until-EOL comments
                state = TOKEN_STATE_COMMENT
            elif c in [' ', '\n']: # whitespace terminates a token
                state = TOKEN_STATE_BEGIN
            else:
                curr_token += c
                state = TOKEN_STATE_SYMBOL
        elif state == TOKEN_STATE_QUOTE:
            if c == '\\': # escape character
                state = TOKEN_STATE_QUOTE_ESCAPE
            elif c == '"':
                curr_token += c
                tokens.append(curr_token)
                curr_token = ''
                state = TOKEN_STATE_BEGIN
            else:
                curr_token += c
        elif state == TOKEN_STATE_QUOTE_ESCAPE:
            curr_token += c
            state = TOKEN_STATE_QUOTE
        elif state == TOKEN_STATE_INLINE_COMMENT:
            if c == ')':
                state = TOKEN_STATE_BEGIN
        elif state == TOKEN_STATE_COMMENT:
            if c == '\n':
                if curr_token:
                    tokens.append(curr_token)
                    curr_token = ''
                state = TOKEN_STATE_BEGIN
        elif state == TOKEN_STATE_SYMBOL:
            if c in [' ', '\n']: # whitespace terminates a token
                if curr_token:
                    tokens.append(curr_token)
                    curr_token = ''
                state = TOKEN_STATE_BEGIN
            else:
                curr_token += c
    return tokens

PARSE_STATE_BEGIN = 0x1
PARSE_STATE_DEFINE = 0x2

def parse(tokens):
    parsed = []
    states = [PARSE_STATE_BEGIN]
    while tokens:
        if states[-1] == PARSE_STATE_BEGIN:
            token = tokens.pop(0)
            if token == ':=':
                states.append(PASE_STATE_DEFINE)
        elif states[-1] == PARSE_STATE_DEFINE:
            pass
    return parsed


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
            stack.append(TowerString(token[1:-1]))
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
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            program = f.read()
        print "PROGRAM:",program
        tokens = lex(program)
        print "TOKENS:",tokens
        from copy import copy
        result = run(tokens, [], copy(builtin_functions))
    else:
        print "usage: python tower.py [program_filename]"
