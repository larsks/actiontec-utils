#!/usr/bin/python

import os
import sys
import argparse
import logging

import actiontec.fwparser as fwparser
import actiontec.confparser as confparser

def get_active_policy(fwcfg):
    active_name = fwcfg.lookup('fw/policy/active')
    active_policy = find(fwcfg.lookup('fw/policy'), 'name', active_name)
    return active_policy[1]

def handle_show(at, cfg, opts):
    logging.info('showing firewall configuraiton')

    p = confparser.Parser()
    res,out = at.run('conf print net_obj')
    net_obj = p.parse(out)

    for dir in [ 'in', 'out' ]:
        obj_name = '%s_%s' % (
                cfg.get('blacklist', 'blacklist'),
                dir
                )
        res = net_obj.find('description', obj_name)
        if res:
            k, obj = res
            print '%s:' % obj_name
            for k,v in obj['item'].items():
                print v['ip'], v['netmask']

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

    apply_parser = fwsub.add_parser('apply')
    apply_parser.add_argument('rules')
    apply_parser.set_defaults(handler=handle_apply)

    show_parser = fwsub.add_parser('show')
    show_parser.set_defaults(handler=handle_show)

