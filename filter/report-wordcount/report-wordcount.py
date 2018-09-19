#!/usr/bin/env python3
"""
Takes document as input and gives a pretty word count histogram as output
"""

import json
import sys
import re
from pandocfilters import *

def main():
    """docstring for main"""
    ast = read_ast()
    if not ast['blocks']:
        ast['blocks'] = [Para([Str('Empty file')])]
        write_ast(ast)
        return
    if ast['blocks'][0]['t'] != 'Header':
        dummy = Header(1, ["premlims", ["unnumbered"], []], [Str('[Prelims]')])
        ast['blocks'].insert(0, dummy)
    if 'title' not in ast['meta']:
        ast['meta']['title'] = elt('MetaInlines', 1)(([Str('Untitled document')]))
    sections = []
    for i, b in enumerate(ast['blocks']):
        if b['t'] == 'Header':
            l = b['c'][0]
            t = stringify(b['c'][2])
            sections += [{'level': l, 'title': t, 'start': i}]
    if not sections:
        log('INFO', 'No sections!')
        write_ast(ast)
        return
    for i, s in enumerate(sections[:-1]):
        s['end'] = sections[i+1]['start']
    sections[-1]['end'] = len(ast['blocks'])
    for s in sections:
        words = stringify2(ast['blocks'][s['start']:s['end']])
        words = depunctuate(words)
        s['words'] = len(words.split())
    for i, s in enumerate(sections[:-1]):
        enclosed_words = 0
        for t in sections[i+1:]:
            if t['level'] <= s['level']:
                break
            else:
                enclosed_words += t['words']
        if enclosed_words > 0:
            s['enclosed_words'] = enclosed_words + s['words']
    for s in sections:
        log('INFO', str(s))
    max_cols = max([s['level'] for s in sections]) + 2
    max_rows = len(sections)
    total_words = sum([s['words'] for s in sections])
    ast['blocks'] = []
    ast['blocks'] += [make_para('Word count: ' + '{0:,}'.format(total_words))]
    # breadcrumbs table
    ast['blocks'] += [Header(1, ["histogram", [], []], [Str('Histogram')])]
    table = init_table(max_rows, 4)
    # headings for each column
    headings = dict()
    headings[0] = ' '
    headings[1] = ' '
    headings[2] = '#'
    headings[3] = '%'
    for i in range(0, max_rows):
        table[i][0] = sections[i]['title']
        table[i][1] = '=' * int(sections[i]['words'] / total_words * 100.0)
        table[i][2] = '{0:,}'.format(sections[i]['words'])
        table[i][3] = '%3d%%' % (sections[i]['words'] / total_words * 100.0)
    log('INFO', str(table))
    ast['blocks'] += [make_table(headings, table)]
    ast['blocks'] += [Header(1, ["cumulative-words", [], []], [Str('Cumulative words')])]
    # word count table
    table = init_table(max_rows, max_cols)
    # headings for each column
    headings = dict()
    for j in range(0, max_cols-1):
        headings[j] = '#' * j
    headings[max_cols-1] = 'Cumulative'
    # word count table
    cumulative = 0
    for i in range(0, max_rows):
        col = sections[i]['level']
        table[i][0] = sections[i]['title']
        if 'enclosed_words' in sections[i]:
            table[i][col] = '{0:,}'.format(sections[i]['enclosed_words'])
            table[i][col+1] = '{0:,}'.format(sections[i]['words'])
        else:
            table[i][col] = '{0:,}'.format(sections[i]['words'])
        cumulative += sections[i]['words']
        table[i][max_cols-1] = '{0:,}'.format(cumulative)
    # prepare ast element
    ast['blocks'] += [make_table(headings, table)]
    ast['blocks'] += [Header(1, ["cumulative-percentage", [], []], [Str('Cumulative percentage')])]
    # percentage table
    cumulative = 0
    for i in range(0, max_rows):
        col = sections[i]['level']
        if 'enclosed_words' in sections[i]:
            table[i][col] = '%3d%%' % (sections[i]['enclosed_words'] / total_words * 100.0)
            table[i][col+1] = '%3d%%' % (sections[i]['words'] / total_words * 100.0)
        else:
            table[i][col] = '%3d%%' % (sections[i]['words'] / total_words * 100.0)
        cumulative += sections[i]['words']
        table[i][max_cols-1] = '%3d%%' % (cumulative / total_words * 100.0)
    ast['blocks'] += [make_table(headings, table)]
    write_ast(ast)

def init_table(max_rows, max_cols):
    table = dict()
    for i in range(0, max_rows):
        table[i] = dict()
        for j in range(0, max_cols):
            table[i][j] = ' '
    return table

def make_table(headings, table):
    max_cols = len(table[0])
    max_rows = len(table)
    cells = [[[Plain([Str(table[i][j])])] for j in range(0, max_cols)] for i in range(0, max_rows)]
    tops = [[Plain([Str(headings[j])])] for j in range(0, max_cols)]
    return Table([],
                 [elt('AlignLeft', 0)()] + ([elt('AlignRight', 0)()] * (max_cols-1)),
                 [0] * max_cols,
                 [tops[j] for j in range(0, max_cols)],
                 [
                     [cells[i][j] for j in range(0, max_cols)] for i in range(0, max_rows)
                 ])

def make_para(string):
    return Para([Str(string)])

def depunctuate(s):
    s = re.sub('[:,;–.\[\]]', '', s)
    s = s.replace(u"\u00A0", " ")
    s = s.replace('/', ' ')
    return s

def read_ast():
    log('DEBUG', 'reading ast')
    return json.load(sys.stdin)

def write_ast(ast):
    log('DEBUG', 'writing ast')
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

def log(level, msg):
    import os
    import sys
    if 'PANZER_SHARED' in os.environ:
        sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
        import panzertools
        panzertools.log(level, msg)
    else:
        pass
        # print(level + ': ' + msg, file=sys.stderr)

def stringify2(x):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val, format, meta):
        if key in ['Str', 'MetaString']:
            result.append(val)
        elif key == 'Code':
            result.append(val[1])
        elif key == 'Math':
            result.append(val[1])
        elif key == 'LineBreak':
            result.append(" ")
        elif key == 'SoftBreak':
            result.append(" ")
        elif key == 'Space':
            result.append(" ")

    walk(x, go, "", {})
    return ' '.join(result)

if __name__ == '__main__':
    main()

