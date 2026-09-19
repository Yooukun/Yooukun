"""Semporia remains evidence only; blackmatrix/manual release boundaries persist."""
import hashlib, json
from manage import ROOT, active, rule
manifest=json.loads((ROOT/'sources/selected-sources.json').read_text())
for name,count in [('TikTok',18),('DouYin',15)]:
    item=manifest[name]
    data=(ROOT/item['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==item['sha256']
    source=[rule(l) for l in active(data.decode())]
    assert len(source)==count
    released=[rule(l) for l in active((ROOT/f'rules/{name}.list').read_text())]
    assert len(released)=={'TikTok':22,'DouYin':9}[name]
    assert source!=released
    assert not any(k in ('host-keyword','user-agent') for k,v in released)
    assert ('host-suffix','snssdk.com') not in released
priority=active((ROOT/'rules/Priority.list').read_text())
assert priority[0]=='host-suffix, snssdk.com, direct'
assert ('host-suffix','isnssdk.com') in [rule(l) for l in active((ROOT/'rules/TikTok.list').read_text())]
print('PASS: Semporia evidence only; blackmatrix 22/9 rules, no broad imports, one shared-domain priority exception.')
