#!/usr/bin/env python3
"""
Remove latex source file generate by pandoc.

Use this when we only care about the final pdf in the current directory, not
the intermediate latex file (a copy of which is stored in .tmp anyway).
"""

import os
import sys
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools


def main():
    OPTIONS = panzertools.read_options()
    filepath = OPTIONS['pandoc']['output']
    if filepath != '-' \
       and not OPTIONS['pandoc']['pdf_output'] \
       and os.path.exists(filepath):
        os.remove(filepath)
        panzertools.log('INFO', 'removed "%s"' % filepath)
    else:
        panzertools.log('INFO', 'not run')



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
