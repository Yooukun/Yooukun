#!/usr/bin/env python3
"""OX rules: pinned import, deterministic build, private export, static validation.
Generated rule data retains upstream GPL-2.0 license. No subscription is fetched.
"""
import argparse
import concurrent.futures
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REV = 'aa137cf64cda1474352875cc7e01b6f7d087cc0d'
UPSTREAM = 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/'
BASE = 'https://raw.githubusercontent.com/Yooukun/Yooukun/yoh_96/OX'
# Earlier entries own exact duplicates. Service-specific lists precede aggregates.
SERVICES = [
 ('Lan','局域网','direct'), ('OpenAI','OpenAI','AI节点'),
 ('Claude','Claude','AI节点'), ('SteamCN','Steam下载','direct'),
 ('Steam','Steam商店','默认代理'), ('PayPal','PayPal','direct'),
 ('Telegram','Telegram','默认代理'), ('Twitter','X推特','默认代理'),
 ('YouTube','YouTube','默认代理'), ('Netflix','Netflix','默认代理'),
 ('Disney','Disney','默认代理'), ('HBO','HBO','默认代理'),
 ('TikTok','TikTok','默认代理'), ('BiliBili','哔哩哔哩','direct'),
 ('NetEaseMusic','网易云音乐','direct'), ('DouYin','抖音','direct'),
 ('Weibo','微博','direct'), ('Riot','Riot游戏','direct'),
 ('Speedtest','测速','direct'), ('Pornhub','Pornhub','默认代理'),
 ('KoreanLive','韩国直播','韩国'),
 ('Apple','Apple','direct'), ('Microsoft','Microsoft','direct'),
 ('Google','Google','默认代理'), ('GlobalMedia','其他海外媒体','默认代理'),
 ('ChinaMax','国内服务','direct')]
REGIONS = {'香港':'Hong Kong|香港|\\bHK\\b', '新加坡':'Singapore|新加坡|\\bSG\\b',
 '日本':'Japan|日本|\\bJP\\b', '美国':'United States|美国|\\bUS\\b',
 '台湾':'Taiwan|台湾|\\bTW\\b', '德国':'Germany|德国|\\bDE\\b',
 '英国':'United Kingdom|英国|\\bUK\\b', '韩国':'South Korea|韩国|\\bKR\\b',
 '澳大利亚':'Australia|澳大利亚|\\bAU\\b', '法国':'France|法国|\\bFR\\b',
 '瑞士':'Switzerland|瑞士|\\bCH\\b', '荷兰':'Netherlands|荷兰|\\bNL\\b',
 '印度':'India|印度|\\bIN\\b'}
LOCAL = {'Pornhub','KoreanLive'}
SHARED = set('sentry.io stripe.com auth0.com algolia.net intercom.io intercomcdn.com segment.io identrust.com launchdarkly.com onetrust.com'.split())
SHARED_HOSTS = set('cdn.usefathom.com static.cloudflareinsights.com browser-intake-datadoghq.com'.split())

def write(path, data):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(data, encoding='utf-8')

def fetch(url):
 req = urllib.request.Request(url, headers={'User-Agent':'OX-maintainer/1.0'})
 with urllib.request.urlopen(req, timeout=40) as r:
  return r.read().decode('utf-8-sig')

def active(text):
 return [l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith(('#',';','//'))]

def sections(text):
 result = {}; section = None
 for line in active(text):
  if line.startswith('['):
   section = line; result[section] = []
  elif section:
   result[section].append(line)
 return result

def rule(line):
 p = [x.strip() for x in line.split(',')]
 if len(p) != 3:
  raise ValueError('Unsupported rule field count: '+line)
 kind, value = p[0].lower(), p[1].lower()
 if kind in ('host','host-suffix'):
  if not re.fullmatch(r'[a-z0-9_.-]+', value) or '*' in value or '?' in value:
   raise ValueError('Invalid host rule: '+line)
 elif kind in ('ip-cidr','ip6-cidr'):
  net = ipaddress.ip_network(value, strict=False)
  if net.version != (4 if kind == 'ip-cidr' else 6):
   raise ValueError('Address family mismatch')
  value = str(net)
 elif kind in ('host-keyword','host-wildcard','user-agent','ip-asn','geoip'):
  if not value:
   raise ValueError('Empty rule')
 else:
  raise ValueError('Unsupported rule: '+line)
 return kind, value

