#!/usr/bin/python3
from enum import Enum
import numpy as np

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
            name = fu['name']+str(i+1)
            cycles = fu['cycles']
            status = np.zeros(9, dtype=np.uint32)
            functional_units.append({
                'name': name,
                'cycles': cycles,
                'status': status
            })
    return functional_units

