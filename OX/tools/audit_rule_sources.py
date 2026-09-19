#!/usr/bin/env python3
"""Read-only upstream audit; write local evidence, never auto-publish."""
import concurrent.futures, datetime, hashlib, json, urllib.request, urllib.parse, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.datetime.now(datetime.timezone.utc)
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'OX-source-audit','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
    with urllib.request.urlopen(req,timeout=30) as r: return r.read()
manifest=json.loads((ROOT/'sources/manifest.json').read_text())
urls=[f['url'].replace(manifest['revision'],'master') for f in manifest['files'] if f['file']!='LICENSE']
urls += [x['url'] for x in json.loads((ROOT/'sources/legacy-link-audit.json').read_text()) if x['section']=='[filter_remote]']
urls += ['https://raw.githubusercontent.com/Semporia/TikTok-Unlock/master/Quantumult-X/TikTok.list']
def audit(url):
    parts=urllib.parse.urlsplit(url).path.lstrip('/').split('/',3)
    owner,repo,ref,path=parts; path=urllib.parse.unquote(path)
    record={'url':url,'repository':owner+'/'+repo,'path':path,'checked_at':NOW.isoformat()}
    historical=len(ref)==40
    try:
        data=get(url); record.update(readable=True,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e: record.update(readable=False,fetch_error=type(e).__name__+':'+str(getattr(e,'code','')))
    try:
        api='https://api.github.com/repos/'+owner+'/'+repo+'/commits?'+urllib.parse.urlencode({'path':path,'sha':ref,'per_page':1})
        commits=json.loads(get(api))
        if commits:
            c=commits[0]; date=c['commit']['committer']['date']
            days=(NOW-datetime.datetime.fromisoformat(date.replace('Z','+00:00'))).days
            record.update(last_file_commit=c['sha'],last_file_commit_date=date,age_days=days,commit_url=c['html_url'])
            record['status']='historical-pin' if historical else ('unreadable' if not record['readable'] else ('recent-180d' if days<=180 else 'older-than-180d'))
        else: record['status']='no-file-history'
    except Exception as e: record.update(status='activity-unverified',history_error=type(e).__name__+':'+str(getattr(e,'code','')))
    return record
if '--reuse-evidence' in sys.argv:
    records=json.loads((ROOT/'sources/source-activity.json').read_text())['files']
else:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(audit,dict.fromkeys(urls)))
if '--history-dir' in sys.argv:
    base=Path(sys.argv[sys.argv.index('--history-dir')+1])
    repos={'Semporia/TikTok-Unlock':'tiktok','Semporia/Quantumult-X':'semporia','ACL4SSR/ACL4SSR':'acl','GeQ1an/Rules':'geq'}
    for r in records:
        if r['repository'] in repos and not r.get('last_file_commit'):
            ref='refs/remotes/origin/master' if r['repository']=='GeQ1an/Rules' else 'HEAD'
            result=subprocess.check_output(['git','-C',str(base/repos[r['repository']]),'log','-1','--format=%H|%cI',ref,'--',r['path']],text=True,timeout=45).strip()
            if result:
                sha,date=result.split('|'); days=(NOW-datetime.datetime.fromisoformat(date)).days
                r.update(last_file_commit=sha,last_file_commit_date=date,age_days=days,commit_url='https://github.com/'+r['repository']+'/commit/'+sha,history_method='local filtered git history',status='recent-180d' if days<=180 else 'older-than-180d')
                r.pop('history_error',None)
        if r.get('fetch_error')=='HTTPError:404': r['status']='unavailable-404'
        if r['repository']=='Yooukun/Yooukun': r['status']='historical-pin'
(ROOT/'sources/source-activity.json').write_text(json.dumps({'checked_at':NOW.isoformat(),'recent_threshold_days':180,'warning':'Commit recency is a signal, not proof of rule validity or author maintenance. Historical pins are not current activity.', 'files':records},ensure_ascii=False,indent=2)+'\n')
# Pin comparison sources only; the build never consumes these snapshots.
entries={}
for name,repo,path in [('TikTok','Semporia/TikTok-Unlock','Quantumult-X/TikTok.list'),('DouYin','Semporia/Quantumult-X','Filter/DouYin.list')]:
    r=next(x for x in records if x['repository']==repo and x['path']==path)
    if not r.get('readable'): raise RuntimeError('Selected source unavailable: '+name)
    revision=r.get('last_file_commit')
    if not revision:
        revision=subprocess.check_output(['git','ls-remote','https://github.com/'+repo+'.git','refs/heads/master'],text=True,timeout=30).split()[0]
    url='https://raw.githubusercontent.com/'+repo+'/'+revision+'/'+path
    data=get(url)
    dest=ROOT/'sources/selected'/ (name+'.list'); dest.parent.mkdir(exist_ok=True); dest.write_bytes(data)
    entries[name]={'repository':repo,'revision':revision,'url':url,'file':'sources/selected/'+name+'.list','sha256':hashlib.sha256(data).hexdigest(),'last_file_commit_date':r.get('last_file_commit_date'),'selection':'Comparison only. User retained blackmatrix plus reviewed local corrections; never auto-merge Semporia. Unknown history is not an activity claim.'}
(ROOT/'sources/selected-sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
print(json.dumps({'files':len(records),'statuses':dict(Counter(x['status'] for x in records))}))
