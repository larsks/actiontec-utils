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

