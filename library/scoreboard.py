#!/usr/bin/python3

from library.util import Step
from library.util import gen_instructions_board
from library.util import gen_functional_units
from library.util import code_reg, decode_reg
from library.util import NONE_ID
from enum import Enum
import numpy as np

import sys

class Scoreboard:
    def __init__(self, instructions, functional_units):
        self.cycle = 1
        self.functional_units = gen_functional_units(functional_units)
        self.instructions = gen_instructions_board(instructions)
        self.register_f = NONE_ID*np.ones(32, dtype=np.uint32)
        self.register_i = NONE_ID*np.ones(32, dtype=np.uint32)

    def check_reg(self, info):
        # check if the write register is free
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
        # check if there is a functional unit
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

    def set_fqr(self, info, fu_id, register_id, register_name):
        if(info[register_id+'_type'] == None):
            self.functional_units[fu_id]['status']['f'+register_name] = '-'
            self.functional_units[fu_id]['status']['q'+register_name] = '-'
            self.functional_units[fu_id]['status']['r'+register_name] = 'Y'
        else:
            self.functional_units[fu_id]['status']['f'+register_name] = code_reg(info[register_id], info[register_id+'_type'])
            if(info[register_id+'_type'] == 'float'):
                if(self.register_f[info[register_id]] == NONE_ID):
                    self.functional_units[fu_id]['status']['q'+register_name] = '-'
                    self.functional_units[fu_id]['status']['r'+register_name] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['q'+register_name] = self.register_f[info[register_id]]
                    self.functional_units[fu_id]['status']['r'+register_name] = 'N'
            else:
                if(self.register_i[info[register_id]] == NONE_ID):
                    self.functional_units[fu_id]['status']['q'+register_name] = '-'
                    self.functional_units[fu_id]['status']['r'+register_name] = 'Y'
                else:
                    self.functional_units[fu_id]['status']['q'+register_name] = self.register_i[info[register_id]]
                    self.functional_units[fu_id]['status']['r'+register_name] = 'N'


    def reserve_reg_fu(self, info, fu_id):
        # reserve functional unit
        self.functional_units[fu_id]['status']['busy'] = 'Y'

        # set rd in functional unit
        if(info['rd_type'] == None):
            self.functional_units[fu_id]['status']['fi'] = '-'
        else:
            self.functional_units[fu_id]['status']['fi'] = code_reg(info['rd'], info['rd_type'])

        # set rs1 and rs2 in functional unit
        self.set_fqr(info, fu_id, 'rs1', 'j')
        self.set_fqr(info, fu_id, 'rs2', 'k')

        # reserve destination register
        if(info['rd_type'] == 'float'):
            self.register_f[info['rd']] = fu_id
        elif(info['rd_type'] == 'int'):
            self.register_i[info['rd']] = fu_id

    def read_regs(self, info, fu_id):
        if(self.functional_units[fu_id]['status']['rj'] == 'Y' and self.functional_units[fu_id]['status']['rk'] == 'Y'):
            self.functional_units[fu_id]['status']['rj'] = 'N'
            self.functional_units[fu_id]['status']['rk'] = 'N'
            return True
        return False

    def execute(self, info, fu_id, read_cycle):
        cycles = self.functional_units[fu_id]['cycles']
        current_cycle = self.cycle
        if(current_cycle - read_cycle == cycles):
            return True
        return False

    def check_write(self, info, fu_id):
        # check if the instruction can write 
        if(info['rd_type'] != None):
            register = code_reg(info['rd'], info['rd_type'])

            for f in self.functional_units:
                if(f['status']['fj'] == register and f['status']['rj'] == 'Y'):
                    return False
                if(f['status']['fk'] == register and f['status']['rk'] == 'Y'):
                    return False
        return True

    def write(self, info, fu_id):
        # set register
        if(info['rd_type'] == 'float'):
            if(self.register_f[info['rd']] == fu_id):
                self.register_f[info['rd']] = NONE_ID
        elif(info['rd_type'] == 'int'):
            if(self.register_i[info['rd']] == fu_id):
                self.register_i[info['rd']] = NONE_ID

        # clean functional unit
        self.functional_units[fu_id]['status']['busy'] = '-'
        self.functional_units[fu_id]['status']['fi'] = '-'
        self.functional_units[fu_id]['status']['fj'] = '-'
        self.functional_units[fu_id]['status']['fk'] = '-'
        self.functional_units[fu_id]['status']['qj'] = '-'
        self.functional_units[fu_id]['status']['rk'] = '-'
        self.functional_units[fu_id]['status']['rj'] = '-'
        self.functional_units[fu_id]['status']['rk'] = '-'

        # check the others functional units
        for fid in range(len(self.functional_units)):
            if(type(self.functional_units[fid]['status']['qj']) == np.int64):
                if(self.functional_units[fid]['status']['qj'] == fu_id):
                    self.functional_units[fid]['status']['qj'] = '-'
                    self.functional_units[fid]['status']['rj'] = 'Y'
            if(type(self.functional_units[fid]['status']['qk']) == np.int64):
                if(self.functional_units[fid]['status']['qk'] == fu_id):
                    self.functional_units[fid]['status']['qk'] = '-'
                    self.functional_units[fid]['status']['rk'] = 'Y'

    def done(self):
        for i in self.instructions:
            if(i['step'] != Step.DONE):
                return False
        return True

    def run(self):
        instruction_size = len(self.instructions)
        instruction_point = 0
        instruction = None

        while(not self.done()):
            if(instruction_point >= instruction_size):
                instruction_point = instruction_size - 1

            for i in range(instruction_point, -1, -1):
                instruction = self.instructions[i]
                
                info = instruction['info']
                status = instruction['status']
                step = instruction['step']
                fu_id = instruction['fu_id']

                if(step == Step.ISSUE):
                    fu_id = self.check_fu(info)
                    if(fu_id != NONE_ID and self.check_reg(info)):
                        self.reserve_reg_fu(info, fu_id)
                        instruction['fu_id'] = fu_id
                        status[0] = self.cycle
                        instruction['step'] = Step.READ
                        instruction_point = instruction_point + 1
                elif(step == Step.READ):
                    if(self.read_regs(info, fu_id)):
                        status[1] = self.cycle
                        instruction['step'] = Step.EXECUTE
                elif(step == Step.EXECUTE):
                    if(self.execute(info, fu_id, status[1])):
                        status[2] = self.cycle
                        instruction['step'] = Step.WRITE
                elif(step == Step.WRITE):
                    if(self.check_write(info, fu_id)):
                        self.write(info, fu_id)
                        status[3] = self.cycle
                        instruction['step'] = Step.DONE

            self.cycle = self.cycle + 1

    def dump_board(self, instructions, program):
        f = open(program, 'r')
        k = 0
        program_lines = []

        for line in f:
            program_lines.append(line.replace('\n', ''))

        print('instruction [ISSUE READ EXECUTE WRITE]')

        for i in self.instructions:
            status = i['status']
            print(f"{program_lines[k]} {status}")
            k = k + 1

    def dump_head(self, program, config):
        print("                        _                         _ ")
        print("                       | |                       | |")
        print(" ___  ___ ___  _ __ ___| |__   ___   __ _ _ __ __| |")
        print("/ __|/ __/ _ \| '__/ _ \ '_ \ / _ \ / _` | '__/ _` |")
        print("\__ \ (_| (_) | | |  __/ |_) | (_) | (_| | | | (_| |")
        print("|___/\___\___/|_|  \___|_.__/ \___/ \__,_|_|  \__,_|")
        print("____________________________________________________")
        print("")
        print("      program file: ", program)
        print("configuration file: ", config)
        print("")
        print("                                 by: thais camacho  ")
        print("____________________________________________________")
