# auto-pilot

这是 `Auto Pilot` 的本地 Codex 插件仓库。

## 语言

- English: [`README.md`](/Users/minsu/Documents/Codex/README.md)
- 한국어: [`README.ko.md`](/Users/minsu/Documents/Codex/README.ko.md)
- 日本語: [`README.ja.md`](/Users/minsu/Documents/Codex/README.ja.md)
- 中文: `README.zh.md`
- العربية: [`README.ar.md`](/Users/minsu/Documents/Codex/README.ar.md)

## 内容

- [Auto Pilot 插件根目录](/Users/minsu/Documents/Codex/auto-pilot)
- [仓库本地 marketplace 配置](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- 用于 intake、状态生成和恢复流程的脚本

## 核心功能

- 将简短的项目请求转换为 intake 会话
- 每次只显示一个问题
- 使用 `1. Question` / `Questions remaining: N` 交互格式
- 在最后一个回答后自动生成 `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json` 和 `autopilot/blockers.json`
- 保留可在后续 Codex 会话中继续使用的状态结构
