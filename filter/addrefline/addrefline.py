#!/usr/bin/env python3
"""
Add extra section heading at end of document:

    # References

"""

import json
import sys
import os
from pandocfilters import *


def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    # panzertools.log('INFO', 'adding "References" section heading')
    try:
        ast['meta']['reference-section-title'] = dict()
        ast['meta']['reference-section-title']['t'] = 'MetaInlines'
        ast['meta']['reference-section-title']['c'] = [Str('Bibliography')]
    except (KeyError, IndexError):
        pass
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

