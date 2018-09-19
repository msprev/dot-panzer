"""
Add my bibliography file to metadata
"""
#!/usr/bin/env python3

import json
import sys
import os
from pandocfilters import *

BIB = "/Users/msprevak/Dropbox/msprevak/-library-/texmf/bibtex/bib/mds-bib/refs.bib"

def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    try:
        if 'bibliography' not in ast['meta']:
            ast['meta']['bibliography'] = dict()
            ast['meta']['bibliography']['t'] = 'MetaInlines'
            ast['meta']['bibliography']['c'] = [Str(BIB)]
    except (KeyError, IndexError):
        pass
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

