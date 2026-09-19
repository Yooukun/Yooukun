# Riot 域名覆盖边界

本次仅检查既有规则，不扩展游戏端点，不将 Riot 策略更名为单个游戏。
依据官方产品入口 https://www.riotgames.com/en 与本地顺序匹配测试：

| 测试域名 | 当前结果 |
|---|---|
| www.leagueoflegends.com | Riot游戏 |
| wildrift.leagueoflegends.com | Riot游戏 |
| teamfighttactics.leagueoflegends.com | Riot游戏 |
| playvalorant.com | Riot游戏 |
| 2xko.riotgames.com | Riot游戏 |
| playruneterra.com | 兜底策略 |

现有规则涵盖多个产品官网域名及 riotgames.com/riotcdn.net 等共用服务，不只 Wild Rift。但不能称为全 Riot 游戏完整覆盖：除已知网站域名缺口外，游戏连接可能使用其他 CDN、IP 直连、UDP 及各地区发行服务，均未实机验证。域名命中不等于游戏所有网络流量已覆盖，更不等于游戏加速或解锁。