def snapshot(rev, target):
 # Fully fetch and parse BEFORE changing any files. Failed downloads preserve prior data.
 paths = [f'rule/QuantumultX/{s}/{s}.list' for s,_,_ in SERVICES if s not in LOCAL] + ['LICENSE']
 def one(path):
  url = UPSTREAM+rev+'/'+path
  text = fetch(url)
  if path != 'LICENSE':
   entries = active(text)
   if not entries: raise ValueError('Empty source: '+path)
   for l in entries: rule(l)
  return path, text, url
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  results = list(pool.map(one, paths))
 manifest = {'repository':'blackmatrix7/ios_rule_script','revision':rev,
  'license':'GPL-2.0','files':[]}
 for path, data, url in results:
  name = Path(path).name
  write(target/'sources/upstream'/name, data)
  manifest['files'].append({'file':name,'url':url,'sha256':hashlib.sha256(data.encode()).hexdigest()})
 write(target/'sources/manifest.json', json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

def build(root):
 seen = {}; report = {'counts':{}, 'removed_exact_duplicates':[], 'broad_rules':[], 'suffix_overlaps':[], 'excluded':[]}
 manifest = json.loads((root/'sources/manifest.json').read_text())
 exclusions=json.loads((ROOT/'sources/exclusions.json').read_text())
 for f in manifest['files']:
  data = (root/'sources/upstream'/f['file']).read_bytes()
  assert hashlib.sha256(data).hexdigest() == f['sha256'], f['file']+' source hash mismatch'
 for name, policy, _ in SERVICES:
  out = []
  source = root/f'sources/upstream/{name}.list'
  raw = active(source.read_text()) if name not in LOCAL else []
  additions = ROOT/f'sources/local/{name}.list'
  if additions.exists(): raw = active(additions.read_text()) + raw
  for l in raw:
   k = rule(l)
   reason = None
   if k[1] in exclusions.get(name,[]): reason='OX reviewed scope exclusion; see sources/exclusions.json'
   if k[0] in ('host-keyword','host-wildcard','user-agent'): reason='Broad pattern retained in source, omitted from release pending evidence'
   if k[1] in SHARED or k[1] in SHARED_HOSTS: reason='Shared infrastructure must not be owned by a single service'
   if name in ('OpenAI','Claude') and k[0] in ('ip-asn','ip-cidr','ip6-cidr'): reason='Unverified shared or stale AI IP allocation'
   if reason:
    report['excluded'].append({'service':name,'rule':list(k),'reason':reason}); continue
   if k in seen:
    report['removed_exact_duplicates'].append({'rule':list(k),'kept':seen[k],'removed':name}); continue
   seen[k] = name
   if k[0] in ('host-keyword','host-wildcard','user-agent'):
    report['broad_rules'].append({'service':name,'rule':list(k)})
   out.append(f'{k[0]}, {k[1]}, {policy}')
  report['counts'][name] = len(out)
  assert out, name+' empty'
  header = (f'# OX / {name}; generated from pinned source and local edits; GPL-2.0\n'
   f'# Source: blackmatrix7/ios_rule_script @ {manifest["revision"]}\n'
   '# Original source and license: sources/upstream/; modifications: policy binding, normalization, exact deduplication.\n')
  write(root/f'rules/{name}.list',header+'\n'.join(out)+'\n')
 suffixes = {v:n for (k,v),n in seen.items() if k=='host-suffix'}
 for (kind,v),n in seen.items():
  if kind not in ('host','host-suffix'): continue
  parts=v.split('.')
  for i in range(0 if kind=='host' else 1,len(parts)-1):
   parent='.'.join(parts[i:])
   if parent in suffixes and suffixes[parent]!=n:
    report['suffix_overlaps'].append({'domain':v,'specific':n,'parent':parent,'general':suffixes[parent]})
 # Put every cross-list specific exception into a dedicated, policy-bearing first resource.
 # No force-policy on this file: each entry must retain its own target.
 domains={r['domain'] for r in report['suffix_overlaps']}
 policies={n:p for n,p,_ in SERVICES}; policies['Lan']='direct'
 priority=[(k,v,n) for (k,v),n in seen.items() if k in ('host','host-suffix') and v in domains]
 priority.sort(key=lambda x:(-len(x[1].split('.')),x[1],0 if x[0]=='host' else 1))
 write(root/'rules/Priority.list','# OX generated cross-service specific exceptions. GPL-2.0. Do not set force-policy.\n'+
  '\n'.join(f'{k}, {v}, {policies[n]}' for k,v,n in priority)+'\n')
 report['priority_exceptions']=len(priority)
 write(root/'sources/build-report.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 write(root/'profiles/quantumultx.conf',profile())
 print(json.dumps({'rules':sum(report['counts'].values()),'lists':len(SERVICES),
  'duplicates_removed':len(report['removed_exact_duplicates']),
  'broad_rules':len(report['broad_rules']),'suffix_overlaps':len(report['suffix_overlaps'])}))

def profile():
 lines=['# OX v1 / public template. Replace node subscription and private DNS before use.',
  '[general]', 'network_check_url = http://connect.rom.miui.com/generate_204',
  'server_check_url = http://www.gstatic.com/generate_204', 'icmp_auto_reply = true',
  '', '[dns]', '# Personal export preserves current DNS and alias settings.',
  'doh-server = https://dns.alidns.com/dns-query', '', '[policy]']
 for name,regex in REGIONS.items():
  lines.append(f'static = {name}, resource-tag-regex=^Kuromis$, server-tag-regex=(?i)({regex})')
 lines += ['available = 故障切换, resource-tag-regex=^Kuromis$',
  'static = mono, resource-tag-regex=^mono$',
  'static = 默认代理, 故障切换, '+', '.join(REGIONS)+', mono',
  'static = 兜底策略, 默认代理, direct']
 for name,policy,default in SERVICES:
  if name=='Lan': continue
  if name in ('OpenAI','Claude'):
   lines.append(f'static = {policy}, resource-tag-regex=^Kuromis$, server-tag-regex=(?i)(Singapore|Japan|United States|新加坡|日本|美国)')
   continue
  elif name=='TikTok':
   opts=['日本','美国','台湾','默认代理','direct']
  else:
   opts=list(dict.fromkeys([default,'direct','默认代理',*REGIONS]))
  lines.append('static = '+policy+', '+', '.join(opts))
 lines += ['', '[server_remote]',
  '# Insert private Quantumult X subscription here with tag=Kuromis; never commit credentials.',
  '', '[filter_remote]',
  f'{BASE}/rules/Priority.list, tag=OX-Priority, update-interval=86400, opt-parser=false, enabled=true']
 for name,policy,_ in SERVICES:
  forced='direct' if name=='Lan' else policy
  lines.append(f'{BASE}/rules/{name}.list, tag=OX-{name}, force-policy={forced}, update-interval=86400, opt-parser=false, enabled=true')
 lines += ['', '[rewrite_remote]', '# Experimental modules: enable individually AFTER device certificate installation and testing.',
  f'{BASE}/modules/weibo.conf, tag=OX-微博增强, update-interval=86400, opt-parser=false, enabled=false',
  f'{BASE}/modules/netflix-rating.conf, tag=OX-Netflix评分, update-interval=86400, opt-parser=false, enabled=false',
  '', '[server_local]', '', '[filter_local]',
  '# Add tested personal exceptions here. No broad geoip CN override.',
  'final, 兜底策略', '', '[rewrite_local]', '# Optional local scripts: see modules/README.md.',
  '', '[task_local]', '', '[http_backend]', '', '[mitm]',
  '# Generate and trust a NEW certificate on device only when enabling an HTTPS rewrite.',
  'skip_validating_cert = false', '']
 icons=json.loads((ROOT/'icons/policies.json').read_text())
 for i,line in enumerate(lines):
  if line.startswith(('static = ', 'available = ')):
   name=line.split('=',1)[1].split(',',1)[0].strip()
   lines[i]=line+', img-url='+icons[name]
 return '\n'.join(lines)

def export(current, out, remote_ready=False):
 text = profile()
 src = sections(current.read_text())
 assert len(src['[server_remote]'])>=1
 subscriptions=[]
 for index,line in enumerate(src['[server_remote]']):
  line=re.sub(r',\s*img-url=[^,]+','',line)
  if index==0: line=re.sub(r'tag=[^,]+','tag=Kuromis',line)
  subscriptions.append(line)
 subscription='\n'.join(subscriptions)
 text = text.replace('# Insert private Quantumult X subscription here with tag=Kuromis; never commit credentials.',subscription)
 text = text.replace('doh-server = https://dns.alidns.com/dns-query','\n'.join(src['[dns]']))
 out.mkdir(parents=True, exist_ok=True)
 remote = out/('OX-个人版-远程规则.conf' if remote_ready else 'OX-个人版-远程规则-待公开托管.conf.template')
 write(remote,text); remote.chmod(0o600)
 # Self-contained rules work before publication and on a first launch without GitHub access.
 parts=text.split('[filter_remote]')
 tail=parts[1].split('[rewrite_remote]',1)[1]
 embedded=active((ROOT/'rules/Priority.list').read_text())
 for name,policy,_ in SERVICES:
  for l in active((ROOT/f'rules/{name}.list').read_text()):
   k,v=rule(l); embedded.append(f'{k}, {v}, '+('direct' if name=='Lan' else policy))
 offline=parts[0]+'[filter_remote]\n# Rules embedded below.\n\n[rewrite_remote]'+tail
 offline=offline.replace('final, 兜底策略','\n'.join(embedded)+'\nfinal, 兜底策略')
 local=out/'OX-个人版-内置规则.conf'; write(local,offline); local.chmod(0o600)
 print('Private profiles exported; subscription and DNS values not logged.')

def validate(root):
 s=sections((root/'profiles/quantumultx.conf').read_text())
 names=[]; references={}
 for l in s['[policy]']:
  kind,rest=l.split('=',1); fields=[x.strip() for x in rest.split(',')]
  names.append(fields[0]); references[fields[0]]=[x for x in fields[1:] if '=' not in x]
  for field in fields[1:]:
   if 'regex=' in field: re.compile(field.split('=',1)[1])
 assert len(names)==len(set(names)), 'Duplicate policy names'
 for name,refs in references.items():
  for ref in refs: assert ref in names or ref in ('direct','proxy','reject'), (name,ref)
 def walk(n,stack):
  assert n not in stack, 'Policy cycle'
  for dep in references.get(n,[]): walk(dep,stack+[n])
 for n in names: walk(n,[])
 all_rules={}
 for name,policy,_ in SERVICES:
  for l in active((root/f'rules/{name}.list').read_text()):
   k=rule(l); assert k not in all_rules, ('Duplicate',k)
   assert l.split(',')[-1].strip()==policy
   all_rules[k]=name
 for line in s['[filter_remote]']:
  url=line.split(',')[0]; assert url.startswith(BASE+'/rules/')
  assert (root/'rules'/url.rsplit('/',1)[1]).is_file()
  match=re.search(r'force-policy=([^,]+)',line)
  if match: assert match[1] in names or match[1]=='direct'
  else:
   assert url.endswith('/Priority.list')
   for l in active((root/'rules/Priority.list').read_text()):
    rule(l); assert l.split(',')[-1].strip() in names+['direct']
 assert s['[filter_local]'][-1]=='final, 兜底策略'
 assert not any('skip_validating_cert = true' in l for l in s['[mitm]'])
 for folder in ('profiles','rules','sources','modules'):
  if not (root/folder).exists(): continue
  for p in (root/folder).rglob('*'):
   if p.is_file():
    content=p.read_text()
    assert not re.search(r'(?:[?&]token=|^\s*p12\s*=|^\s*passphrase\s*=)',content,re.M), 'Secret-like field in '+str(p)
 print(f'PASS: {len(names)} policies, {len(all_rules)} unique rules, references, regex syntax, cycles, own URLs, secret-field scan. Device behavior NOT tested.')

def main():
 p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
 a=sub.add_parser('snapshot'); a.add_argument('--revision',default=REV); a.add_argument('--target',type=Path,required=True)
 a=sub.add_parser('build'); a.add_argument('--root',type=Path,default=ROOT)
 a=sub.add_parser('validate'); a.add_argument('--root',type=Path,default=ROOT)
 a=sub.add_parser('export'); a.add_argument('--current',type=Path,required=True); a.add_argument('--out',type=Path,required=True); a.add_argument('--remote-ready',action='store_true',help='Use only after anonymous public resource verification passes')
 a=p.parse_args()
 if a.cmd=='snapshot':
  assert re.fullmatch('[0-9a-f]{40}',a.revision), 'Use immutable full commit SHA'
  snapshot(a.revision,a.target)
 elif a.cmd=='build': build(a.root)
 elif a.cmd=='validate': validate(a.root)
 elif a.cmd=='export': export(a.current,a.out,a.remote_ready)

if __name__=='__main__': main()
