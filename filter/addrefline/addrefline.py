#!/usr/bin/env python3
"""
Add extra section heading at end of document:

    # References

"""

import json
import sys
import os
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools
from pandocfilters import *


def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    panzertools.log('INFO', 'adding "References" section heading')
    try:
        ast['blocks'].append(Header(1, attributes({'id': 'references', 'classes': ['unnumbered']}), [Str('References')]))
    except (KeyError, IndexError):
        panzertools.log('WARNING', '"name" field inside "author" field not found')
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

