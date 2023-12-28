#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Jussi Pakkanen

import argparse, sys, os, pathlib

p = argparse.ArgumentParser(prog='Module test project generator')
p.add_argument('--source', help='Root dir for sources.', required=True)
p.add_argument('--build', help='Root dir for build.', required=True)

def create_sources(path, template):
    num_sources = 10
    for i in range(num_sources):
        fname = path / (template % i)
        with open(fname, 'w') as ofile:
            ofile.write('This is a source file.\n')

def generate():
    args = p.parse_args()
    if os.path.exists(args.source):
        sys.exit('Source dir already exists.')
    if os.path.exists(args.build):
        sys.exit('Build dir already exists.')
    srcdir = pathlib.Path(args.source)
    builddir = pathlib.Path(args.build)
    ninjafile = builddir / 'build.ninja'
    srcdir.mkdir()
    builddir.mkdir()
    create_sources(srcdir, 'target0src%d.cpp')
    with open(ninjafile, "w") as n:
        n.write('ninja_required_version = 1.11.2\n\n')
        n.write('# Rules\n\n')
        n.write('# Actual work steps\n\n')
        n.write('# The all important all target\n\n')
        n.write('default all\n')

if __name__ == '__main__':
    generate()
