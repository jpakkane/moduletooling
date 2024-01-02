#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Jussi Pakkanen

import argparse, sys, os, pathlib, random

p = argparse.ArgumentParser(prog='Module test project generator')
p.add_argument('--source', help='Root dir for sources.', required=True)
p.add_argument('--build', help='Root dir for build.', required=True)

def gen_imports(template, i):
    imports = []
    if i < 1:
        return imports
    used_imports = set()
    num_imports = random.randrange(min(i, 4))
    while len(used_imports) < num_imports:
        modnum = random.randrange(i)
        if modnum not in used_imports:
            used_imports.add(modnum)
            imports.append(template % modnum)
    return imports

def create_sources(path, template):
    srclist = []
    num_sources = 10
    for i in range(num_sources):
        fname = pathlib.Path(template % i).with_suffix('.cpp')
        modulename = template % i
        srclist.append(fname)
        full_name = path / fname
        with open(full_name, 'w') as ofile:
            ofile.write(f'export {modulename}\n\n')
            imports = gen_imports(template, i)
            for imp in imports:
                ofile.write(f'import {imp}\n')
    return srclist

def create_rules(ninjafile):
    tooldir = pathlib.Path(__file__).parent
    compiler = tooldir / 'compiler.py'
    linker= tooldir / 'linker.py'
    assert(compiler.is_file())

    ninjafile.write('rule compiler\n')
    ninjafile.write(f' command = {compiler} $args -o $out $in\n')
    ninjafile.write(' deps = gcc\n')
    ninjafile.write(' depfile = $DEPFILE\n')
    ninjafile.write(' description = Compiling source file $out\n')
    ninjafile.write('\n')

    ninjafile.write('rule linker\n')
    ninjafile.write(f' command = {linker} -o $out $in\n')
    ninjafile.write(' description = Linking target $out\n')
    ninjafile.write('\n')

    ninjafile.write('rule command\n')
    ninjafile.write(' command = $COMMAND\n')
    ninjafile.write(' description = $DESC\n')
    ninjafile.write('\n')

def write_compilations(ninjafile, build_to_src, srclist):
    objfiles = []
    for src in srclist:
        objfile = pathlib.Path(src.name).with_suffix('.o')
        depfile = str(objfile) + '.d'
        objfiles.append(objfile)
        rel_src = build_to_src / src
        ninjafile.write(f'build {objfile}: compiler {rel_src}\n')
        ninjafile.write(' args = \n')
        ninjafile.write(f' DEPFILE = {depfile}\n')
        ninjafile.write(' \n')
    return objfiles

def write_link(ninjafile, output, objlist):
    ninjafile.write(f'build {output}: linker')
    for o in objlist:
        ninjafile.write(' ')
        ninjafile.write(str(o))
    ninjafile.write('\n')
    # link args would go here
    ninjafile.write('\n')

def generate():
    args = p.parse_args()
    if os.path.exists(args.source):
        sys.exit('Source dir already exists.')
    if os.path.exists(args.build):
        sys.exit('Build dir already exists.')
    srcdir = pathlib.Path(args.source)
    builddir = pathlib.Path(args.build)
    build_to_src = '..' / srcdir # FIXME
    ninjafile = builddir / 'build.ninja'
    srcdir.mkdir()
    builddir.mkdir()
    with open(ninjafile, "w") as n:
        output = 'prog'
        n.write('ninja_required_version = 1.11.2\n\n')
        n.write('# Rules\n\n')
        create_rules(n)
        n.write('# Actual work steps\n\n')
        srclist = create_sources(srcdir, 'target0src%d')
        objlist = write_compilations(n, build_to_src, srclist)
        write_link(n, output, objlist)
        n.write('# Housekeeping targets\n\n')
        n.write(f'build clean: phony actualclean\n\n')
        n.write(f'build actualclean: command\n')
        n.write( ' COMMAND = ninja -t clean\n')
        n.write( ' description = Cleaning\n\n')
        n.write('# The all important all target\n\n')
        n.write(f'build all: phony {output}\n\n')
        n.write('default all\n')

if __name__ == '__main__':
    generate()
