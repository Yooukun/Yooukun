# 自定义适配图标

7 张 108x108 RGBA PNG，与现有 mini 系列尺寸一致；透明圆角、保持标识比例。尺寸是本项目选择，不宣称圈叉只接受此尺寸。图标版权和商标归原权利人，仅用于服务识别，不代表官方授权或背书。

- Claude：从 https://claude.com/ 的官方内嵌 wordmark SVG 提取未改动的星形 path，按原色渲染，留白放入圆角底板；原 SVG 和 PNG 保留在 sources/。不用低清 favicon 放大版本。
- Riot：使用 https://www.riotgames.com/ 页面引用的官方 apple-touch-icon（180x180），保留拳头图形，等比缩小并圆角化；来源地址见 manifest.json。
- 网易云：使用已镜像 Orz-3 mini 的 neteasemusic 正式音乐标识，而非 Netease_Music_Unlock 解锁图。
- Pornhub：使用已镜像 Qure Color/Pornhub_2 的品牌文字标识，加深色底板，不使用电视图形占位图。
- 印度：使用 Qure Color/India 的三色旗与法轮，不使用 IN 字母图。
- 瑞士、荷兰：基于国旗基本几何图案绘制的圆角 UI 标识，不是官方制旗规范图。

可复现步骤：tools/fetch_claude_mark.py 保存官方向量；用 sharp 将 sources/claude-mark.svg 渲染为 sources/claude-vector.png；用具备 Pillow 的 Python 运行 tools/build_custom_icons.py，然后 tools/refresh_icon_catalog.py。重新构建不从网络自动改变节点或分流。
