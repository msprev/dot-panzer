#!/usr/bin/env python3
"""
Add acknowledgements section heading at end of document based on metadata field of same name:

    # Acknowledgements

"""

import json
import sys
import os
from pandocfilters import *


def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    if 'acknowledgements' in ast['meta']:
        # sys.stderr.write(str(ast['blocks'][2]))
        # sys.stderr.write('\n')
        # sys.stderr.write(str(Para([Str('hell')])))
        # sys.stderr.write('\n')
        # sys.stderr.flush()
        ast['blocks'] += [Header(1, ["acknowledgements",["unnumbered"],[]], [Str('Acknowledgements')])]
        ast['blocks'] += [Para(ast['meta']['acknowledgements']['c'])]
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

