#!/usr/bin/env python3
"""Compare a candidate rules build; never copy/promote/publish it automatically."""
import argparse
import json
from pathlib import Path
from manage import ROOT, active
p=argparse.ArgumentParser(); p.add_argument('candidate',type=Path); a=p.parse_args()
report={}; blocked=[]
for current in sorted((ROOT/'rules').glob('*.list')):
 other=a.candidate/'rules'/current.name
 if not other.exists(): blocked.append(current.name+': missing'); continue
 old=set(active(current.read_text())); new=set(active(other.read_text()))
 added=sorted(new-old); removed=sorted(old-new)
 report[current.name]={'before':len(old),'after':len(new),'added':added,'removed':removed}
 if not new or len(removed)>max(10,len(old)*0.1): blocked.append(current.name+': empty or >10% removal (minimum 10 rules)')
print(json.dumps({'review_required':True,'blocked':blocked,'diff':report},ensure_ascii=False,indent=2))
raise SystemExit(2 if blocked else 0)
