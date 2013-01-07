#!/usr/bin/python

import os
import sys
import argparse
import pprint

def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()

class Parser(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {}
        self.stack = []
        self.acc = []
        self.prev = []
        self.cur = self.stack

    def accumulate(self, x):
        self.acc.append(x)

    def acc_value(self):
        val = ''.join(self.acc).strip()
        self.acc = []
        return val

    def handle_open_paren(self):
        v = self.acc_value()
        if v:
            self.cur.append(v)
        newlist = []
        self.cur.append(newlist)
        self.prev.append(self.cur)
        self.cur = newlist

    def handle_close_paren(self):
        v = self.acc_value()
        if v:
            self.cur.append(v)

        self.cur = self.prev.pop()

    def parse(self,data):
        self.reset()

        last_was_space=False

        for c in data:
            if not c.isspace():
                last_was_space = False

            if c == '(':
                self.handle_open_paren()
            elif c == ')':
                self.handle_close_paren()
            elif c.isspace():
                if not last_was_space:
                    self.accumulate(c)
                last_was_space = True
            else:
                self.accumulate(c)

def dictify (data):
    print len(data), data

    for datum in data:
        try:
            k,v = datum
            print 'k',k,'v',v
            vv = dictify(v)
            return {k: vv}
        except ValueError:
            return datum[0]

def main():
    opts = parse_args()

    p = Parser()
    p.parse(sys.stdin.read())
    pprint.pprint(p.stack)
    pprint.pprint( dictify(p.stack))

if __name__ == '__main__':
    main()


