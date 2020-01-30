#!/usr/bin/env python3

"""Main."""

import sys
from cpu2 import *

cpu = CPU()

# cpu.load_memory(sys.argv[1])
cpu.load()
cpu.run()