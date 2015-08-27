#!/usr/bin/env python3
"""
Add page break at the start of each H1 section

    --- page break ---

    # Section

"""

import json
import sys
import os
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools
from pandocfilters import *

def rehead(key, value, format, meta):
    if key == 'Header' and value[0] == 1:
        if format == 'latex':
            text = '\\newpage\n\\thispagestyle{empty}\n\\setcounter{page}{1}'
            insert = RawInline('latex', text)
        elif format == 'html':
            text = '<hr>'
            insert = RawInline('html', text)
        return [Para([insert]), Header(value[0], value[1], value[2])]

if __name__ == "__main__":
    panzertools.log('INFO', 'adding page break before each H1 section')
    toJSONFilter(rehead)

