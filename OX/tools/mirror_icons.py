#!/usr/bin/env python3
"""Mirror pinned mini and Qure icon directories, retaining provenance and checksums."""
import io
import concurrent.futures
import hashlib
import json
import re
import urllib.request
import urllib.parse
import zipfile
from pathlib import Path
from manage import ROOT, BASE

CATALOG = ROOT/'icons/original-policies.json'
OWN = BASE+'/icons/'

def destination(repository, source):
    # macOS volumes may collapse Steam.png and steam.png: stable suffix keeps both.
    prefix='mini' if repository=='Orz-3/mini' else 'qure'
    original=source if prefix=='mini' else source[len('IconSet/'):]
    path=Path(original)
    filename=path.stem+'--'+hashlib.sha256(source.encode()).hexdigest()[:12]+path.suffix
    return str(Path(prefix)/path.parent/filename)

def relative(url):
    prefixes = {
        'https://raw.githubusercontent.com/Orz-3/mini/master/Color/': 'mini/',
        'https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/': 'qure/',
    }
    for prefix, folder in prefixes.items():
        if url.startswith(prefix):
            name=url[len(prefix):]
            assert '/' not in name and name.endswith('.png')
            repository='Orz-3/mini' if folder=='mini/' else 'Koolson/Qure'
            source=('Color/' if folder=='mini/' else 'IconSet/')+name
            return destination(repository,source)
    raise ValueError('Unapproved icon source')

def fetch(url):
    path=ROOT/'icons'/relative(url)
    if path.exists():
        data=path.read_bytes()
    else:
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=15) as response:
                    assert response.status==200
                    data=response.read()
                break
            except Exception:
                if attempt==2: raise
    assert data.startswith(b'\x89PNG\r\n\x1a\n')
    return url, path, data

def main():
    original=json.loads(CATALOG.read_text())
    manifest=[]
    libraries=[]
    for repository in ('Orz-3/mini','Koolson/Qure'):
        def get(url):
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(url,timeout=45) as response: return response.read()
                except Exception:
                    if attempt==2: raise
        meta=json.loads(get('https://api.github.com/repos/'+repository+'/commits/master'))
        revision=meta['sha']
        assert re.fullmatch('[0-9a-f]{40}', revision)
        print('Downloading pinned library:',repository,revision,flush=True)
        archive=zipfile.ZipFile(io.BytesIO(get('https://codeload.github.com/'+repository+'/zip/'+revision)))
        count=0
        for entry in archive.infolist():
            if entry.is_dir(): continue
            source=entry.filename.split('/',1)[1]
            is_mini=repository=='Orz-3/mini'
            if source=='README.md':
                target=ROOT/'icons'/('mini' if is_mini else 'qure')/'UPSTREAM-README.md'
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(archive.read(entry))
                continue
            if not source.lower().endswith('.png'): continue
            if is_mini and not source.startswith(('Color/','Alpha/')): continue
            if not is_mini and not source.startswith('IconSet/'): continue
            local_path=destination(repository,source)
            assert '..' not in Path(local_path).parts
            data=archive.read(entry)
            assert data.startswith(b'\x89PNG\r\n\x1a\n'), source
            target=ROOT/'icons'/local_path
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
            source_url='https://raw.githubusercontent.com/'+repository+'/'+revision+'/'+urllib.parse.quote(source,safe='/')
            manifest.append({'source_url':source_url,'path':local_path,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
            count+=1
        libraries.append({'repository':repository,'revision':revision,'png_count':count})
        print('Saved',count,'PNG assets from',repository,flush=True)
    custom=ROOT/'icons/custom/manifest.json'
    if custom.exists(): manifest.extend(json.loads(custom.read_text()))
    manifest.sort(key=lambda item:item['path'])
    assert len({item['path'] for item in manifest})==len(manifest)
    mapping={name:OWN+relative(url) for name,url in original.items()}
    overrides=ROOT/'icons/overrides.json'
    if overrides.exists(): mapping.update(json.loads(overrides.read_text()))
    assert all((ROOT/'icons'/relative(url)).is_file() for url in original.values())
    for filename,value in [('policies.json',mapping),('manifest.json',manifest),('libraries.json',libraries)]:
        (ROOT/'icons'/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    index=['# 可复用策略图标目录','','来源和限制见 [README](README.md)。包含 mini 的 Color/Alpha 与 Qure IconSet 全部 PNG。','','| 图标 | 文件 | 引用地址 |','|---|---|---|']
    for item in manifest:
        path=item['path']
        encoded=urllib.parse.quote(path,safe='/')
        index.append(f'| ![]({encoded}) | {path} | {OWN+encoded} |')
    (ROOT/'icons/INDEX.md').write_text('\n'.join(index)+'\n')
    print(f'Mirrored {len(manifest)} PNG files for {len(mapping)} policies; source SHA-256 recorded.')

if __name__=='__main__': main()
