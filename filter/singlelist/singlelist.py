#!/usr/bin/env python3
"""
Makes ordered lists between open and close div tags one big list.
Picks the first ordered list type it hits after opening tag as the list to match on.
To have nested singlelists, use unique id tags in the opening div.

Example:

    <div class="FILTER-singlelist">
    1. hello
    2. there

    more text

    1. hello again
    2. there again
    </div>


-- filter transforms to ->>>:
    1. hello
    2. there

    more text

    3. hello again
    4. there again
"""

import json
import sys
import os
from pandocfilters import *

def transform_div(key, value, format, meta):
    if key == 'Div' and "FILTER-singlelist" in value[0][1]:
        return singlelist(value[1], None)

def singlelist(lst, pat):
    if lst == []:
        return []
    x = lst[0]   # head
    xs = lst[1:]  # tail
    if type(x) is dict and 't' in x and x['t'] == 'OrderedList':
        spec = list(x['c'][0])
        items = list(x['c'][1])
        if pat == None:
            # if first list hit, use as the pattern to match on
            pat = spec
            offset = len(items)
            pat[0] += offset
        elif spec[1] == pat[1] and spec[2] == pat[2]:
            # if matches spec of current pattern, then increment it
            x['c'][0][0] = pat[0]
            offset = len(items)
            pat[0] += offset
    return [x] + singlelist(xs, pat)

if __name__ == "__main__":
    toJSONFilter(transform_div)

