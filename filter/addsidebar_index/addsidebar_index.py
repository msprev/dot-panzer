#!/usr/bin/env python3
"""
Write an index from headings and subheadings (used for my website)

    sidebar_index:
        - href: "#introduction"
          title: "1 &nbsp; Introduction"
        - href: "#kinds-of-realism"
          title: "2 &nbsp; Kinds of realism"
        - href: "#why-care-about-mind-independence"
          title: "3 &nbsp; Why care about mind independence?"
        - subsection: true
          contents:
            - href: "#why-care-about-mind-independence"
              title: "5.1 &nbsp; Why care about mind independence?"
            - href: "#why-care-about-mind-independence"
              title: "5.1 &nbsp; Why care about mind independence?"
        - href: "#kinds-of-realism"
          title: "2 &nbsp; Kinds of realism"
        - href: "#why-care-about-mind-independence"
          title: "3 &nbsp; Why care about mind independence?"

"""

import sys
import pickle
from pandocfilters import *

def heads(key, value, format, meta):
    if key == 'Header':
        level = value[0]
        if level == 1 or level == 2:
            if heads.insubsection and level == 1:
                heads.insubsection = False
            if not heads.insubsection and level == 2:
                heads.sidebar_index += [{ 'subsection': True, 'contents': list() }]
                heads.insubsection = True
                heads.subsectnum = 1
            href = '#' + value[1][0]
            sect_title = stringify(value[2][0:]).strip()
            if heads.insubsection:
                title = str(heads.sectnum-1) + '.' + str(heads.subsectnum) + ' &nbsp; ' + sect_title
                heads.sidebar_index[-1]['contents'] += [{ 'href': href, 'title': title }]
                heads.subsectnum += 1
            else:
                title = str(heads.sectnum) + ' &nbsp; ' + sect_title
                heads.sidebar_index += [{ 'href': href, 'title': title }]
                heads.sectnum += 1
            # sys.stderr.write('\n')
            # sys.stderr.write('sectionnum: %s \n' % str(heads.sectnum))
            # sys.stderr.write('level: %s \n' % str(level))
            # sys.stderr.write('href: %s \n' % href)
            # sys.stderr.write('sect_title: %s \n' % str(sect_title))
            # sys.stderr.write('index: %s \n' % str(heads.sidebar_index))
            # sys.stderr.write('insubsection: %s \n' % str(heads.insubsection))
            # sys.stderr.write('\n')
            # sys.stderr.flush()

heads.sidebar_index = []
heads.insubsection = False
heads.sectnum = 1
heads.subsectnum = 1

if __name__ == "__main__":
    toJSONFilter(heads)
    fname = 'tmp_index.pickle'
    with open(fname, 'wb') as fp:
        pickle.dump(heads.sidebar_index, fp)
    from pprint import pprint
    # sys.stderr.write('\n')
    # sys.stderr.write('\n')
    # pprint(heads.sidebar_index, stream=sys.stderr)
    # sys.stderr.write('\n')
    # sys.stderr.write('\n')
    # sys.stderr.flush()



