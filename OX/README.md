# OX Quantumult X 自有配置与规则库

当前公开推送因权限 403 尚未完成，见 RELEASE_STATUS.md。个人远程导出默认带 .conf.template 后缀；
只有公开推送及 verify_published.py 校验通过后才使用 export --remote-ready。

由旧个人配置的服务覆盖与近期配置的节点分组整合而来。手机使用本仓库发布的规则，
上游只作为候选资料，由维护者决定何时更新。首版为待设备验收版本。

公开分发位置：Yooukun/Yooukun 仓库的 yoh_96 分支、OX/ 目录。
所有发布规则与脚本均使用该公开目录的 Raw 地址，私人订阅、DNS 和证书不进入公开仓库。
原 yoh_96 私有仓库继续保持私有，作为维护副本；公共仓库根目录的五份旧规则已由 OX/rules 替代，历史可从 Git 恢复。

## 文件

| 路径 | 用途 |
|---|---|
| profiles/quantumultx.conf | 公共模板，不含节点凭证；需填私人订阅才能使用 |
| rules/*.list | 发布规则，含服务集合和 Priority 具体域名例外 |
| sources/local/ | 人工补充，后续日常维护入口 |
| sources/exclusions.json | 自有排除决定 |
| sources/upstream/ | 固定上游原文及 GPL-2.0 许可 |
| sources/build-report.json | 规则数量、删除原因、重复及包含关系 |
| sources/legacy-link-audit.json | 旧公开链接的当次可用性检查 |
| modules/ | MITM、实验脚本模块、本地版本及许可说明 |
| tools/ | 构建、校验、更新比较和本地个人配置导出 |

## 配置设计

地区节点通过订阅标签 Kuromis 和中英文地区名称筛选；新增、改名节点无需逐个改配置。
地区组及服务组使用手动选择；故障切换为第一个可用节点，不是最快节点。
地区名与实际订阅不匹配时组可能为空，导入后必须检查。
OpenAI、Claude 各自只匹配新加坡、日本、美国节点，首次导入后分别选定实测可用节点。
地区匹配不保证服务可用性，未通过账号、出口和实际请求验证不能称为可用。
Apple、Microsoft、国内服务、抖音、微博、网易云、Steam 国内下载等优先直连；Steam 商店另行选择。
PayPal 默认直连，可手动固定节点；未知流量交给兜底策略。

公共模板提供通用 DoH 示例；个人导出保留近期配置的 DNS alias、自定义 DoH 和节点订阅，
避免未经验证地改变当前接入条件。并未认定这套私人 DNS 最优，也未测试其可达性。
默认不继承旧 Wi-Fi 暂停名单、资源转换器、外部图标、证书及跳过证书校验。
MITM 和脚本功能见 modules/README.md，两项实验模块默认关闭；旧 TikTok 重写仅归档。

## 本地校验

```sh
python3 tools/manage.py build
python3 tools/manage.py validate
python3 tools/test_rules.py
node tools/test_scripts.js
```

校验不需要订阅凭证，不发起节点连接。域名测试是顺序匹配模型，不能替代 Quantumult X 实机验证。

## 生成个人导入版

```sh
python3 tools/manage.py export --current /absolute/path/current.conf --out /absolute/path/private-output
```

生成两个权限为 0600 的文件：远程规则版引用公开 OX 目录；内置规则版直接包含同一套规则，便于首次导入和回退。
两者仍需节点订阅及网络，内置版只是不依赖规则下载。个人配置不能提交 Git。
首次导入可使用内置版；确认登录、DNS、AI、视频、下载和局域网正常后再切换远程版。

## 更新流程

```sh
python3 tools/manage.py snapshot --revision <完整40位提交SHA> --target candidate
python3 tools/manage.py build --root candidate
python3 tools/manage.py validate --root candidate
python3 tools/compare.py candidate
```

候选不会自动覆盖发布规则。来源失败或空文件会停止；明显删除会在比较时报警。
审阅本地排除、域名归属和差异后，才迁入 sources/upstream、manifest 并重新构建发布。
没有设置定时抓取、后台自动推送或 GitHub 定时任务。
日常也可只根据官方资料或设备请求记录维护 sources/local，不要求持续同步同一个上游。

## 设备验收与回退

保存近期原配置，在手机导入内置版后：

1. 检查节点订阅成功、地区组非空，OpenAI/Claude 分别选定节点。
2. 对照请求记录核实国内网页、AI 登录/对话、YouTube/Netflix 播放、TikTok/抖音分离。
3. 检查 Steam 商店和下载分别命中，Riot 登录与游戏 UDP、局域网访问正常。
4. 逐项开启实验 MITM 模块；Netflix 评分还需要私人 OMDb key。
5. 出现异常先关闭相应模块或切回原配置；Git 回退采用新提交恢复规则，不强制改写分支历史。

许可证按来源分开：规则衍生数据 GPL-2.0；yichahucha 脚本及修改版 GPL-3.0。
来源原文、许可证和修改工具均随库提供。其他新增维护工具和说明按 MIT 发布，见 LICENSE-tools。
