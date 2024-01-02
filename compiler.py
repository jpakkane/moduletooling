#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Jussi Pakkanen

import argparse, sys, os, time

p = argparse.ArgumentParser(prog='Fake compiler')
p.add_argument('-o', dest='objfile', required=True)
p.add_argument('sources', nargs='+')
p.add_argument('-d', help='Execution time in seconds', type=int, default=1)
p.add_argument('--mod-out-dir', dest='moddir', default='.')

def module2filename(modname):
    return modname + '.mod'

class ParseResults:
    def __init__(self, export, imports):
        self.export = export
        self.imports = imports

def parse_source(srcfile):
    imports = []
    export = ''
    for line in open(srcfile):
        line = line.strip()
        if not line:
            continue
        [command, modname] = line.split(' ')
        if command == 'import':
            imports.append(modname)
        elif command == 'export':
            if export:
                sys.exit('Export module declared twice.')
            export = modname
    return ParseResults(export, imports)

def verify_imports(search_dirs, imported_modules):
    imported_module_files = []
    for m in imported_modules:
        mfile = module2filename(m)
        found = False
        for d in search_dirs:
            trial = os.path.join(d, mfile)
            if os.path.exists(trial):
                found = True
                imported_module_files.append(trial)
                break
        if not found:
            sys.exit(f'Module {m} could not be found.')
    return imported_module_files

def compile():
    args = p.parse_args()
    if len(args.sources) != 1:
        sys.exit('Must have exactly one source, got: ' + str( args.sources))
    cppfile = args.sources[0]
    if not os.path.exists(cppfile):
        sys.exit(f'Source file {cppfile} does not exist.')
    presults = parse_source(cppfile)
    module_search_dirs = ['.']
    imported_module_files = verify_imports(module_search_dirs, presults.imports)
    time.sleep(args.d)
    depfile = args.objfile + '.d'
    modfile_name = None
    if presults.export:
        modfile_name = os.path.join(args.moddir, module2filename(presults.export))
        with open(modfile_name, 'w') as modfile:
            modfile.write('This is a module file.\n')
    with open(args.objfile, 'w') as objfile:
        objfile.write('This is an object file.\n')
    with open(depfile, 'w') as depfile:
        # Does not handle spaces in paths.
        depfile.write(f'{args.objfile}: {cppfile}')
        for mf in imported_module_files:
            depfile.write(f' {mf}')
        depfile.write('\n')
        if modfile_name:
            depfile.write(f'{modfile_name}: {cppfile}\n')

if __name__ == '__main__':
    compile()
