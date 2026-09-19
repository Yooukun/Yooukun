#!/usr/bin/env python3
"""Preserve licensed legacy scripts at immutable revision; never execute them."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from manage import ROOT, BASE, fetch, write, sections

REV='06d6e36771880959c008d3c59c192068f00ddd51'
def main():
 p=argparse.ArgumentParser(); p.add_argument('old',type=Path); p.add_argument('--offline',action='store_true'); a=p.parse_args()
 original=sections(a.old.read_text())['[rewrite_local]']
 manifest=[]
 for name in ['wb_launch.js','wb_ad.js','nf_rating.js','LICENSE']:
  url=f'https://raw.githubusercontent.com/yichahucha/surge/{REV}/{name}'
  data=(ROOT/'modules/vendor/yichahucha'/name).read_text() if a.offline else fetch(url)
  write(ROOT/'modules/vendor/yichahucha'/name,data)
  if name.endswith('.js'):
   modified=data
   if name=='nf_rating.js':
    modified=re.sub(r'function IMDbApikeys\(\)\s*\{.*?^\}', 'function IMDbApikeys() { return []; }', modified, flags=re.S|re.M)
    modified=modified.replace('"ImdbApikeyCacheKey"','"OX_OMDB_API_KEY"')
    modified=modified.replace('if (!IMDbApikey) updateIMDbApikey();', 'if (!IMDbApikey) { $done({}); return; }')
    modified=modified.replace('function IMDbApikeys()', 'function getIMDbApikeys()').replace('var IMDbApikeys = IMDbApikeys();','var IMDbApikeys = getIMDbApikeys();')
   modified=('/* OX derivative of yichahucha/surge @ '+REV+'; GPL-3.0.\n'
    'Modifications: synchronous failures pass through; Netflix requires own OMDb preference key, shared key pool removed. */\n'
    '(function () { try {\n'+modified+'\n} catch (error) { $done({}); } })();\n')
   write(ROOT/'modules/scripts'/name,modified)
  manifest.append({'file':name,'source':url,'sha256':hashlib.sha256(data.encode()).hexdigest(),'license':'GPL-3.0','modified':False})
 write(ROOT/'modules/manifest.json',json.dumps(manifest,indent=2)+'\n')
 for group,needle,hosts in [('weibo','wb_', 'api.weibo.cn, mapi.weibo.com, *.uve.weibo.com'),
                            ('netflix-rating','nf_rating','ios-*.prod.ftl.netflix.com, ios.prod.ftl.netflix.com')]:
  matches=[]
  for line in original:
   if needle not in line: continue
   script=line.rsplit('/',1)[1]
   matches.append(re.sub(r'https://\S+$',BASE+'/modules/scripts/'+script,line))
  write(ROOT/f'modules/{group}.conf','# EXPERIMENTAL: static source preserved; current app endpoints not device-tested.\n[rewrite_local]\n'+'\n'.join(matches)+'\n\n[mitm]\nhostname = '+hosts+'\n')
  write(ROOT/f'modules/{group}-local.txt','# Merge lines below into the corresponding sections. Copy JS files into Quantumult X/Scripts.\n[rewrite_local]\n'+'\n'.join(re.sub(r'https://\S+/', '',l) for l in matches)+'\n\n[mitm]\nhostname = '+hosts+'\n')
 # Historical TikTok rules are archived as comments, NOT offered as an enabled working module.
 lines=[l for l in original if ' url 30' in l]
 write(ROOT/'modules/tiktok-legacy.txt','# Historical only: unbounded parameter replacements; unsupported current efficacy.\n'+'\n'.join('; '+l for l in lines)+'\n')
 print('Preserved 3 scripts plus GPL-3.0 license; two experimental modules and local-script snippets. No script execution.')
if __name__=='__main__': main()
