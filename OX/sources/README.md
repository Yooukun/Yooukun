# 规则来源与维护决定

初版以 blackmatrix7/ios_rule_script 固定提交建立基线，完整来源 URL、SHA-256 在 manifest.json。
原文和 GPL-2.0 许可保存在 upstream/。发布规则经过格式统一、策略绑定、跨集合去重和本地筛选，
不是逐条重新发现的原创域名，也不是所有域名均已实机验证。

手机只读取 OX/rules，今后上游变化不会自动覆盖这些文件。
local/ 放经过说明的人工补充；exclusions.json 放明确不应归到特定服务的域名。
修改 local/ 或 exclusions.json 后，执行 build、validate、test_rules 再审阅 diff。
不要直接编辑生成的 rules/；否则下次构建会覆盖修改。

初版决定：

- 移除 host-keyword、user-agent、host-wildcard 候选，保留明确域名/IP 规则；原始候选仍在 upstream。
- 移除部分共享基础服务的整体归属（如 sentry.io、stripe.com、auth0.com）。它们仍可经其他匹配或兜底访问。
- OpenAI/Claude 不继承未经核实的共享 IP、ASN 分配。
- TikTok 排除国内 snssdk 及 CapCut/Trae 等其他业务整体归属；抖音排除西瓜、头条等其他业务。
- Riot 排除部分疑似辅助工具、拼写近似或不相关域名；其他条目仍为来源基线，不代表逐一完成归属审查。
- Priority.list 显式列出跨集合具体域名例外，按域名层级从具体到宽泛排序，保留每条目标策略。
  此文件不得使用 force-policy。仍需在 Quantumult X 请求记录验证资源优先级与实际命中。
- 国内规则保留 ChinaMax 基线，数量较大；未添加 geoip CN 的广泛覆盖。

人工补充的证据：

- Claude 应用域名：https://support.claude.com/en/articles/13198485-enforce-network-level-access-control-with-tenant-restrictions
- 抖音入口：https://www.douyin.com/
- 成人站点：用户自己的 Yooukun/Yooukun 固定提交 1bbe8254bb16bee92376e7de567ccfd163cd7e1d 中 pornhub.list。
- 韩国直播：https://m.winktv.co.kr/policy/claim 官方公告说明 2025-06-02 WinkTV 停服并转至 PandaTV。
  仅保留迁移入口和新平台核心域名，播放 CDN 尚待实际访问记录补充。

旧配置引用检查见 legacy-link-audit.json：只检查公开规则/脚本链接，不请求私人节点订阅、DoH 或证书。
HTTP 200 仅说明当次可以读取，不说明规则、脚本或域名当前业务有效。

更新上游时使用完整提交 SHA，把 snapshot 输出到 candidate/，build --root candidate 后运行 compare.py。
候选为空、抓取失败或删除超阈值时不得晋升。无报警也要审阅；工具不会自动推送、自动启用。
