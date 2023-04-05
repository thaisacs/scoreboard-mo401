from library.util import Step
from library.util import gen_instructions_board
from library.util import gen_functional_units
from library.util import code_reg, decode_reg
from library.util import NONE_ID
from enum import Enum
import numpy as np

class Scoreboard:
    def __init__(self, instructions, functional_units):
        self.functional_units = gen_functional_units(functional_units)
        self.instructions = gen_instructions_board(instructions)
        self.register_f = -1*np.ones(20, dtype=np.uint32)
        self.register_i = -1*np.ones(20, dtype=np.uint32)

    def check_reg(self, info):
        if(info['rd_type'] == 'float'):
            if(self.register_f[info['rd']] == NONE_ID):
                return True
        elif(info['rd_type'] == 'int'):
            if(self.register_i[info['rd']] == NONE_ID):
                return True
        elif(info['rd_type'] == None):
            return True
        return False

    def check_fu(self, info):
        fus = self.functional_units
        op = info['opcode']
        for fu_id in range(len(fus)):
            fu = fus[fu_id]
            name = fu['name']
            if(fu['status']['busy'] == '-'):
                if((op == 0 or op == 1) and name == 'int'):
                    return fu_id
                elif((op == 2 or op == 3) and name == 'add'):
                    return fu_id
                elif(op == 4 and name == 'mult'):
                    return fu_id
                elif(op == 5 and name == 'div'):
                    return fu_id
        return NONE_ID

    def reserve_reg_fu(self, info, fu_id):
        self.functional_units[fu_id]['status']['busy'] = 'Y'
        if(info['rd_type'] == None):
            self.functional_units[fu_id]['status']['fi'] = '-'
        else:
            self.functional_units[fu_id]['status']['fi'] = code_reg(info['rd'], info['rd_type'])

        if(info['rs1_type'] == None):
            self.functional_units[fu_id]['status']['fj'] = '-'
            self.functional_units[fu_id]['status']['qj'] = '-'
            self.functional_units[fu_id]['status']['rj'] = 'Y'
        else:
            self.functional_units[fu_id]['status']['fj'] = code_reg(info['rs1'], info['rs1_type'])
            if(info['rs1_type'] == 'float'):
                if(self.register_f[info['rs1']] == NONE_ID):
                    self.functional_units[fu_id]['status']['qj'] = '-'
                    self.functional_units[fu_id]['status']['rj'] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['qj'] = str(self.register_f[info['rs1']])
                    self.functional_units[fu_id]['status']['rj'] = 'N'
            else:
                if(self.register_i[info['rs1']] == NONE_ID):
                    self.functional_units[fu_id]['status']['qj'] = '-'
                    self.functional_units[fu_id]['status']['rj'] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['qj'] = str(self.register_i[info['rs1']])
                    self.functional_units[fu_id]['status']['rj'] = 'N'

        if(info['rs2_type'] == None):
            self.functional_units[fu_id]['status']['fk'] = '-'
            self.functional_units[fu_id]['status']['qk'] = '-'
            self.functional_units[fu_id]['status']['rk'] = 'Y'
        else:
            self.functional_units[fu_id]['status']['fk'] = code_reg(info['rs2'], info['rs2_type'])
            if(info['rs2_type'] == 'float'):
                if(self.register_f[info['rs2']] == NONE_ID):
                    self.functional_units[fu_id]['status']['qk'] = '-'
                    self.functional_units[fu_id]['status']['rk'] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['qk'] = str(self.register_f[info['rs2']])
                    self.functional_units[fu_id]['status']['rk'] = 'N'
            else:
                if(self.register_i[info['rs2']] == NONE_ID):
                    self.functional_units[fu_id]['status']['qk'] = '-'
                    self.functional_units[fu_id]['status']['rk'] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['qk'] = str(self.register_i[info['rs2']])
                    self.functional_units[fu_id]['status']['rk'] = 'N'

        if(info['rd_type'] == 'float'):
            self.register_f[info['rd']] = fu_id
        elif(info['rd_type'] == 'int'):
            self.register_i[info['rd']] = fu_id

        print(self.functional_units[fu_id]['status'])
        print(info)

    def run(self):
        instruction_size = len(self.instructions)
        instruction_issue = 0
        instruction = None
        cycle = 1

        while(instruction_issue < instruction_size):
            for i in range(instruction_issue, -1, -1):
                instruction = self.instructions[i]
                
                info = instruction['info']
                status = instruction['status']
                step = instruction['step']

                if(step == Step.ISSUE):
                    fu_id = self.check_fu(info)
                    if(fu_id != NONE_ID and self.check_reg(info)):
                        self.reserve_reg_fu(info, fu_id)
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
        print('ISSUE   -   READ   -   EXECUTE   -   WRITE   ')
        for i in self.instructions:
            status = i['status']
            print(status)

