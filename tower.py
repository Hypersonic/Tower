class TowerFun(object):
    def __init__(self, opcodes=[0x0]):
        self.opcodes = opcodes
    
    def run(self, stack, inst_it):
        for opcode in self.opcodes:
            if opcode == 0x0: #noop
                pass
            elif opcode == 0x1: #add
                first = stack.pop()
                second = stack.pop()
                stack.append(first + second)
            elif opcode == 0x2: #sub
                first = stack.pop()
                second = stack.pop()
                stack.append(second - first)
            elif opcode == 0x3: #mul
                first = stack.pop()
                second = stack.pop()
                stack.append(first * second)
            elif opcode == 0x4: #div
                first = stack.pop()
                second = stack.pop()
                stack.append(second / first)

tower_opcodes = {
        'noop': 0x0,
        '+'   : 0x1,
        '-'   : 0x2,
        '*'   : 0x3,
        '/'   : 0x4
        }

def tokenize(pgm):
    return pgm.split()

def parse(tokens):
    out = []
    for token in tokens:
        if token.isdigit():
            out.append(int(token))
            continue
        elif token in tower_opcodes:
            out.append(TowerFun(opcodes=[tower_opcodes[token]]))
    return out

def run(ops):
    stack = []
    it = iter(ops)
    for op in it:
        if type(op) == int:
            stack.append(op)
        else:
            op.run(stack, it)
    return stack

if __name__ == '__main__':
    program = """
    1 1 + 1 -
    """
    print "PROGRAM:",program
    tokens = tokenize(program)
    print "TOKENS:",tokens
    parsed = parse(tokens)
    print "PARSED:",parsed
    result = run(parsed)
    print "RESULT:",result
