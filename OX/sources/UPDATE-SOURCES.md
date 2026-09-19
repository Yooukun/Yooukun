# OX 分流更新来源维护表

核验时间：2026-09-19T11:03:03.562147+00:00

覆盖26个服务列表＋1个自动生成的Priority列表。所有来源均来自已收录作者、历史配置或用户明确指定；未扩展到新作者。

“近180天”仅为文件提交活跃度指标，不是有效性结论。较旧文件仍可能可用；仓库有提交也不代表每份列表有更新。
原始URL、内容哈希、文件提交日期及证据方式见 `source-activity.json`；机器映射见 `update-registry.json`。
历史固定提交只用于追溯；404来源禁用。备用列表仅作候选，不能无审核替换首选。

| 策略 / 发布文件 | 首选及核验状态 | 已收录备选 | 维护约束 |
|---|---|---|---|
| 局域网 / `Lan.list` | [blackmatrix7/ios_rule_script / Lan.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Lan/Lan.list)；2026-04-13；近180天有文件提交 | [ACL4SSR/ACL4SSR / LocalAreaNetwork.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/LocalAreaNetwork.list)；2025-12-06；超过180天未改；不等于失效<br>[ACL4SSR/ACL4SSR / UnBan.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/UnBan.list)；2025-08-10；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 旧综合列表仅供相关条目参考，不整表替换。 |
| OpenAI / `OpenAI.list` | [blackmatrix7/ios_rule_script / OpenAI.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/OpenAI/OpenAI.list)；2025-06-17；超过180天未改；不等于失效 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 |
| Claude / `Claude.list` | [blackmatrix7/ios_rule_script / Claude.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Claude/Claude.list)；2025-06-17；超过180天未改；不等于失效 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 Claude官方网络域名资料是人工补充证据，不是自动订阅。 |
| Steam下载 / `SteamCN.list` | [blackmatrix7/ios_rule_script / SteamCN.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/SteamCN/SteamCN.list)；2025-06-17；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / Download.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Download.list)；2024-06-30；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 旧综合列表仅供相关条目参考，不整表替换。 |
| Steam商店 / `Steam.list` | [blackmatrix7/ios_rule_script / Steam.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Steam/Steam.list)；2025-06-17；超过180天未改；不等于失效 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 |
| PayPal / `PayPal.list` | [blackmatrix7/ios_rule_script / PayPal.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/PayPal/PayPal.list)；2025-06-17；超过180天未改；不等于失效 | [Yooukun/Yooukun / paypal.list](https://raw.githubusercontent.com/Yooukun/Yooukun/1bbe8254bb16bee92376e7de567ccfd163cd7e1d/paypal.list)；未确认；历史快照，非持续更新源 | 保留本地补充/排除；无差异不强行更新。 |
| Telegram / `Telegram.list` | [blackmatrix7/ios_rule_script / Telegram.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Telegram/Telegram.list)；2025-12-21；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / Telegram.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Telegram.list)；2024-09-16；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| X推特 / `Twitter.list` | [blackmatrix7/ios_rule_script / Twitter.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Twitter/Twitter.list)；2025-12-21；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / Twitter.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Twitter.list)；2024-12-14；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| YouTube / `YouTube.list` | [blackmatrix7/ios_rule_script / YouTube.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/YouTube/YouTube.list)；2025-06-17；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / YouTube.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/YouTube.list)；2026-01-24；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| Netflix / `Netflix.list` | [blackmatrix7/ios_rule_script / Netflix.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Netflix/Netflix.list)；2025-06-17；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / Netflix.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Netflix.list)；2026-01-24；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| Disney / `Disney.list` | [blackmatrix7/ios_rule_script / Disney.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Disney/Disney.list)；2025-12-21；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / DisneyPlus.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/DisneyPlus.list)；2026-01-24；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| HBO / `HBO.list` | [blackmatrix7/ios_rule_script / HBO.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/HBO/HBO.list)；2025-06-17；超过180天未改；不等于失效 | [Yooukun/Yooukun / HBO.list](https://raw.githubusercontent.com/Yooukun/Yooukun/585d5c724900614192585b0936cb6f760bf0e3ce/HBO.list)；2022-06-24；历史快照，非持续更新源 | 保留本地补充/排除；无差异不强行更新。 |
| TikTok / `TikTok.list` | [blackmatrix7/ios_rule_script / TikTok.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/TikTok/TikTok.list)；2025-12-21；超过180天未改；不等于失效 | [Semporia/TikTok-Unlock / TikTok.list](https://raw.githubusercontent.com/Semporia/TikTok-Unlock/master/Quantumult-X/TikTok.list)；2022-06-23；超过180天未改；不等于失效 | 用户确认blackmatrix为基线，保留人工补充/排除；Semporia仅对照，不整表替换或自动合并。 |
| 哔哩哔哩 / `BiliBili.list` | [blackmatrix7/ios_rule_script / BiliBili.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/BiliBili/BiliBili.list)；2025-06-17；超过180天未改；不等于失效 | [ACL4SSR/ACL4SSR / Bilibili.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Bilibili.list)；2026-01-24；超过180天未改；不等于失效<br>[ACL4SSR/ACL4SSR / BilibiliHMT.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/BilibiliHMT.list)；2023-03-23；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| 网易云音乐 / `NetEaseMusic.list` | [blackmatrix7/ios_rule_script / NetEaseMusic.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/NetEaseMusic/NetEaseMusic.list)；2025-06-17；超过180天未改；不等于失效 | [GeQ1an/Rules / Netease Music.list](https://raw.githubusercontent.com/GeQ1an/Rules/master/QuantumultX/Filter/Optional/Netease%20Music.list)；2022-01-25；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 GeQ1an的master为历史分支，默认分支已变更，不视为活跃维护。 |
| 抖音 / `DouYin.list` | [blackmatrix7/ios_rule_script / DouYin.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/DouYin/DouYin.list)；2025-06-17；超过180天未改；不等于失效 | [Semporia/Quantumult-X / DouYin.list](https://raw.githubusercontent.com/Semporia/Quantumult-X/master/Filter/DouYin.list)；2025-03-06；超过180天未改；不等于失效 | 用户确认blackmatrix为基线，保留人工补充/排除；Semporia仅对照，不整表替换或自动合并。 |
| 微博 / `Weibo.list` | [blackmatrix7/ios_rule_script / Weibo.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Weibo/Weibo.list)；2025-06-17；超过180天未改；不等于失效 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 |
| Riot游戏 / `Riot.list` | [blackmatrix7/ios_rule_script / Riot.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Riot/Riot.list)；2025-06-17；超过180天未改；不等于失效 | [Yooukun/Yooukun / lol wildrift.list](https://raw.githubusercontent.com/Yooukun/Yooukun/271169a76d244087c64f485b7f79f8a32cc133e5/lol%20wildrift.list)；未确认；历史快照，非持续更新源 | 保留本地补充/排除；无差异不强行更新。 旧Wild Rift列表仅单游戏证据，不能代表全Riot。 |
| 测速 / `Speedtest.list` | [blackmatrix7/ios_rule_script / Speedtest.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Speedtest/Speedtest.list)；2025-06-17；超过180天未改；不等于失效 | [Jia-6/NET / SpeedTest.list](https://raw.githubusercontent.com/Jia-6/NET/main/Ruleset/SpeedTest.list)；未确认；404，不自动使用 | 保留本地补充/排除；无差异不强行更新。 |
| Pornhub / `Pornhub.list` | [Yooukun/Yooukun / pornhub.list](https://raw.githubusercontent.com/Yooukun/Yooukun/1bbe8254bb16bee92376e7de567ccfd163cd7e1d/pornhub.list)；未确认；历史快照，非持续更新源 | 暂无已收录备选；需用户授权扩展来源 | 自维护；无已确认的外部更新源。 |
| 韩国直播 / `KoreanLive.list` | PandaTV/WinkTV 官方迁移资料；人工维护 | [Jia-6/NET / WinkTV.list](https://raw.githubusercontent.com/Jia-6/NET/main/Ruleset/WinkTV.list)；未确认；404，不自动使用 | 官方迁移公告＋人工维护；仅核心域名，播放CDN待请求记录。 |
| Apple / `Apple.list` | [blackmatrix7/ios_rule_script / Apple.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Apple/Apple.list)；2026-09-17；近180天有文件提交 | [ACL4SSR/ACL4SSR / Apple.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Apple.list)；2023-07-03；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |
| Microsoft / `Microsoft.list` | [blackmatrix7/ios_rule_script / Microsoft.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Microsoft/Microsoft.list)；2025-12-21；超过180天未改；不等于失效 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 |
| Google / `Google.list` | [blackmatrix7/ios_rule_script / Google.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Google/Google.list)；2026-05-11；近180天有文件提交 | 暂无已收录备选；需用户授权扩展来源 | 保留本地补充/排除；无差异不强行更新。 |
| 其他海外媒体 / `GlobalMedia.list` | [blackmatrix7/ios_rule_script / GlobalMedia.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/GlobalMedia/GlobalMedia.list)；2026-09-13；近180天有文件提交 | [ACL4SSR/ACL4SSR / ProxyLite.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyLite.list)；2025-12-06；超过180天未改；不等于失效<br>[Jia-6/NET / Proxyown.list](https://raw.githubusercontent.com/Jia-6/NET/main/Ruleset/Proxyown.list)；未确认；404，不自动使用 | 保留本地补充/排除；无差异不强行更新。 旧综合列表仅供相关条目参考，不整表替换。 |
| 国内服务 / `ChinaMax.list` | [blackmatrix7/ios_rule_script / ChinaMax.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/ChinaMax/ChinaMax.list)；2026-09-17；近180天有文件提交 | [ACL4SSR/ACL4SSR / ChinaDomain.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list)；2025-12-06；超过180天未改；不等于失效<br>[ACL4SSR/ACL4SSR / ChinaCompanyIp.list](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaCompanyIp.list)；2025-03-29；超过180天未改；不等于失效 | 保留本地补充/排除；无差异不强行更新。 |

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
