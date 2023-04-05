import numpy as np
from enum import Enum

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

class Scoreboard:
    def __init__(self, instructions, functional_units):
        functional_units = gen_functional_units(functional_units)
        instructions = gen_instructions_board(instructions)
        self.status = {
            'register_f': np.zeros(20, dtype=np.uint32),
            'register_i': np.zeros(20, dtype=np.uint32),
            'functional_units': functional_units,
            'instructions': instructions
        }

    def run(self):
        instruction_size = len(self.status['instructions'])
        instruction_issue = 0
        instruction = None
        cycle = 1

        while(instruction_issue < instruction_size):
            for i in range(instruction_issue, -1, -1):
                instruction = self.status['instructions'][i]

                info = instruction['info']
                status = instruction['status']
                step = instruction['step']

                if(step == Step.ISSUE):
                    instruction['step'] = Step.READ
                    status[0] = cycle
                    instruction_issue = instruction_issue + 1
                elif(step == Step.READ):
                    instruction['step'] = Step.EXECUTE
                elif(step == Step.EXECUTE):
                    instruction['step'] = Step.WRITE
                elif(step == Step.WRITE):
                    instruction['step'] = Step.DONE
                
            cycle = cycle + 1

    def dump_board(self):
        instructions = self.status['instructions']
        
        print('ISSUE   -   READ   -   EXECUTE   -   WRITE   ')

        for i in instructions:
            status = i['status']
            print(status)

