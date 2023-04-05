from library.util import Step
from library.util import gen_instructions_board
from library.util import gen_functional_units
from enum import Enum
import numpy as np

class Scoreboard:
    def __init__(self, instructions, functional_units):
        functional_units = gen_functional_units(functional_units)
        instructions = gen_instructions_board(instructions)
        self.status = {
            'register_f': np.zeros(20, dtype=np.uint32),
            'register_i': np.zeros(20, dtype=np.uint32),
            'functional_units': functional_units,
            'instructions': instructions,
            'mapping': []
        }

    def check_reg(self, info):
        #print(self.status['register_i'])
        #print(self.status['register_f'])
        #for i in self.status['functional_units']:
        #    print(i)
        #for i in self.status['instructions']:
        #    print(i)

        print(info)
        if(info['rd_type'] == 'float'):
            if(self.status['register_f'][info['rd']] == 0):
                return True
        elif(info['rd_type'] == 'int'):
            if(self.status['register_i'][info['rd']] == 0):
                return True
        elif(info['rd_type'] == None):
            return True
        return False

    def check_fu(self, info):
        fus = self.status['functional_units']
        op = info['opcode']
        for fu in fus:
            name = fu['name']
            if(fu['status'][0] == 0):
                if((op == 0 or op == 1) and name == 'int'):
                    return True
                elif((op == 2 or op == 3) and name == 'add'):
                    return True
                elif(op == 4 and name == 'mult'):
                    return True
                elif(op == 5 and name == 'div'):
                    return True
        return False

    def get_reg(self, info):
        return

    def get_fu(self, info):
        return

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
                    if(self.check_fu(info) and self.check_reg(info)):
                        #self.get_fu(info)
                        #self.get_reg(info)
                        status[0] = cycle
                        instruction['step'] = Step.READ
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

