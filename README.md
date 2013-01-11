## Configuration

- conf show <path>
- conf set <path>
- conf del <path>
- conf commit

## Firewall

- fw enable
- fw disable
- fw apply <rules>
- fw list
- fw clear
- fw block ( --out | --in ) <ip>
- fw unblock ( --out | --in ) <ip>

## DNS manipulation

- dns add <host> <addr>
- dns del <host>

## DHCP server

- dhcp show [ ( --host <host> | --mac <mac> | --ip <ip> ) ]
- dhcp del ( --host <host> | --mac <mac> | --ip <ip> )
- dhcp set ( --host <host> | --mac <mac> | --ip <ip> ) <attr> <val>

## Routing

- route show
- route add <dest> <mask> <gw> [ <metric> ]
- route del <dest> <mask> <gw>

