#!/usr/bin/env python3
"""Ordered domain/keyword and supplied-UA model, NOT a Quantumult X engine emulator."""
from manage import ROOT, SERVICES, active, rule
import fnmatch
ordered=active((ROOT/'rules/Priority.list').read_text())
for name,_,_ in SERVICES: ordered+=active((ROOT/f'rules/{name}.list').read_text())
def match(host, user_agent=''):
 for l in ordered:
  k,v=rule(l)
  if (k=='host' and v==host or k=='host-suffix' and (v==host or host.endswith('.'+v))
      or k=='host-keyword' and v in host or k=='user-agent' and user_agent and fnmatch.fnmatchcase(user_agent,v)):
   return l.split(',')[-1].strip()
 return '兜底策略'
cases={'chatgpt.com':'OpenAI','api.openai.com':'OpenAI','claude.ai':'Claude','claude.com':'Claude',
 'api.anthropic.com':'Claude','www.youtube.com':'YouTube','www.netflix.com':'Netflix',
 'www.tiktok.com':'TikTok','www.douyin.com':'抖音','www.bilibili.com':'哔哩哔哩',
 'store.steampowered.com':'Steam商店','dl.steam.clngaa.com':'Steam下载',
 'disney.my.sentry.io':'Disney','www.paypal.com':'PayPal','www.riotgames.com':'Riot游戏',
 'www.pandalive.co.kr':'韩国直播','www.pornhub.com':'Pornhub',
 'www.leagueoflegends.com':'Riot游戏','wildrift.leagueoflegends.com':'Riot游戏',
 'playvalorant.com':'Riot游戏','teamfighttactics.leagueoflegends.com':'Riot游戏',
 '2xko.riotgames.com':'Riot游戏','playruneterra.com':'兜底策略',
 'not-openai.example':'兜底策略','api.openai.com.evil.example':'兜底策略',
 'api.snssdk.com':'direct','tiktok.snssdk.com':'direct','www.ixigua.com':'国内服务',
 'www.toutiao.com':'国内服务','cdn.douyinvod.example':'兜底策略',
 'p16-tiktokcdn-com.akamaized.net':'TikTok','v.tiktokv.com':'TikTok',
 'cdn-tiktokcdn-com.example':'兜底策略'}
for host,want in cases.items():
 got=match(host); assert got==want,(host,got,want)
assert match('unknown-service.example','TikTok/46.9.0')=='兜底策略'
assert match('api.snssdk.com','TikTok/46.9.0')=='direct'
assert match('www.capcut.com')!='TikTok'
assert match('www.trae.ai')!='TikTok'
assert match('api.isnssdk.com')=='TikTok'
print(f'PASS: {len(cases)} domain routing regressions, including shared-host exception and false-positive checks. Device engine not tested.')
