"""Keep reviewed HK allocation out of ChinaMax while preserving adjacent coverage."""
import ipaddress
from manage import ROOT, active, rule

nets=[ipaddress.ip_network(v) for k,v in map(rule,active((ROOT/'rules/ChinaMax.list').read_text())) if k=='ip-cidr']
excluded=ipaddress.ip_network('43.92.128.0/17')
assert not any(n.overlaps(excluded) for n in nets)
block=ipaddress.ip_network('43.0.0.0/9')
actual=list(ipaddress.collapse_addresses(n for n in nets if n.subnet_of(block)))
expected=list(ipaddress.collapse_addresses(block.address_exclude(excluded)))
assert actual==expected
print('PASS: HK /17 excluded; remaining 43.0.0.0/9 coverage exact')
