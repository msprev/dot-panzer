#!/usr/bin/env python
"""
Test filter -- dumps the ast, without changing it, as a json to stderr for printing by panzer
"""

import json
import os
import sys
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools


def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    outgoing = { 'level': 'INFO', 'message': json.dumps(ast) }
    outgoing_json = json.dumps(outgoing) + '\n'
    outgoing_bytes = outgoing_json.encode('utf8')
    sys.stderr.write(outgoing_bytes)
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
