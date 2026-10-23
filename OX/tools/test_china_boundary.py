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

for cidr in ('189.24.118.0/23','189.24.121.0/24'):
    assert not any(n.overlaps(ipaddress.ip_network(cidr)) for n in nets)
block6=ipaddress.ip_network('240b:4006:1100::/44')
nets6=[ipaddress.ip_network(v) for k,v in map(rule,active((ROOT/'rules/ChinaMax.list').read_text())) if k=='ip6-cidr']
actual6=list(ipaddress.collapse_addresses(n for n in nets6 if n.overlaps(block6)))
expected6=list(ipaddress.collapse_addresses(map(ipaddress.ip_network,('240b:4006:1104::/46','240b:4006:110c::/46'))))
assert actual6==expected6
assert not {'capcutapi.com','capcutapi.us','capcutstatic.com'} & {v for k,v in map(rule,active((ROOT/'rules/TikTok.list').read_text()))}
print('PASS: DE IPv4 additions excluded; SG IPv6 prior coverage retained; CapCut not owned by TikTok')
