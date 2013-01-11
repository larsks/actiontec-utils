#!/usr/bin/python

import os
import sys
import re

# block (in|out) on <interface> [!] from (<ip>|any) [!] to (<ip>|any) [ (reject|drop) ] [log]
re_fw_cmd = re.compile('''
        (?P<type>(block|pass)) \s+ (?P<dir>(in|out)) \s+
        ((?P<neg_src>!) \s+)?
        from \s+ (?P<src>\S+) \s+
        ((?P<neg_dst>!) \s+)?
        to \s+ (?P<dst>\S+)
        (\s+ (?P<action>(reject|drop)))?
        (\s+ (?P<log>log))?
        ''', re.VERBOSE)

'''
        '''

def parse(rulefile, pid=0, chain='at_firewall_%s'):
    pid = int(pid)

    rules = []
    for line in rulefile:
        if not line.strip():
            continue
        if line.startswith('#'):
            continue

        mo = re_fw_cmd.match(line)
        if not mo:
            print >>sys.stderr, 'ERROR: unable to parse:', line
            sys.exit(1)

        rules.append(mo.groupdict())

    for dir in [ 'in', 'out' ]:
        yield('conf del fw/policy/%d/chain/%s/rule' % (pid, chain % dir))

    for i, rule in enumerate(rules):
        if rule['type'] == 'pass':
            rule['action'] = 'accept_packet'

        chain_name='fw_%(iface)s_%(dir)s' % rule
        yield('conf set fw/policy/%d/chain/%s/rule/%d/enabled 1' % (
            pid, chain_name, i))
        yield('conf set fw/policy/%d/chain/%s/rule/%d/action/type %s' % (
                pid, chain_name, i, rule['action']))
        yield('conf set fw/policy/%d/chain/%s/rule/%d/action/log %d' % (
                pid, chain_name, i, 1 if rule['log'] else 0))

        yield('conf set fw/policy/%d/chain/%s/rule/%d/match/src_is_exclude %d' % (
                pid, chain_name, i, 1 if rule['neg_src'] else 0))
        yield('conf set fw/policy/%d/chain/%s/rule/%d/match/dst_is_exclude %d' % (
                pid, chain_name, i, 1 if rule['neg_dst'] else 0))

        if rule['src'] != 'any':
            yield('conf set fw/policy/%d/chain/%s/rule/%d/match/src/0/item/0/ip %s' % (
                    pid, chain_name, i,
                    rule['src'] if rule['src'] != 'any' else '0.0.0.0'))
        if rule['dst'] != 'any':
            yield('conf set fw/policy/%d/chain/%s/rule/%d/match/dst/0/item/0/ip %s' % (
                pid, chain_name, i,
                rule['dst'] if rule['dst'] != 'any' else '0.0.0.0'))

