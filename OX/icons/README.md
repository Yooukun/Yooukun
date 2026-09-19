# 策略组图标

policies.json 保存策略名称与自有镜像地址，不包含私人订阅、节点或证书。
本次镜像 Orz-3 mini Color/Alpha 全部 753 张 PNG，Qure IconSet 全部 1347 张 PNG，共 2100 张。包含当前未使用的资源，不包含上游其他无关目录。
预览和复制地址见 [图标索引](INDEX.md)。mini/Color/ 为彩色版，mini/Alpha/ 为透明版；qure/ 保留 IconSet 内目录层级。文件名添加源路径哈希短后缀，避免 macOS 大小写不敏感文件系统将 Steam.png/steam.png 等不同图标互相覆盖。

旧配置的 16 项对应关系已按当前策略名称恢复。其余策略补充同系列图标。
Claude、Riot、网易云、Pornhub、瑞士、荷兰、印度已更换为 custom/ 中的准确标识适配图；抖音与 TikTok 仍使用同一音乐标识。
custom/ 中新增 7 张 108x108 RGBA PNG；官方品牌素材来源、保留的原文件及操作见 custom/README.md 与 custom/manifest.json。映射已增加 mono，共 42 项。

来源：
- Orz-3 mini：https://github.com/Orz-3/mini 。原 README 见 mini/UPSTREAM-README.md；明确说明可用于策略图标，未发现通用开源许可证。本镜像不声明获得额外版权授权。
- Koolson Qure：https://github.com/Koolson/Qure 。原 README 见 qure/UPSTREAM-README.md；作者要求转载注明出处、禁止商业用途，图标权利归原作者。
- 图标不适用本仓库规则文件的 GPL 授权；本镜像不会扩大使用权限。保留署名、来源说明；如权利人提出问题，应核实处理。

图片仅用于界面展示，不参与分流。运行时只引用本仓库，原作者删除资源不会影响已镜像版本；仍依赖本仓库及 GitHub 可访问。
更新远程分流资源不会更新本地策略的 img-url，手机需合并新的 [policy] 内容。

libraries.json 记录两套库的固定提交；manifest.json 记录原始固定链接、相对路径、SHA-256 与字节数；original-policies.json 保留基础来源映射，overrides.json 固定自定义图标，防止更新来源库后退回旧占位图。
新增策略可从 INDEX.md 复制现有链接写入 policies.json，或直接追加到策略的 img-url。更新来源库需要明确运行 tools/mirror_icons.py，不自动跟随上游删除文件。
