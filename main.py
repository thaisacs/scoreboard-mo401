#!/usr/bin/python3

import argparse
from library.parse import parse_file
from library.parse import ParseType

# --------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Simulador de execução fora de ordem com Scoreboard.\n')
parser.add_argument(
        '-p',
        '--program',
        type=str, help=' (default: inputs/example.s)',
        default='inputs/example.s')
parser.add_argument(
        '-c',
        '--configuration',
        type=str, help=' (default: inputs/cfg.in)',
        default='inputs/cfg.in')

# --------------------------------------------------------------------------------------------

def main():
    args = parser.parse_args()
    instructions = parse_file(args.program, ParseType.PROG)
    functional_units = parse_file(args.configuration, ParseType.CFG)

if __name__ == '__main__':
    main()
