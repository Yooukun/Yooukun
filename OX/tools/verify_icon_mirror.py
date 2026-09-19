#!/usr/bin/env python3
"""Verify all local assets, and optionally every public Git blob at an immutable commit."""
import argparse
import hashlib
import json
import re
import urllib.request
from manage import ROOT, BASE

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--published-revision')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'icons/manifest.json').read_text())
    libraries=json.loads((ROOT/'icons/libraries.json').read_text())
    custom=ROOT/'icons/custom/manifest.json'
    extra=json.loads(custom.read_text()) if custom.exists() else []
    assert len(manifest)==sum(lib['png_count'] for lib in libraries)+len(extra)
    assert len({item['path'] for item in manifest})==len(manifest)
    blobs={}
    for item in manifest:
        data=(ROOT/'icons'/item['path']).read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n'),item['path']
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        blobs['OX/icons/'+item['path']]=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    icons=json.loads((ROOT/'icons/policies.json').read_text())
    for url in icons.values():
        assert url.startswith(BASE+'/icons/')
        assert 'OX/icons/'+url[len(BASE+'/icons/'):] in blobs
    if args.published_revision:
        assert re.fullmatch('[0-9a-f]{40}',args.published_revision)
        url='https://api.github.com/repos/Yooukun/Yooukun/git/trees/'+args.published_revision+'?recursive=1'
        with urllib.request.urlopen(url,timeout=30) as response: tree=json.load(response)
        assert not tree.get('truncated')
        remote={item['path']:item['sha'] for item in tree['tree'] if item['type']=='blob'}
        for path,sha in blobs.items(): assert remote.get(path)==sha,path
        print(f'PASS: all {len(blobs)} public Git blobs match local assets at immutable revision.')
    print(f'PASS: {len(manifest)} PNG signatures, sizes and SHA-256; {len(icons)} own-host policy URLs.')

if __name__=='__main__': main()
