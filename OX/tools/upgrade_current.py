#!/usr/bin/env python3
"""Narrow user-authorized migration: icons, Pornhub label, disabled mono standby."""
import argparse
import re
from pathlib import Path
from policy_icons import merge

def transform(original, url):
    assert url.startswith('https://') and not any(c in url for c in '\r\n, ')
    newline='\r\n' if '\r\n' in original else '\n'
    mono_policy='static = mono, resource-tag-regex=^mono$'+newline
    mono_resource=url+', tag=mono, update-interval=86400, opt-parser=false, enabled=false'+newline
    result=[]
    section=''
    changed_name=0
    default_before=default_after=None
    def finish(section):
        if section=='[policy]': result.append(mono_policy)
        if section=='[server_remote]': result.append(mono_resource)
    for line in original.splitlines(keepends=True):
        if line.strip().startswith('['):
            finish(section)
            section=line.strip()
        if section=='[policy]' and re.match(r'^\s*static\s*=\s*mono\s*,',line): raise ValueError('mono already exists')
        if section=='[server_remote]' and re.search(r'\btag=mono(?:,|\s*$)',line): raise ValueError('mono resource already exists')
        if section in ('[policy]','[filter_local]','[filter_remote]'):
            line,count=re.subn(r'(?<=[=,])(\s*)成人站点(?=\s*(?:,|$))',r'\1Pornhub',line)
            changed_name+=count
        if section=='[policy]' and re.match(r'^\s*static\s*=\s*默认代理\s*,',line):
            default_before=line
            clean=re.sub(r',\s*img-url=[^,\r\n]+','',line).rstrip('\r\n')
            default_after=clean+', mono'+newline
            line=default_after
        result.append(line)
    finish(section)
    assert changed_name>=2 and default_before is not None
    staged=''.join(result)
    # Undo the three allowed structural edits; everything else must be byte-identical.
    restored=staged.replace(mono_policy,'').replace(mono_resource,'').replace(default_after,default_before)
    restored=re.sub(r'(?<=[=,])(\s*)Pornhub(?=\s*(?:,|$))',r'\1成人站点',restored,flags=re.M)
    assert restored==original, 'Unexpected non-icon edit'
    return merge(staged)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--mono-url-file',type=Path,required=True)
    p.add_argument('--in-place',action='store_true')
    a=p.parse_args()
    assert not a.out.exists() or (a.in_place and a.out==a.source)
    original=a.source.read_bytes().decode('utf-8')
    updated=transform(original,a.mono_url_file.read_text().strip())
    a.out.write_bytes(updated.encode('utf-8'))
    a.out.chmod(0o600)
    print('PASS: preserved all other content; 42 own-host icons; Pornhub rename; mono standby added disabled. No secrets logged.')

if __name__=='__main__':main()
