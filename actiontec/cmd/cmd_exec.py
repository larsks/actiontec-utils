#!/usr/bin/python

import os
import sys
import argparse

def handle(at, cfg, opts):
    res, out = at.run(' '.join(opts.command))
    print out
    return int(res)
    
def add_parser(sub):
    parser_exec = sub.add_parser('exec')
    parser_exec.add_argument('command', nargs='+')
    parser_exec.set_defaults(handler=handle)

