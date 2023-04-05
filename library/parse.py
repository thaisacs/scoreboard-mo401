from enum import Enum
import sys

# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------

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

#def parse_file(filename):
#    instructions = []
#    with open(filename, 'r') as f:
#        for line in f:
#            fields = line.strip().replace(',', ' ').split()
#            opcode = fields[0].lower()
#            if opcode not in OPCODES:
#                raise ValueError(f'Invalid opcode: {opcode}')
#            opcode = OPCODES[opcode]
#            rs1, rs2, rd, imm = 0, 0, 0, None  # Set imm to None by default
#            rs1_type, rs2_type, rd_type = None, None, None
#            if opcode == 0:  # fld format: "instruction rd imm(rs1)"
#                rd = int(fields[1][1:])
#                rd_type = REG_PREFIXES[fields[1][0].lower()]
#                rs1_imm = fields[2].split('(')
#                imm = int(rs1_imm[0])
#                rs1 = int(rs1_imm[1][1:-1])
#                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
#            elif opcode == 1:  # fsd format: "instruction rs2 imm(rs1)"
#                rs2 = int(fields[1][1:])
#                rs2_type = REG_PREFIXES[fields[1][0].lower()]
#                rs1_imm = fields[2].split('(')
#                imm = int(rs1_imm[0])
#                rs1 = int(rs1_imm[1][1:-1])
#                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
#            else:  # Other instructions format: "instruction rd rs1 rs2"
#                rd = int(fields[1][1:])
#                rd_type = REG_PREFIXES[fields[1][0].lower()]
#                rs1 = int(fields[2][1:])
#                rs1_type = REG_PREFIXES[fields[2][0].lower()]
#                if len(fields) > 3:
#                    rs2 = int(fields[3][1:])
#                    rs2_type = REG_PREFIXES[fields[3][0].lower()]
#                else:
#                    rs2 = 0
#                    rs2_type = None
#            instructions.append({
#                'opcode': opcode,
#                'rs1': rs1,
#                'rs1_type': rs1_type,
#                'rs2': rs2,
#                'rs2_type': rs2_type,
#                'rd': rd,
#                'rd_type': rd_type,
#                'imm': imm
#            })
#    return instructions
