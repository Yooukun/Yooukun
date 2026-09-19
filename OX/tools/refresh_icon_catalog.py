#!/usr/bin/env python3
"""Refresh local mappings and custom manifest entries without updating upstream snapshots."""
import json
import urllib.parse
from manage import ROOT, BASE
from mirror_icons import relative

def main():
    folder=ROOT/'icons'
    original=json.loads((folder/'original-policies.json').read_text())
    mapping={name:BASE+'/icons/'+relative(url) for name,url in original.items()}
    mapping.update(json.loads((folder/'overrides.json').read_text()))
    manifest=[item for item in json.loads((folder/'manifest.json').read_text()) if not item['path'].startswith('custom/')]
    manifest+=json.loads((folder/'custom/manifest.json').read_text())
    manifest.sort(key=lambda x:x['path'])
    for filename,data in [('policies.json',mapping),('manifest.json',manifest)]:
        (folder/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# 图标目录','','含 2100 张镜像图标与自定义适配图标；来源和限制见 [README](README.md)。','','| 预览 | 路径 | URL |','|---|---|---|']
    for item in manifest:
        path=urllib.parse.quote(item['path'],safe='/')
        lines.append(f'| ![]({path}) | {item["path"]} | {BASE}/icons/{path} |')
    (folder/'INDEX.md').write_text('\n'.join(lines)+'\n')
    print('Refreshed',len(mapping),'policy mappings and',len(manifest),'indexed PNGs.')

if __name__=='__main__': main()
