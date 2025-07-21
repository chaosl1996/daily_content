# 英语诗词 (English Poetry) 集成

Home Assistant 集成，同时提供每日诗词和英语名言功能。

## 功能特点
- 每日自动获取一首中文诗词
- 每日自动获取一句英语名言
- 可分别配置诗词和英语的更新频率
- 支持手动刷新数据

## 安装方法
1. 下载或克隆本仓库到 Home Assistant 的 `custom_components` 目录
2. 重启 Home Assistant
3. 在集成页面搜索 "英语诗词" 并添加

## 配置选项
- **诗词更新间隔**: 诗词内容的自动更新频率 (小时)
- **英语更新间隔**: 英语名言的自动更新频率 (小时)

## 实体说明
- **传感器**: 每日诗词、每日英语
- **按钮**: 诗词刷新、英语刷新

## 故障排除
- 确保网络连接正常
- 检查 API 密钥是否有效
- 查看 Home Assistant 日志获取详细错误信息

## 贡献
欢迎提交 PR 或 issue 到 [GitHub 仓库](https://github.com/chaosl1996/ha-english-poetry)

## 许可证
MIT