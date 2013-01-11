#!/usr/bin/python

import os
import sys
import logging
import re
from telnetlib import Telnet

class ActionTec (object):
    def __init__(self, ip, username, password,
            timeout=10):
        self.ip = ip
        self.username = username
        self.password = password
        self.channel = None
        self.timeout = timeout

        self.setup_logging()

    def setup_logging(self):
        self.log = logging.getLogger('actiontec')

    def connect(self):
        ch = Telnet(self.ip, timeout=self.timeout)
        ch.read_until('Username:')
        ch.write('%s\n' % self.username)
        ch.read_until('Password:')
        ch.write('%s\n' % self.password)
        ch.read_until('Router>')

        self.channel = ch

    def run(self, cmd):
        ch = self.channel
        res = 0

        self.log.debug('sending: %s', cmd)

        ch.write('%s\n' % cmd)
        ch.read_until('\r\n')

        i, mo, out = ch.expect([
            'Returned (?P<res>[-\d+]+)',
            'Router>',
            ])

        if i == 0:
            ch.read_until('Router>')
            res = int(mo.group('res'))

        return res, out[:-8].strip()

