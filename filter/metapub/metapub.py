#!/usr/bin/env python3
"""
Injects info into metadata from separate publications yaml file:

---
metapub: 52B5C198-A66C-4F0D-8F97-35F01C30DF4A
metapub_file: "/Users/msprevak/Documents/CV/publications.yaml"
...

-- to -->

---
title: Realism and instrumentalism
date: 20 December 2009
author:
- affiliation: University of Edinburgh
  email: 'mark.sprevak@ed.ac.uk'
  name: Mark Sprevak
  name_first: Mark
  name_last: Sprevak
doi: '10.4135/9781452257044'
published: |
    Published in H. Pashler (Ed.) *The Encyclopedia of the Mind* (2013),
    Thousand Oaks, CA: SAGE Publications, pp. 633–636
metapub: '52B5C198-A66C-4F0D-8F97-35F01C30DF4A'
metapub_file: '/Users/msprevak/Documents/CV/publications.yaml'
...

"""

import json
import sys
import yaml
from pandocfilters import stringify
from util import there

ENCODING = 'utf-8'

def main():
    """docstring for main"""
    # read input ast
    ast = read_ast()
    meta = ast[0]['unMeta']
    if 'metapub' not in meta:
        write_ast(ast)
        return
    # read metapub_file
    if 'metapub_file' not in meta:
        log('ERROR', 'No "metapub_file" metadata field in input document')
        write_ast(ast)
        return
    metapub_file = stringify(meta['metapub_file'])
    log('DEBUG', 'reading from: ' + metapub_file)
    pubs = read_yaml(metapub_file)
    # find entry in metapub_file
    ident = stringify(meta['metapub'])
    log('DEBUG', 'looking for: ' + ident)
    entries = [e for e in pubs
               if ('uuid' in e and e['uuid'] == ident) \
               or ('slug' in e and e['slug'] == ident)]
    if not entries:
        log('ERROR', 'Publication with id "%s" not found in "%s"' % (ident, metapub_file))
        write_ast(ast)
        return
    if len(entries) > 1:
        log('WARNING', 'More than 1 publication with id "%s" found in "%s"' % (ident, metapub_file))
    entry = entries[0]
    # build new metadata from entry
    new = dict()
    add_title(new, entry)
    add_author(new, entry)
    add_date_updated(new, entry)
    add_disclaimer(new, entry)
    add_publication(new, entry)
    add_abstract(new, entry)
    add_keywords(new, entry)
    add_note(new, entry)
    # convert new metadata to pandoc's ast metadata format
    log('DEBUG', 'new metadata: ' + str(new))
    incoming = generate_meta(new)
    # update using new metadata
    meta.update(incoming)
    # write output ast
    ast[0]['unMeta'] = meta
    write_ast(ast)

def add_title(new, entry):
    if there('title', entry):
        new['title'] = entry['title']

def add_author(new, entry):
    if there('author', entry):
        new['author'] = entry['author']
    for a in new['author']:
        a['name'] = a.get('name_first', '') + ' ' + a.get('name_last', '')

def add_date_updated(new, entry):
    if there('date_updated', entry):
        new['date'] = uk_date(entry['date_updated'])

def add_disclaimer(new, entry):
    if there('disclaimer', entry):
        new['disclaimer'] = entry['disclaimer']
    elif there('status', entry) and entry['status'] in ['proposed', 'in preparation']:
        new['disclaimer'] = '*Rough draft only. Please do not cite without permission.*'

def add_publication(new, entry):
    def add_published(new, entry):
        import formatter
        f = getattr(formatter, entry['published']['type'], formatter.default)
        new['published'] = f(entry)
    def add_doi(new, entry):
        if there('doi', entry['published']):
            new['doi'] = entry['published']['doi']
    if there('published', entry):
        add_disclaimer(new, entry)
        add_published(new, entry)
        add_doi(new, entry)

def add_abstract(new, entry):
    if there('abstract', entry):
        new['abstract'] = entry['abstract']

def add_note(new, entry):
    if there('note', entry):
        new['note'] = entry['note']

def add_keywords(new, entry):
    if there('keywords', entry):
        new['keywords'] = entry['keywords']

def read_ast():
    log('DEBUG', 'reading ast')
    return json.load(sys.stdin)

def write_ast(ast):
    log('DEBUG', 'writing ast')
    sys.stdout.write(json.dumps(ast))
    sys.stdout.flush()

def read_yaml(filename):
    with open(filename, 'r', encoding=ENCODING) as f:
        return yaml.load(f)

def generate_meta(incoming_dict):
    import pandoc
    yaml_str = yaml.dump(incoming_dict)
    yaml_str_appended = '---\n' + yaml_str + '...\n\n'
    json_str = pandoc.text2json(yaml_str_appended, 'markdown', ['--smart', '--standalone'])
    return json_str[0]['unMeta']

def log(level, msg):
    import os
    import sys
    if 'PANZER_SHARED' in os.environ:
        sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
        import panzertools
        panzertools.log(level, msg)
    else:
        print(level + ': ' + msg, file=sys.stderr)

def uk_date(iso_date):
    """
    return 4 March 2015 from 2015-03-04
    """
    import datetime
    d = datetime.datetime.strptime(str(iso_date), "%Y-%m-%d")
    return d.strftime('%-d %B %Y')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

