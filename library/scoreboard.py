import numpy as np

def gen_instructions_board(configuration):
    instructions = []
    for i in configuration:
        status = np.zeros(4, dtype=np.uint32)
        instructions.append({
            'instruction': i,
            'status': status,
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

class Scoreboard:
    def __init__(self, instructions, functional_units):
        functional_units = gen_functional_units(functional_units)
        instructions = gen_instructions_board(instructions)
        status = {
            'register_f': np.zeros(10, dtype=np.uint32),
            'register_i': np.zeros(10, dtype=np.uint32),
            'functional_units': functional_units,
            'instructions': instructions
        }

    def run(self):
        print('running')
