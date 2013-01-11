#!/usr/bin/python

import os
import sys
import argparse
import logging
import yaml

from connection import ActionTec
from cmd import cmd_fw
from cmd import cmd_exec

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--debug', action='store_const',
            const=logging.DEBUG,
            dest='loglevel')
    p.add_argument('--password', '-p')
    p.add_argument('--username', '-u', default='admin')
    p.add_argument('--ip', '-i', default='192.168.1.1')
    p.add_argument('--timeout', '-t', default=10, type=int)
    p.add_argument('--config', '-f')

    sub = p.add_subparsers()

    cmd_fw.add_parser(sub)
    cmd_exec.add_parser(sub)

    p.set_defaults(loglevel=logging.INFO)

    return p.parse_args()

def main():
    opts = parse_args()

    logging.basicConfig(
            level=opts.loglevel,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

    if opts.config:
        cfg = yaml.load(open(opts.config)).get('actiontec', {})
    else:
        cfg = {}

    if opts.username:
        cfg['username'] = opts.username
    if opts.password:
        cfg['password'] = opts.password
    if opts.ip:
        cfg['ip'] = opts.ip

    at = ActionTec(cfg['ip'], cfg['username'], cfg['password'],
            timeout=opts.timeout)
    at.connect()
    return opts.handler(at, cfg, opts)

if __name__ == '__main__':
    sys.exit(main())

