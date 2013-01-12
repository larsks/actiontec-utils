#!/usr/bin/python

import os
import sys
import argparse
import logging
import pprint

import actiontec.confparser as confparser

def handle_show(at, cfg, opts):
    if opts.prefix and not opts.prefix.endswith('/'):
        opts.prefix = opts.prefix + '/'

    parser = confparser.Parser()

    for path in opts.path:
        path = '%s%s' % (opts.prefix, path)

        res, out = at.run('conf print %s' % path)
        if res != 0:
            logging.error('unable to show %s', path)
            continue

        fwcfg = parser.parse(out)
        if not fwcfg:
            logging.warn('no value for %s', path)
            continue

        if len(fwcfg) == 1 and not isinstance(fwcfg.values()[0], dict):
            print fwcfg.values()[0]
        elif opts.keys_only:
            print '\n'.join(fwcfg[path.split('/')[-1]].keys())
        else:
            print '\n'.join(['%s %s' % (k,v) for k,v in fwcfg.flatten()])

def handle_set(at, cfg, opts):
    if opts.prefix and not opts.prefix.endswith('/'):
        opts.prefix = opts.prefix + '/'

    i = iter(opts.nvpairs)
    for path, value in zip(i,i):
        path = '%s%s' % (opts.prefix, path)
        logging.info('set %s = %s', path, value)
        res, out = at.run('conf set %s "%s"' % (path, value))
        if res != 0:
            logging.error('unable to set %s = %s', path, value)
            continue

def handle_del(at, cfg, opts):
    if opts.prefix and not opts.prefix.endswith('/'):
        opts.prefix = opts.prefix + '/'

    for path in opts.path:
        path = '%s%s' % (opts.prefix, path)
        logging.info('deleting %s', path)

        res, out = at.run('conf del %s' % path)
        if res != 0:
            logging.error('unable to delete %s', path)
            continue

def handle_commit(at, cfg, opts):
    res, out = at.run('conf reconf 1')
    print out
    return res

def add_parser(parent):
    parser = parent.add_parser('conf')
    sub = parser.add_subparsers()

    show_parser = sub.add_parser('show')
    show_parser.add_argument('--keys-only', '-k', action='store_true')
    show_parser.add_argument('--prefix', '-p', default='')
    show_parser.add_argument('path', nargs='+')
    show_parser.set_defaults(handler=handle_show)

    set_parser = sub.add_parser('set')
    set_parser.add_argument('--prefix', '-p', default='')
    set_parser.add_argument('nvpairs', nargs='+')
    set_parser.set_defaults(handler=handle_set)

    del_parser = sub.add_parser('del')
    del_parser.add_argument('path', nargs='+')
    del_parser.add_argument('--prefix', '-p', default='')
    del_parser.set_defaults(handler=handle_del)

    commit_parser = sub.add_parser('commit')
    commit_parser.set_defaults(handler=handle_commit)

