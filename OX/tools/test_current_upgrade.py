#!/usr/bin/env python3
"""Synthetic regression for private configuration migration; no real subscriptions."""
import re
from manage import profile, sections
from upgrade_current import transform

current=profile()
current=re.sub(r'^static = mono,.*\n','',current,flags=re.M)
current=current.replace(', mono, img-url=',', img-url=')
current=current.replace('static = Pornhub,','static = 成人站点,').replace('force-policy=Pornhub','force-policy=成人站点')
current=current.replace('[server_remote]\n','[server_remote]\nhttps://example.invalid/primary, tag=Kuromis, enabled=true\n')
before=sections(current)
after=sections(transform(current,'https://example.invalid/standby'))
assert len(after['[policy]'])==41
assert not any(re.match(r'^static = mono,',line) for line in after['[policy]'])
assert all('^(Kuromis|mono)$' in line for line in after['[policy]'] if 'resource-tag-regex=' in line)
assert after['[server_remote]'][0]==before['[server_remote]'][0]
assert after['[server_remote]'][-1].endswith('enabled=false')
assert 'tag=mono' in after['[server_remote]'][-1]
for section in ('[dns]','[mitm]','[rewrite_remote]','[rewrite_local]','[task_local]'):
    assert before[section]==after[section]
assert any(line.startswith('static = Pornhub,') for line in after['[policy]'])
print('PASS: synthetic migration, original subscription/settings preserved, disabled mono and Pornhub label.')
