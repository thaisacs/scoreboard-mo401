#!/usr/bin/python3
from enum import Enum
import numpy as np

# --------------------------------------------------------------------------------------------

#fld (usa unidade de inteiros)
#fsd (usa unidade de inteiros)
#fadd (usa somador de ponto flutuante)
#fsub (usa somador de ponto flutuante)
#fmul (usa multiplicador de ponto flutuante)
#fdiv (usa divisor de ponto flutuante).

# Define opcode constants
OPCODES = {
    'fld': 0,
    'fsd': 1,
    'fadd': 2,
    'fsub': 3,
    'fmul': 4,
    'fdiv': 5
}

# Define register prefix constants
REG_PREFIXES = {
    'x': 'int',
    'f': 'float'
}

class ParseType(Enum):
    PROG = 1
    CFG = 2

class Step(Enum):
    ISSUE = 0,
    READ = 1,
    EXECUTE = 2,
    WRITE = 3,
    DONE = 4

def gen_instructions_board(configuration):
    instructions = []
    for i in configuration:
        status = np.zeros(4, dtype=np.uint32)
        instructions.append({
            'info': i,
            'status': status,
            'step': Step.ISSUE
        })
    return instructions

def gen_functional_units(configuration):
    functional_units = []
    for fu in configuration:
        for i in range(fu['quantity']):
            name = fu['name']
            identifier = i+1
            cycles = fu['cycles']
            status = np.zeros(9, dtype=np.uint32)
            functional_units.append({
                'name': name,
                'id': identifier,
                'cycles': cycles,
                'status': status
            })
    return functional_units

