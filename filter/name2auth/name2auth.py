#!/usr/bin/env python3
"""
Transforms metadata:

    author:
        - name: Joe Bloggs
          affiliation: Nowhere
        - name: Jim Brown
          affiliation: Somewhere

-- to -->

    author:
        - Joe Bloggs
        - Jim Brown

The latter format is that assumed by pandoc's default templates. The former, I use in my own templates.
"""

import json
import sys
import os
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools


def main():
    """docstring for main"""
    ast = json.load(sys.stdin)
    panzertools.log('INFO', 'transforming "author" field from list of "name" fields to list of inlines')
    try:
        if ast['meta']['author']['t'] == 'MetaList':
            authors = list()
            for auth in ast['meta']['author']['c']:
                authors.append(dict(auth['c']['name']))
            ast['meta']['author']['t'] = 'MetaList'
            ast['meta']['author']['c'] = authors
            panzertools.log('INFO', 'done')
    except (KeyError, IndexError):
        panzertools.log('WARNING', '"name" field inside "author" field not found')
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

