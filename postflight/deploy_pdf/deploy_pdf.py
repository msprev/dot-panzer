#!/usr/bin/env python3
"""
deploy generated pdf file to homepage
"""

import json
import os
import shutil
import subprocess
import sys
import yaml
from pandocfilters import stringify

ENCODING = 'utf-8'


def main():
    """docstring for main"""
    message_in = read_message()
    # read input ast
    meta = message_in[0]['metadata']
    if 'metapub' not in meta:
        log('ERROR', 'No "metapub" metadata field in input document')
        return 1
    # read metapub_file
    if 'metapub_file' not in meta:
        log('ERROR', 'No "metapub_file" metadata field in input document')
        return 1
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
        return 1
    if len(entries) > 1:
        log('WARNING', 'More than 1 publication with id "%s" found in "%s"' % (ident, metapub_file))
    entry = entries[0]
    dest = str()
    try:
        dest = entry['deploy']['path']
    except KeyError:
        log('ERROR', '"path" field inside "deploy" field not found in metadata')
        return 1
    if not dest:
        log('WARNING', '"path" field inside "deploy" empty')
        return 1
    # copy the file
    source = message_in[0]['options']['pandoc']['output']
    if source == '-':
        log('ERROR', 'no output filename for panzer given')
        return 1
    source = os.path.splitext(source)[0]+'.pdf'
    log('INFO', 'source file: "%s"' % source)
    log('INFO', 'deploying to location "%s"' % dest)
    if not os.path.exists(source):
        log('ERROR', 'source file "%s" does not exist' % source)
        return 1
    shutil.copyfile(source, dest)
    if os.path.exists(dest):
        open_pdf(dest)
    return 0

def read_message():
    stdin_bytes = sys.stdin.buffer.read()
    stdin = stdin_bytes.decode(ENCODING)
    message_in = json.loads(stdin)
    return message_in

def read_yaml(filename):
    with open(filename, 'r', encoding=ENCODING) as f:
        return yaml.load(f)

def log(level, msg):
    import os
    import sys
    if 'PANZER_SHARED' in os.environ:
        sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
        import panzertools
        panzertools.log(level, msg)
    else:
        print(level + ': ' + msg, file=sys.stderr)

def open_pdf(filepath):
    """Use AppleScript to open View.app"""
    fullpath = os.path.abspath(filepath)
    command = """
    set theFile to POSIX file "%s" as alias
    set thePath to POSIX path of theFile
    tell application "Skim"
      activate
      set theDocs to get documents whose path is thePath
      try
        if (count of theDocs) > 0 then revert theDocs
      end try
      open theFile
    end tell
    """ % fullpath
    asrun(command)


def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."
    osa = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdin_bytes = ascript.encode(ENCODING)
    stdout_bytes = osa.communicate(stdin_bytes)[0]
    stdout = str()
    if stdout_bytes:
        stdout = stdout_bytes.decode(ENCODING)
    return stdout

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
