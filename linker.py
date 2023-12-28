#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Jussi Pakkanen

import argparse, sys, os, time

p = argparse.ArgumentParser(prog='Fake linker')
p.add_argument('-o', dest='output', required=True)
p.add_argument('objs', nargs='+')
p.add_argument('-d', help='Execution time in seconds', type=int, default=1)

def compile():
    args = p.parse_args()
    for o in args.objs:
        if not os.path.exists(o):
            sys.exit(f'Input file {o} does not exist.'))
    time.sleep(args.d)
    with open(args.output, 'w') as outfile:
        if args.output.endswith('.a') or args.output.ends_with('.lib'):
            outfile.write('This is a static library file.\n')
        elif args.output.endswith('.so') or args.output.ends_with('.dll'):
            outfile.write('This is a shared library file.\n')
        else:
            outfile.write('This is an executable file.\n')

if __name__ == '__main__':
    link()