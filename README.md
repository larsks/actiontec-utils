# ActionTec Utilities

This is collection of tools for interacting with your ActionTec
MI424WR (Verizon FIOS) modem via the command line.

**NOTE**: Only the `conf` subcommand is fully implemented at this
time.

## Configuration

The `actiontec` command needs a configuration file to provide
authentication credentials for your router.  The file is a [YAML][]
file that should look something like this:

    actiontec:
      username: admin
      password: secret

You can specify the location of this file using the `--config` (`-f`)
command line option:

    actiontec -f router.conf ...

Or by setting the `ACTIONTEC_CONFIG` environment variable:

    export ACTIONTEC_CONFIG=$HOME/.actiontec
    actiontec ...

[yaml]: http://www.yaml.org/

## Commands

### Configuration commands

The `conf` command provides the following subcommands:

- conf show [ --keys-only ] [ --prefix <prefix> ] <path> [ <path> ... ]
- conf del [ --prefix <prefix> ] <path> [ <path> ... ]
- conf set [ --prefix <prefix> ] <path> <value> [ <path> <value> ... ]
- conf commit

#### Examples

Show the name of the active firewall policy:

    $ actiontec -q conf show fw/policy/active
    default

Show the access control blacklist:

    actiontec -q conf show fw/policy/0/chain/access_ctrl_block
    {'access_ctrl_block': {'description': 'Access Control - Block',
                           'output': '0',
                           'rule': {},
                           'type': '4'}}

Create a new routing entry:

    $ actiontec -q conf set --prefix route/static/0 \
      addr 192.168.100.0 \
      netmask 255.255.255.0 \
      dev br0 \
      gateway 192.168.1.21 \
      metric 0

Show static routes:

    $ actiontec -q conf show route/static
    {'static': {'0': {'addr': '192.168.100.0',
                      'dev': 'br0',
                      'gateway': '192.168.1.21',
                      'metric': '0',
                      'netmask': '255.255.255.0'}}}

Get information about DHCP leases:

    $ actiontec -q conf show dev/br0/dhcps/lease -k |
      xargs -iID actiontec -q conf show dev/br0/dhcps/lease/ID/hardware_mac
    22:53:10:a3:d5:32
    14:01:d2:5d:2f:03
    88:b3:e5:1a:00:36

### Firewall commands

- fw enable
- fw disable
- fw apply <rules>
- fw list
- fw clear
- fw block ( --out | --in ) <ip>
- fw unblock ( --out | --in ) <ip>

### DNS commands

- dns add <host> <addr>
- dns del <host>

### DHCP server commands

- dhcp show [ ( --host <host> | --mac <mac> | --ip <ip> ) ]
- dhcp del ( --host <host> | --mac <mac> | --ip <ip> )
- dhcp set ( --host <host> | --mac <mac> | --ip <ip> ) <attr> <val>

### Routing commands

- route show
- route add <dest> <mask> <gw> [ <metric> ]
- route del <dest> <mask> <gw>

