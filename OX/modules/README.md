# MITM、脚本与重写

主配置保留 MITM、rewrite_local、task_local；两条实验重写订阅已列出，默认 enabled=false。
这不是已验证的脚本增强版。已完成语法检查和人工构造响应测试；当前微博、Netflix 接口及设备证书未实测。

| 模块 | 当前交付 | 使用边界 |
|---|---|---|
| 微博开屏、信息流 | weibo.conf；scripts/wb_launch.js、wb_ad.js | 保留旧功能；增加同步异常原样放行；接口改变可能使功能不生效 |
| Netflix 评分 | netflix-rating.conf；scripts/nf_rating.js | 保留旧请求/响应挂钩；运行版删除公共 API key 池，需用户自己的 OMDb key |
| TikTok 地区修改 | tiktok-legacy.txt | 仅注释归档；旧规则缺少严格域名限制，未证明现版本有效，不启用 |
| 通用重定向 | 旧地址审计记录 | 原源 404；没有证据支持恢复全部行为，首版不启用 |
| 网易云解锁 | 网易云独立分流策略 | 未取得有效解锁节点，未宣称实现解锁 |
| 定时任务 | task_local 入口 | 旧配置无有效任务，未新增后台任务 |

## 在手机使用

1. 先导入个人配置并验证基本网络与分流。
2. 在 Quantumult X 中生成、安装并信任新证书；证书和密码留在设备中。
3. 只启用需要的一个实验模块，检查其访问记录和实际效果。MITM 总开关也需在设备中确认。
4. 保持 skip_validating_cert=false。不要对 AI、支付、所有网站设置通配 MITM。
5. 出现登录、响应或播放异常时，关闭对应模块，不必停用整个代理。

远程模块仅从 OX 下载脚本。需要本地使用时，将 scripts/ 下对应 JS 放到 Quantumult X/Scripts，
把 *-local.txt 的内容分别合并到对应配置段；不要同时启用同一功能的本地规则和远程模块。
hostname 合并时保留已有必要域名，不复制旧证书。

Netflix 脚本会请求 OMDb、豆瓣获取评分，所以评分数据本身仍依赖外部服务。
运行版使用设备偏好键 OX_OMDB_API_KEY；应在设备本地通过 $prefs.setValueForKey 写入自己的 key，
不要写进 Git 或公共脚本。无 key 时响应阶段原样放行；原始接口和数据形状仍需实测。
vendor/ 保存有 GPL-3.0 许可的原始源码供审阅，包含上游历史公共 key 池；主配置不引用 vendor 版本。

## 许可与变更

原作者 yichahucha，来源和不可变提交见 manifest.json，GPL-3.0 正文见 vendor/yichahucha/LICENSE。
scripts/ 为 OX 修改版：同步异常透传、Netflix 移除公共 key 池、使用私人偏好键、修正包装后的同名声明。
原始源代码和变更工具一并提供；不声称为全新原创代码。
