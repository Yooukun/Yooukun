#!/usr/bin/env python3
"""Read-only anonymous verification of all runtime public resources."""
import concurrent.futures
import hashlib
import json
from manage import ROOT, BASE, fetch

files = sorted((ROOT/'rules').glob('*.list')) + sorted((ROOT/'modules/scripts').glob('*.js'))
files += [ROOT/'modules/weibo.conf', ROOT/'modules/netflix-rating.conf', ROOT/'profiles/quantumultx.conf']
def check(path):
 rel=path.relative_to(ROOT).as_posix()
 expected=hashlib.sha256(path.read_bytes()).hexdigest()
 error=''
 for attempt in range(3):
  try:
   actual=hashlib.sha256(fetch(BASE+'/'+rel).encode()).hexdigest()
   if actual==expected: return {'file':rel,'ok':True}
   error='SHA256 mismatch'
  except Exception as exc:
   error=type(exc).__name__
 return {'file':rel,'ok':False,'error':error}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 results=list(pool.map(check,files))
failed=[r for r in results if not r['ok']]
print(json.dumps({'checked':len(results),'passed':len(results)-len(failed),'failed':failed},ensure_ascii=False))
raise SystemExit(1 if failed else 0)
