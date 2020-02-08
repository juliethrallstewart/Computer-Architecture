#!/usr/bin/env python3

"""Main."""

# python3 ls8.py examples/stack.ls8

import sys
from cpu import *

cpu = CPU()

# cpu.load_memory(sys.argv[1])
cpu.load()
cpu.run()