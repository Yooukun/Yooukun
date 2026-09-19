#!/usr/bin/env python3
"""Mechanically merge icon attributes; preserve policy candidates and all other sections."""
import argparse
import concurrent.futures
import json
import re
import urllib.request
from pathlib import Path
from manage import ROOT

ICONS = json.loads((ROOT/'icons/policies.json').read_text())

def merge(text):
    result = []
    inside = False
    seen = set()
    for line in text.splitlines(keepends=True):
        if line.strip().startswith('['):
            inside = line.strip() == '[policy]'
        if inside and re.match(r'^(static|available)\s*=', line):
            name = line.split('=', 1)[1].split(',', 1)[0].strip()
            if name in ICONS:
                newline = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
                clean = re.sub(r',\s*img-url=[^,\r\n]+', '', line.rstrip('\r\n'))
                line = clean + ', img-url=' + ICONS[name] + newline
                seen.add(name)
        result.append(line)
    assert seen == set(ICONS), 'Missing or unmapped policy groups'
    return ''.join(result)

def check(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                data=response.read()
                assert response.status == 200 and data.startswith(b'\x89PNG\r\n\x1a\n'), 'Not PNG'
                return url, True
        except Exception:
            pass
    return url, False

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', type=Path)
    parser.add_argument('--check-network', action='store_true')
    parser.add_argument('--copy-from', type=Path, help='Create one new version, preserving the original')
    args=parser.parse_args()
    if args.copy_from:
        assert len(args.paths)==1 and not args.paths[0].exists(), 'New output path required'
    if args.check_network:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            results=list(pool.map(check, sorted(set(ICONS.values()))))
        for url, ok in results:
            if not ok: print('FAILED:', url)
        assert all(ok for _,ok in results), 'Icon download check failed'
        print(f'PASS: {len(results)} unique PNG URLs')
    for path in args.paths:
        source=args.copy_from or path
        original=source.read_bytes().decode('utf-8')
        updated=merge(original)
        strip=lambda s: re.sub(r',\s*img-url=[^,\r\n]+', '', s)
        assert strip(original)==strip(updated), 'Non-icon content changed'
        assert merge(updated)==updated
        path.write_bytes(updated.encode('utf-8'))
        path.chmod(source.stat().st_mode & 0o777)
        print('Updated policy icons:', path.name)

if __name__=='__main__':
    main()
