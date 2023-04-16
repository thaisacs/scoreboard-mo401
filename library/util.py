#!/usr/bin/python3

from enum import Enum
import numpy as np
import sys

# --------------------------------------------------------------------------------------------

#fld (usa unidade de inteiros)
#fsd (usa unidade de inteiros)
#fadd (usa somador de ponto flutuante)
#fsub (usa somador de ponto flutuante)
#fmul (usa multiplicador de ponto flutuante)
#fdiv (usa divisor de ponto flutuante).
NONE_ID = -1

PIPELINE_DEPTH = 4

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
        status = np.zeros(PIPELINE_DEPTH, dtype=np.uint32)
        instructions.append({
            'info': i,
            'fu_id': NONE_ID,
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
            status = {
                'busy': '-',
                'fi': '-',
                'fj': '-',
                'fk': '-',
                'qj': '-',
                'qk': '-',
                'rj': '-',
                'rk': '-',
            }
            functional_units.append({
                'name': name,
                'id': identifier,
                'cycles': cycles,
                'status': status
            })
    return functional_units

def decode_reg(register):
    rd = int(register[1:])
    rd_type = REG_PREFIXES[register[1][0].lower()]

def code_reg(reg_number, reg_type):
    if(reg_type == 'int'):
        return 'x' + str(reg_number)
    return reg_type[0] + str(reg_number)

def parse_file(filename: str, parse: ParseType):
    collector = []

    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print(f"File {filename} not found.  Aborting.")
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error opening {filename} is {repr(err)}.")
        sys.exit(1)

    if(parse == ParseType.CFG):
        for line in f:
            fields = line.strip().replace(',', ' ').split()
            name = fields[0].lower()
            quantity = int(fields[1])
            cycles = int(fields[2])
            collector.append({
                'name': name,
                'quantity': quantity,
                'cycles': cycles,
            })
    else:
        for line in f:
            fields = line.strip().replace(',', ' ').split()
            opcode = fields[0].lower()
            if opcode not in OPCODES:
                raise ValueError(f'Invalid opcode: {opcode}')
            opcode = OPCODES[opcode]
            rs1, rs2, rd, imm = 0, 0, 0, None  # Set imm to None by default
            rs1_type, rs2_type, rd_type = None, None, None
            if opcode == 0:  # fld format: "instruction rd imm(rs1)"
                rd = int(fields[1][1:])
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = int(rs1_imm[1][1:-1])
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            elif opcode == 1:  # fsd format: "instruction rs2 imm(rs1)"
                rs2 = int(fields[1][1:])
                rs2_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = int(rs1_imm[1][1:-1])
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            else:  # Other instructions format: "instruction rd rs1 rs2"
                rd = int(fields[1][1:])
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1 = int(fields[2][1:])
                rs1_type = REG_PREFIXES[fields[2][0].lower()]
                if len(fields) > 3:
                    rs2 = int(fields[3][1:])
                    rs2_type = REG_PREFIXES[fields[3][0].lower()]
                else:
                    rs2 = 0
                    rs2_type = None
            collector.append({
                'opcode': opcode,
                'rs1': rs1,
                'rs1_type': rs1_type,
                'rs2': rs2,
                'rs2_type': rs2_type,
                'rd': rd,
                'rd_type': rd_type,
                'imm': imm
            })
    return collector

