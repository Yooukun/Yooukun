#!/usr/bin/env python3
"""Icon presence, generation and non-icon preservation regressions."""
import re
from manage import ROOT, profile, sections
from policy_icons import ICONS, merge

source=(ROOT/'profiles/quantumultx.conf').read_text()
assert profile()==source, 'Generated template differs from published template'
assert len(ICONS)==42
policies=sections(source)['[policy]']
assert len(policies)==len(ICONS)
for line in policies:
    name=line.split('=',1)[1].split(',',1)[0].strip()
    assert line.count('img-url=')==1
    assert line.endswith(', img-url='+ICONS[name])
bare=re.sub(r',\s*img-url=[^,\r\n]+','',source)
assert merge(bare)==source
assert merge(source)==source
assert sections(bare)['[filter_remote]']==sections(source)['[filter_remote]']
print('PASS: 42 icon mappings, exact generation, icon-only merge, idempotency.')
