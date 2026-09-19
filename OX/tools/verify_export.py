#!/usr/bin/env python3
import argparse
from pathlib import Path
from manage import ROOT, SERVICES, active, sections
p=argparse.ArgumentParser(); p.add_argument('--current',type=Path,required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args()
source=sections(a.current.read_text())
remote_path=a.out/'OX-个人版-远程规则.conf'
if not remote_path.exists(): remote_path=a.out/'OX-个人版-远程规则-待公开托管.conf.template'
remote=sections(remote_path.read_text())
local=sections((a.out/'OX-个人版-内置规则.conf').read_text())
assert source['[dns]']==remote['[dns]']==local['[dns]']
assert source['[server_remote]'][0].split(',')[0]==remote['[server_remote]'][0].split(',')[0]
assert local['[server_remote]']==remote['[server_remote]']
assert remote['[policy]']==local['[policy]']
assert len(remote['[filter_remote]'])==len(SERVICES)+1
assert not local['[filter_remote]']
want=active((ROOT/'rules/Priority.list').read_text())
for name,policy,_ in SERVICES:
 for l in active((ROOT/f'rules/{name}.list').read_text()):
  parts=[s.strip() for s in l.split(',')]; parts[2]='direct' if name=='Lan' else policy
  want.append(', '.join(parts))
assert local['[filter_local]']==want+['final, 兜底策略']
assert all('enabled=false' in l for l in remote['[rewrite_remote]'])
assert not any(l.startswith(('p12','passphrase')) for l in remote['[mitm]'])
print(f'PASS: exported DNS and subscription preserved, rules equivalent ({len(want)} including priority exceptions), modules disabled, no copied certificate. Values not logged.')
