# 发布状态

更新：用户补充权限后，公开仓库推送成功。tools/verify_published.py 检查 33 个运行时资源，全部匿名下载成功且 SHA-256 与本地一致。
公开仓库新增 OX/ 目录并清理五个根目录旧规则；历史可从原提交恢复，未强制改写历史。
已通过 export --remote-ready 生成正式个人远程配置，个人订阅与 DNS 仅保存在本地交付文件。

- Git：公开目录推送成功；旧 HBO.list、lol wildrift.list、paypal.list、pornhub.list、steam.list 已从当前分支删除，历史保留。
- 原维护仓库 yoh_96 保持私有；经用户确认，公共分发改用 Yooukun/Yooukun 的 yoh_96 分支 OX/ 目录。
- 未修改仓库可见性，未将 GitHub 访问凭证写入配置。
- 手机首次使用：个人内置规则版或远程规则版；可选脚本支持公开 OX 订阅或本地 Scripts。
- 手机远程更新：规则及脚本地址统一指向公开目录，不需要 GitHub 登录凭据。
- 代码静态检查与合成测试通过；设备导入、实时节点、实际请求命中及 MITM 行为待验证。
