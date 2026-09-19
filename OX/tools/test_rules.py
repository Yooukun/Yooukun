#!/usr/bin/env python3
"""Domain-only ordered model: regression tests, NOT a Quantumult X engine emulator."""
from manage import ROOT, SERVICES, active, rule
ordered=active((ROOT/'rules/Priority.list').read_text())
for name,_,_ in SERVICES: ordered+=active((ROOT/f'rules/{name}.list').read_text())
def match(host):
 for l in ordered:
  k,v=rule(l)
  if k=='host' and v==host or k=='host-suffix' and (v==host or host.endswith('.'+v)):
   return l.split(',')[-1].strip()
 return '兜底策略'
cases={'chatgpt.com':'OpenAI','api.openai.com':'OpenAI','claude.ai':'Claude','claude.com':'Claude',
 'api.anthropic.com':'Claude','www.youtube.com':'YouTube','www.netflix.com':'Netflix',
 'www.tiktok.com':'TikTok','www.douyin.com':'抖音','www.bilibili.com':'哔哩哔哩',
 'store.steampowered.com':'Steam商店','dl.steam.clngaa.com':'Steam下载',
 'disney.my.sentry.io':'Disney','www.paypal.com':'PayPal','www.riotgames.com':'Riot游戏',
 'www.pandalive.co.kr':'韩国直播','www.pornhub.com':'成人站点',
 'not-openai.example':'兜底策略','api.openai.com.evil.example':'兜底策略'}
for host,want in cases.items():
 got=match(host); assert got==want,(host,got,want)
print(f'PASS: {len(cases)} domain routing regressions, including shared-host exception and false-positive checks. Device engine not tested.')
