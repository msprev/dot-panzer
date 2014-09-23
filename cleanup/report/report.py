#!/usr/bin/env python3

import sys
import json

def main():
    """docstring for main"""
    stdin_bytes = sys.stdin.buffer.read()
    stdin = stdin_bytes.decode('utf8')
    message_in = json.loads(stdin)
    output = json.dumps(message_in, sort_keys=True, indent=2)
    with open('report.json', 'w', encoding='utf8') as output_file:
        output_file.write(output)
        output_file.flush()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

