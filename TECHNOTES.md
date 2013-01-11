## Top-level configuration keys

These are possible OpenRG top level configuration keys (suitable for
passing to the `actiontec show ...` command).  Many of these keys may
not exist on the Verizon router, and some (such as `net_obj`) only
exist if they contain something.

Commonly used:

- dev
- fw
- route
- net_obj
- dns
- qos

Less commonly used:

- admin
- wbm
- syslog
- service
- interception
- proxy
- mcast
- reset_history
- rmt_upd
- voip
- enotify
- email
- watchdog
- radius
- cwmp
- cert
- upnp
- storage_service
- pppoe_relay
- system
- fs
- manufacturer
- internal

## Filtering on network objects

    {'fw_clink1_out': {'description': {},
                       'dev': 'clink1',
                       'output': '1',
                       'rule': {'0': {'action': {'log': '0', 'type': 'drop'},
                                      'enabled': '1',
                                      'match': {'dscp': {'mask': '63',
                                                         'value': '-1'},
                                                'dscp_is_exclude': '0',
                                                'dst': {'0': {'net_obj': '0'}},
                                                'dst_is_exclude': '0',
                                                'length': {'from': '-1',
                                                           'to': '-1'},
                                                'priority': '-1',
                                                'priority_is_exclude': '0',
                                                'services': {},
                                                'services_is_exclude': '0',
                                                'src': {'0': {'description': 'sandbox',
                                                              'item': {'0': {'ip': '192.168.1.8'}}}},
                                                'src_is_exclude': '0'},
                                      'rule_permanent_id': '0'}},
                       'type': '2'}}

