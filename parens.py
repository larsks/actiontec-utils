#!/usr/bin/python

import os
import sys
import argparse

def dictify(data):
    '''Convert the tree structure produced by the OpenRG
    `conf print` command into a Python dictionary.'''

    try:
        k, v = data[0], data[1:]
    except IndexError:
        return {}

    if len(v) == 0:
        return {k: {}}
    elif len(v) == 1 and len(v[0]) == 1:
        return {k: v[0][0]}
    else:
        new = {}
        for datum in v:
            new.update(dictify(datum))
        return {k: new}

def lookup(d, path):
    '''Given a nested dictionary (such as that returned by dictify(),
    above) and a path in the form 'key/key/key', return the value of
    d[key][key][key].  For examaple:
        
        >>> parens.lookup(p.asdict(), 'fw/policy/0/chain/access_ctrl_block')
        {'output': '0', 'type': '4',
        'description': 'Access Control - Block',
        'rule': {}}
    '''

    path = path.split('/')
    if len(path) == 1:
        return d[path[0]]
    else:
        return lookup(d[path[0]], '/'.join(path[1:]))

class Parser(object):
    '''Parses the parenthesized tree returned by the OpenRG
    `conf print` command.  After parsing, the `data` attribute will 
    contain a Python list equivalent to the original data and the
    `asdict()` method will return the configuration as a dictionary.'''

    def reset(self):
        self.acc = []
        self.data = []
        self.stack = []
        self.cur = self.data

    def accumulate(self, c):
        self.acc.append(c)

    def token(self):
        t = ''.join(self.acc).strip()
        self.acc = []
        return t

    def handle_open_paren(self):
        tok = self.token()
        if tok:
            self.cur.append(tok)

        self.stack.append(self.cur)
        self.cur.append([])
        self.cur = self.cur[-1]

    def handle_close_paren(self):
        tok = self.token()
        if tok:
            self.cur.append(tok)
        if self.stack:
            self.cur = self.stack.pop()

    def parse(self, data):
        self.reset()
        
        last_was_space = False

        for c in data:
            if not c.isspace():
                last_was_space = False

            if c == '(':
                self.handle_open_paren()
            elif c == ')':
                self.handle_close_paren()
            else:
                if not c.isspace() or not last_was_space:
                    self.accumulate(c)

    def asdict(self):
        return dictify(self.data[0])

def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()

def main():
    opts = parse_args()

    # Read in the configuration.
    data = sys.stdin.read()

    # Get a parser object.
    p = Parser()

    # Parse the data.
    p.parse(data)

    # At this point, p.data has the verbatim tree structure
    # and p.asdict() will return the structure converted to
    # a dictionary.
    import pprint
    pprint.pprint(p.asdict())

if __name__ == '__main__':
    main()

