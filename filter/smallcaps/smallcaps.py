#!/usr/bin/env python3
"""
Transforms all items listed in 'smallcaps:' metadata field to small caps.

    smallcaps:
        - ONE
        - TWO

transforms:

    Lorem ONE ipsum dolor TWO sit amet

to use small caps for ONE and TWO.

Will transform anything in the list in the document delimited by whitespace or punctuation.
"""

import sys
import os
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools
from pandocfilters import toJSONFilter, Str, SmallCaps, stringify

def get_list(meta):
    if get_list.checked == True:
        pass
    else:
        try:
            get_list.checked = True
            get_list.hitlist = [stringify(x) for x in meta.get('smallcaps', {})['c']]
            panzertools.log('INFO', 'small caps: ' + repr(get_list.hitlist))
        except KeyError:
            pass
    return get_list.hitlist

get_list.hitlist = list()
get_list.checked = False

def clean(word):
    """
    target words are delimited by letters or digits
    """
    clean_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    word_index = range(0, len(word))
    for start in word_index:
        if word[start] in clean_chars:
            break
    for end in reversed(word_index):
        if word[end] in clean_chars:
            break
    return(word[start:end+1])

def smallcaps(key, value, format, meta):
    if key == 'Str':
        if clean(value) in get_list(meta):
            return SmallCaps([Str(value.lower())])

if __name__ == "__main__":
    toJSONFilter(smallcaps)

