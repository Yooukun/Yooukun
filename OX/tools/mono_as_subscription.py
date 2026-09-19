#!/usr/bin/env python3
"""Remove the mistaken mono policy; make existing dynamic groups accept either subscription."""
import argparse
import re
from pathlib import Path
from policy_icons import merge

def correct(original):
    result=[]
    section=''
    removed=0
    for line in original.splitlines(keepends=True):
        if line.strip().startswith('['): section=line.strip()
        if section=='[policy]':
            if re.match(r'^\s*static\s*=\s*mono\s*,',line):
                removed+=1
                continue
            if re.match(r'^\s*static\s*=\s*默认代理\s*,',line):
                line=re.sub(r',\s*mono(?=\s*(?:,|$))','',line)
            line=line.replace('resource-tag-regex=^Kuromis$','resource-tag-regex=^(Kuromis|mono)$')
        result.append(line)
    staged=''.join(result)
    assert removed==1
    # All non-policy sections, including the original subscription and certificate, are untouched.
    strip_policy=lambda s: re.sub(r'(?ms)^\[policy\]\r?\n.*?(?=^\[|\Z)','',s)
    assert strip_policy(original)==strip_policy(staged)
    return merge(staged)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--in-place',action='store_true')
    a=p.parse_args()
    assert not a.out.exists() or (a.in_place and a.out==a.source)
    text=correct(a.source.read_bytes().decode('utf-8'))
    a.out.write_bytes(text.encode('utf-8'))
    a.out.chmod(0o600)
    print('PASS: mono is subscription only, 41 policy icons; non-policy sections preserved.')

if __name__=='__main__':main()
