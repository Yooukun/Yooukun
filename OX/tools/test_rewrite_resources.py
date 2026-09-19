#!/usr/bin/env python3
"""Regression for native Quantumult X remote rewrite format (no section headers)."""
from pathlib import Path
import re
from manage import ROOT, BASE, active

def validate(text):
 lines=active(text)
 assert lines and not any(line.startswith('[') for line in lines), 'Remote rewrite must not contain section headers'
 hosts=[l for l in lines if l.startswith('hostname = ')]
 assert len(hosts)==1 and hosts[0].split('=',1)[1].strip()
 rules=[l for l in lines if not l.startswith('hostname = ')]
 assert len(rules)==2
 for line in rules:
  pattern,action,target=line.rsplit(' url ',1)[0],*line.rsplit(' url ',1)[1].split(' ',1)
  re.compile(pattern)
  assert action in ('script-request-header','script-response-body')
  assert target.startswith(BASE+'/modules/scripts/')
  assert (ROOT/'modules/scripts'/target.rsplit('/',1)[1]).is_file()

for name in ('weibo','netflix-rating'):
 text=(ROOT/f'modules/{name}.conf').read_text()
 validate(text)
 for section in ('[rewrite_local]','[mitm]'):
  try: validate(section+'\n'+text)
  except AssertionError: pass
  else: raise AssertionError('Did not reject invalid section header')
 local=(ROOT/f'modules/{name}-local.txt').read_text()
 assert '[rewrite_local]' in local and '[mitm]' in local
print('PASS: 2 remote resources, 4 invalid-header regressions, local installation snippets preserved. Device import still needs verification.')
