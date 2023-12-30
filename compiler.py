#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Jussi Pakkanen

import argparse, sys, os, time

p = argparse.ArgumentParser(prog='Fake compiler')
p.add_argument('-o', dest='objfile', required=True)
p.add_argument('sources', nargs='+')
p.add_argument('-d', help='Execution time in seconds', type=int, default=1)

def compile():
    args = p.parse_args()
    if len(args.sources) != 1:
        sys.exit('Must have exactly one source, got: ' + str( args.sources))
    cppfile = args.sources[0]
    if not os.path.exists(cppfile):
        sys.exit(f'Source file {cppfile} does not exist.')
    time.sleep(args.d)
    depfile = args.objfile + '.d'
    with open(args.objfile, 'w') as objfile:
        objfile.write('This is an object file.\n')
    with open(depfile, 'w') as objfile:
        # Does not handle spaces in paths.
        objfile.write(f'{args.objfile}: {cppfile}\n')

if __name__ == '__main__':
    compile()

