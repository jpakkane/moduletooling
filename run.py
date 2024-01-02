#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Jussi Pakkanen

import os, sys, subprocess, shutil, pathlib

srcdir = pathlib.Path('source')
builddir = pathlib.Path('build')

if srcdir.exists():
    shutil.rmtree(srcdir)
if builddir.exists():
    shutil.rmtree(builddir)

subprocess.check_call(['./projectgenerator.py',
                       '--source',
                       srcdir,
                       '--build',
                       builddir])