#!/usr/bin/python

import os
import sys
import argparse
import logging

import fwparser

def handle_clear(at, cfg, opts):
    logging.info('clearing clink1 firewall rules')
    res, out = at.run('conf del fw/policy/%d/chain/fw_clink1_out/rule' % (
        opts.policy))
    res, out = at.run('conf del fw/policy/%d/chain/fw_clink1_in/rule' % (
        opts.policy))

def handle_list(at, cfg, opts):
    logging.info('listing firewall configuraiton')
    res, out = at.run('conf print fw/policy/%d/chain' % opts.policy)
    print out
    return res

def handle_apply(at, cfg, opts):
    logging.info('populating firewall rules')
    with open(opts.rules) as fd:
        for line in fwparser.parse(fd, opts.policy):
            res, out = at.run(line)
            if res != 0:
                print >>sys.stderr, 'failed to create firewall rule:', line
                print >>sys.stderr, out

    if not opts.nocommit:
        logging.info('activating firewall rules')
        res, out = at.run('conf reconf 1')
        if res != 0:
            print >>sys.stderr, 'failed to commit firewall rules'
            print >>sys.stderr, out

def add_parser(sub):
    parser_fw = sub.add_parser('fw')
    parser_fw.add_argument('--policy', '-p', default=0, type=int)
    parser_fw.add_argument('--nocommit', '-n', action='store_true')

    fwsub = parser_fw.add_subparsers()
    clear_parser = fwsub.add_parser('clear')
    clear_parser.set_defaults(handler=handle_clear)

    apply_parser = fwsub.add_parser('apply')
    apply_parser.add_argument('rules')
    apply_parser.set_defaults(handler=handle_apply)

    list_parser = fwsub.add_parser('list')
    list_parser.set_defaults(handler=handle_list)

