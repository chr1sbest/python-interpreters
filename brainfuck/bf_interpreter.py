"""
Brainfuck language is in its own bytecode, no compilation step required.

Consists of a tape of 0's: [0][0][0][0]...
Values in the tape can be modified by pointer
"""
import os
import sys

class Tape(object):
    def __init__(self):
        self.thetape = [0]
        self.position = 0

    def get(self):
        return self.thetape[self.position]

    def increment(self):
        self.thetape[self.position] += 1

    def decrement(self):
        self.thetape[self.position] -= 1

    def advance(self):
        self.position += 1
        if len(self.thetape) <= self.position:
            self.thetape.append(0)

    def devance(self):
        self.position -= 1

#All commands readable by BF and their associated function
BF_commands = {
    '>': lambda x: x.advance(),
    '<': lambda x: x.devance(),
    '+': lambda x: x.increment(),
    '-': lambda x: x.decrement(),
    '.': lambda x: os.write(1, chr(x.get())),
    '[': lambda x, pc, bm: bm[pc] if not x.get() else pc,
    ']': lambda x, pc, bm: bm[pc] if x.get() else pc
    }

def evaluate(program, bracket_map):
    """Executes the commands in the program"""
    pc = 0
    tape = Tape()
    while pc < len(program):
        code = program[pc]
        if code in ('[', ']'):
            pc = BF_commands[code](tape, pc, bracket_map)
        else: 
            BF_commands[code](tape)
        pc += 1

def parse(program):
    """Returns only valid commands and a proper bracket mapping"""
    parsed, left_stack = [], []
    bracket_map = {}
    pc = 0

    for char in program:
        if char in BF_commands.keys() or char in (']', '['):
            parsed.append(char)
            if char == '[':
                left_stack.append(pc)
            elif char == ']':
                left = left_stack.pop()
                right = pc
                bracket_map[left] = right
                bracket_map[right] = left
            pc += 1

    return "".join(parsed), bracket_map

def input_reader(filename):
    """Returns contents of first argument given"""
    program_contents = ""
    bf = os.open(filename, os.O_RDONLY, 0777)
    while True:
        read = os.read(bf, 4096)
        program_contents += read
        if not len(read): break
    os.close(bf)
    return program_contents

if __name__ == "__main__":
    program_contents = input_reader(sys.argv[1])
    program, bracket_map = parse(program_contents)
    evaluate(program, bracket_map)
