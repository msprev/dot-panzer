#!/usr/bin/env python3
# encoding: utf-8

import sys

input_lines  = sys.stdin.readlines()
output_lines = []
closed = False

for l in input_lines:
    if not closed and l == '...\n':
        output_lines.append('---\n')
        closed = True
    else:
        output_lines.append(l)

for line in output_lines:
    sys.stdout.write(line)

sys.stdout.flush()

