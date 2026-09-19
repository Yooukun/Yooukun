#!/usr/bin/env python3
"""Check public tree against actual secrets from user configs without printing them."""
import argparse
from urllib.parse import urlparse, parse_qs
from manage import ROOT, sections
p=argparse.ArgumentParser(); p.add_argument('configs',nargs='+'); a=p.parse_args()
secrets=set()
for file in a.configs:
 from pathlib import Path
 data=sections(Path(file).read_text())
 for line in data.get('[server_remote]',[]):
  url=line.split(',')[0].strip()
  if url.startswith('https://'):
   secrets.add(url)
   for values in parse_qs(urlparse(url).query).values():
    for v in values:
     if len(v)>16: secrets.add(v)
 for line in data.get('[mitm]',[]):
  k,_,v=line.partition('=')
  if k.strip() in ('passphrase','p12') and v.strip(): secrets.add(v.strip())
 for line in data.get('[dns]',[]):
  if line.startswith(('alias','doh-server')):
   secrets.add(line.split('=',1)[1].strip())
checked=0
for file in ROOT.rglob('*'):
 if not file.is_file() or any(x in file.relative_to(ROOT).parts for x in ('.git','__pycache__','private','candidate')): continue
 try: text=file.read_text()
 except UnicodeDecodeError: continue
 assert not any(secret in text for secret in secrets), 'Private value detected in '+str(file.relative_to(ROOT))
 checked+=1
print(f'PASS: {checked} public text files checked against private configuration values. No values printed.')
