#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Simulador de execução fora de ordem com Scoreboard.\n')
parser.add_argument(
        '-p',
        '--program',
        type=str, help=' (default: example.s)',
        default='example.s')
parser.add_argument(
        '-c',
        '--configuration',
        type=str, help=' (default: cfg.in)',
        default='cfg.in')

def main():
    args = parser.parse_args()

if __name__ == '__main__':
    main()
