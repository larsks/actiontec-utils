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

fw/policy/0/chain/fw_clink1_out/output 1
fw/policy/0/chain/fw_clink1_out/rule/0/action/type drop
fw/policy/0/chain/fw_clink1_out/rule/0/action/log 0
fw/policy/0/chain/fw_clink1_out/rule/0/rule_permanent_id 0
fw/policy/0/chain/fw_clink1_out/rule/0/enabled 1
fw/policy/0/chain/fw_clink1_out/rule/0/match/dscp/mask 63
fw/policy/0/chain/fw_clink1_out/rule/0/match/dscp/value -1
fw/policy/0/chain/fw_clink1_out/rule/0/match/src_is_exclude 0
fw/policy/0/chain/fw_clink1_out/rule/0/match/src/0/item/0/ip 192.168.1.8
fw/policy/0/chain/fw_clink1_out/rule/0/match/src/0/description sandbox
fw/policy/0/chain/fw_clink1_out/rule/0/match/services_is_exclude 0
fw/policy/0/chain/fw_clink1_out/rule/0/match/dst_is_exclude 0
fw/policy/0/chain/fw_clink1_out/rule/0/match/dst/0/net_obj 0
fw/policy/0/chain/fw_clink1_out/rule/0/match/priority_is_exclude 0
fw/policy/0/chain/fw_clink1_out/rule/0/match/priority -1
fw/policy/0/chain/fw_clink1_out/rule/0/match/length/to -1
fw/policy/0/chain/fw_clink1_out/rule/0/match/length/from -1
fw/policy/0/chain/fw_clink1_out/rule/0/match/dscp_is_exclude 0
fw/policy/0/chain/fw_clink1_out/dev clink1
fw/policy/0/chain/fw_clink1_out/type 2

