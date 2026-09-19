#!/usr/bin/env python3
"""Read configs locally; audit public references only. Never fetch subscription/DoH URLs."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

def main():
 p=argparse.ArgumentParser(); p.add_argument('old',type=Path); p.add_argument('--out',type=Path,required=True)
 a=p.parse_args(); jobs={}; sec=''
 for raw in a.old.read_text().splitlines():
  line=raw.strip()
  if line.startswith('['): sec=line; continue
  if not line or line.startswith(('#',';','//')): continue
  if sec not in ('[filter_remote]','[rewrite_remote]','[rewrite_local]'): continue
  for url in re.findall(r'https://[^\s,]+',line):
   if not url.startswith(('https://raw.githubusercontent.com/','https://cdn.jsdelivr.net/')): continue
   jobs[url]=sec
 def check(item):
  url,sec=item
  row={'section':sec,'url':url}
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OX-audit'}),timeout=25) as r:
    data=r.read(); row.update(status=r.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    if sec=='[rewrite_local]':
     text=data.decode('utf-8-sig')
     row['script_apis']=sorted(set(re.findall(r'\$(?:task|httpClient|prefs|persistentStore|done|request|response|notify|notification)\b',text)))
     row['note']='Downloaded for static review only; not executed; API compatibility and current app behavior unverified.'
  except urllib.error.HTTPError as e: row.update(status=e.code)
  except Exception as e: row.update(status='network-error',error=type(e).__name__)
  return row
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(check,jobs.items()))
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'references':len(results),'http_200':sum(r['status']==200 for r in results),
  'unavailable':[{'url':r['url'],'status':r['status']} for r in results if r['status']!=200]},ensure_ascii=False))
if __name__=='__main__': main()
