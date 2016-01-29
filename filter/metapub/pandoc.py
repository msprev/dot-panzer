######################################
#  programmatic interface to pandoc  #
######################################

import json
import subprocess

ENCODING = 'utf-8'

class Pandoc(object):

    def __init__(self, args=list()):
        self.args = args
        self.stdin = str()
        self.stdout = str()
        self.stderr = str()

    def pandoc(self):
        cmd = ['pandoc']
        cmd.extend(self.args)
        process = subprocess.Popen(cmd,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        stdin_bytes = self.stdin.encode(ENCODING)
        stdout_bytes, stderr_bytes = process.communicate(input=stdin_bytes)
        self.stdout = stdout_bytes.decode(ENCODING)
        self.stderr = stderr_bytes.decode(ENCODING)

def text2json(text, text_format, args=None):
    pandoc_args = ['-', '-f', text_format, '-t', 'json']
    if args:
        pandoc_args.extend(args)
    p = Pandoc(pandoc_args)
    p.stdin = text
    p.pandoc()
    json_doc = json.loads(p.stdout)
    return json_doc
