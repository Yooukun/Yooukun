"""Generate a service-by-service source registry from live audit evidence."""
import json
from pathlib import Path
from manage import ROOT, SERVICES
audit=json.loads((ROOT/'sources/source-activity.json').read_text())
records=audit['files']
def find(repo,path):
    return next(x for x in records if x['repository']==repo and x['path']==path)
fallback={
 'Lan':['Clash/LocalAreaNetwork.list','Clash/UnBan.list'],
 'SteamCN':['Clash/Download.list'], 'Apple':['Clash/Apple.list'],
 'Netflix':['Clash/Netflix.list'], 'Telegram':['Clash/Telegram.list'],
 'Twitter':['Clash/Ruleset/Twitter.list'], 'YouTube':['Clash/Ruleset/YouTube.list'],
 'Disney':['Clash/Ruleset/DisneyPlus.list'],
 'BiliBili':['Clash/Ruleset/Bilibili.list','Clash/Ruleset/BilibiliHMT.list'],
 'GlobalMedia':['Clash/ProxyLite.list'],
 'ChinaMax':['Clash/ChinaDomain.list','Clash/ChinaCompanyIp.list']}
special={'NetEaseMusic':('GeQ1an/Rules','QuantumultX/Filter/Optional/Netease Music.list'),
 'HBO':('Yooukun/Yooukun','HBO.list'), 'PayPal':('Yooukun/Yooukun','paypal.list'),
 'Riot':('Yooukun/Yooukun','lol wildrift.list'),
 'Speedtest':('Jia-6/NET','Ruleset/SpeedTest.list'), 'KoreanLive':('Jia-6/NET','Ruleset/WinkTV.list')}
states={'recent-180d':'近180天有文件提交','older-than-180d':'超过180天未改；不等于失效','historical-pin':'历史快照，非持续更新源','unavailable-404':'404，不自动使用','activity-unverified':'活跃度待核验'}
def label(r):
    return f"[{r['repository']} / {Path(r['path']).name}]({r['url']})；{r.get('last_file_commit_date','未确认')[:10]}；{states[r['status']]}"
rows=[]; table=[]
for service,policy,_ in SERVICES:
    alternatives=[]
    if service in ('TikTok','DouYin'):
        repo,path=('Semporia/TikTok-Unlock','Quantumult-X/TikTok.list') if service=='TikTok' else ('Semporia/Quantumult-X','Filter/DouYin.list')
        primary=find('blackmatrix7/ios_rule_script',f'rule/QuantumultX/{service}/{service}.list')
        alternatives=[find(repo,path)]
        note='用户确认blackmatrix为基线，保留人工补充/排除；Semporia仅对照，不整表替换或自动合并。'
    elif service=='Pornhub':
        primary=find('Yooukun/Yooukun','pornhub.list');note='自维护；无已确认的外部更新源。'
    elif service=='KoreanLive':
        primary=None;note='官方迁移公告＋人工维护；仅核心域名，播放CDN待请求记录。'
    else:
        primary=find('blackmatrix7/ios_rule_script',f'rule/QuantumultX/{service}/{service}.list')
        note='保留本地补充/排除；无差异不强行更新。'
    alternatives += [find('ACL4SSR/ACL4SSR',p) for p in fallback.get(service,[])]
    if service in special: alternatives.append(find(*special[service]))
    if service=='GlobalMedia': alternatives.append(find('Jia-6/NET','Ruleset/Proxyown.list'))
    if service=='Claude':note+=' Claude官方网络域名资料是人工补充证据，不是自动订阅。'
    if service=='Riot':note+=' 旧Wild Rift列表仅单游戏证据，不能代表全Riot。'
    if service in ('SteamCN','GlobalMedia','Lan'):note+=' 旧综合列表仅供相关条目参考，不整表替换。'
    if service=='NetEaseMusic':note+=' GeQ1an的master为历史分支，默认分支已变更，不视为活跃维护。'
    row={'service':service,'policy':policy,'primary':primary,'alternatives':alternatives,'notes':note,'local_additions':f'sources/local/{service}.list' if (ROOT/f'sources/local/{service}.list').exists() else None}
    rows.append(row)
    table.append(f"| {policy} / `{service}.list` | {label(primary) if primary else 'PandaTV/WinkTV 官方迁移资料；人工维护'} | {'<br>'.join(label(r) for r in alternatives) or '暂无已收录备选；需用户授权扩展来源'} | {note} |")
(ROOT/'sources/update-registry.json').write_text(json.dumps({'checked_at':audit['checked_at'],'lists':rows,'generated_priority':'Priority.list is derived, not fetched'},ensure_ascii=False,indent=2)+'\n')
header='''# OX 分流更新来源维护表

核验时间：'''+audit['checked_at']+'''

覆盖26个服务列表＋1个自动生成的Priority列表。所有来源均来自已收录作者、历史配置或用户明确指定；未扩展到新作者。

“近180天”仅为文件提交活跃度指标，不是有效性结论。较旧文件仍可能可用；仓库有提交也不代表每份列表有更新。
原始URL、内容哈希、文件提交日期及证据方式见 `source-activity.json`；机器映射见 `update-registry.json`。
历史固定提交只用于追溯；404来源禁用。备用列表仅作候选，不能无审核替换首选。

| 策略 / 发布文件 | 首选及核验状态 | 已收录备选 | 维护约束 |
|---|---|---|---|
'''
footer='''

## Priority 与 Semporia 对照

- `Priority.list` 由sources/local/Priority.list的人工例外与跨集合具体域名例外生成；不能直接编辑生成文件。
- snssdk.com在TikTok/抖音上游都有收录，是共享域名。人工例外让其优先直连，避免落到GlobalMedia；不代表该域名属于抖音独占，设备仍需验证。
- TikTok 22条、抖音9条继续使用blackmatrix基线和原人工决定；不引入Semporia关键词或User-Agent，不改变MITM。
- sources/local/DouYin.list与exclusions.json内决定继续生效。capcut/trae等不归TikTok，西瓜/头条保持国内服务规则归属。
- Semporia固定对照见selected-sources.json，原文存selected/；文件名为历史命名，不表示被构建采用。构建不读取这些对照数据。
- 两个Semporia源仓库根目录未发现独立LICENSE，不为其重新声明GPL授权，来源权利归原作者。

## “更新OX分流策略”的执行约定

1. 检查Git状态、快进拉取；按本表核查指定文件变化，不仅检查仓库日期。
2. 优先已有来源中仍有维护的相关文件；TikTok/抖音以blackmatrix为基线，Semporia仅作对照，不因作者名或规则数量盲目替换。
3. 在候选目录抓取完整提交SHA与哈希，保留人工决定；备选新增条目须核实归属后写入local，不自动拼接所有列表。
4. 运行build、validate、test_rules、test_selected_sources，检查增删、关键词扩大匹配、共享域名和策略归属。
5. 明显删除、来源失效、行为冲突或必须改主配置时暂停；安全差异经审核后提交发布。失败不得覆盖线上。
6. 现有来源解决不了的列出缺口，等待用户授权寻找新资料或提供请求记录；不擅自扩展来源。
7. 不改节点订阅、MITM、脚本、策略组选项。手机手动更新资源后做真实请求验收；回退使用新提交恢复旧规则。

没有后台定时更新。audit_rule_sources.py会写本地审计及selected对照快照，必须在干净候选工作区运行并审阅差异，不会自动推送。
'''
(ROOT/'sources/UPDATE-SOURCES.md').write_text(header+'\n'.join(table)+footer)
print('Generated 26 service mappings + Priority maintenance instructions.')
