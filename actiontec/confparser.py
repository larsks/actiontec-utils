#!/usr/bin/python

import os
import sys
import argparse

def lookup(d, path):
    path = path.split('/')
    if len(path) == 1:
        v = d[path[0]]
        if isinstance(v, dict):
            return FirewallConfig(v)
        else:
            return v
    else:
        return lookup(d[path[0]], '/'.join(path[1:]))

def flatten(d, prefix=''):
    paths = []

    for k,v in d.items():
        if isinstance(v, dict):
            paths.extend(flatten(v, prefix='%s/%s' % (prefix, k)))
        else:
            paths.append(('%s/%s' % (prefix,k), v))

    return paths

class FirewallConfig (dict):
    def lookup(self, path):
        return lookup(self, path)

    def flatten(self):
        return flatten(self)

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

        if self.data:
            return FirewallConfig(dictify(self.data[0]))

