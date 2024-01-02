#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Jussi Pakkanen

import argparse, sys, os
from compiler import parse_source, module2filename

p = argparse.ArgumentParser()
p = argparse.ArgumentParser(prog='Fake dep scanner')
p.add_argument('-o', dest='ddfile', required=True)
#p.add_argument('--objfile', dest='objfile', required=True)
p.add_argument('sources', nargs='+')

def src2obj(cppfile):
    # The hackiest of hacks. <o>
    return os.path.split(cppfile)[1][:-4] + '.o'

def scan():
    args = p.parse_args()
    if len(args.sources) == 0:
        sys.exit('No inputs defined.')
    # FIXME, does not handle output directories.
    with open(args.ddfile, 'w') as ddfile:
        ddfile.write('ninja_dyndep_version = 1\n\n')
        for cppfile in args.sources:
            presults = parse_source(cppfile)
            out_mod = module2filename(presults.export)
            objfile = src2obj(cppfile)
            ddfile.write(f'build {objfile} | {out_mod}: dyndep')
            if presults.imports:
                ddfile.write(' |')
                for imp in presults.imports:
                    ddfile.write(' ')
                    ddfile.write(module2filename(imp))
            ddfile.write('\n')

if __name__ == '__main__':
    scan()
