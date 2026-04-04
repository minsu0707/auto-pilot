# Auto Pilot

正式文档和插件主体现在都在仓库根目录下。

- 完整文档: [README.md](./README.md)
- 详细使用指南: [docs/06-usage-guide.md](./docs/06-usage-guide.md)
- 한국어: [README.ko.md](./README.ko.md)
- 日本語: [README.ja.md](./README.ja.md)
- 中文: [docs/i18n/zh.md](./docs/i18n/zh.md)
- العربية: [docs/i18n/ar.md](./docs/i18n/ar.md)

## 一行安装

当前 stable `v0.1.1` 依赖 `curl`、`tar` 和 `python3`，并继续使用已经发布的 slash command 入口。

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

如果你要提前验证下一条 stable release 线，再显式安装 `develop`：

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/develop/install.sh | env -u NO_COLOR bash
```

当前已发布版本是 `v0.1.1`。只有在明确测试未发布行为时才使用 `develop`。下一个 stable tag 发布时，要一起更新 stable install URL、运行示例和 baked-in stable ref。

## 在 Codex 中运行

### Stable `v0.1.1`

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

stable 的公开主入口是 `/auto-pilot:autopilot`。安装后请重启一次 Codex，让 slash command 正常加载。

安装一次后，新项目会自动进入 intake，已有项目会自动走 resume 流程。重启后也可以使用自然语言快捷写法：

```text
Build a budgeting app for freelancers ap
```

### Preview on `develop`

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

只有在安装了 `develop` 之后才使用 `$auto-pilot`。重启后也可以使用自然语言快捷写法：

```text
Build a diary app my friend Dohyeon would love ap
```

下面的内容描述的是 `main` 上当前仓库工作流，也就是下一次 stable release 将要包含的行为。

当前 `main` 还新增了 upfront integration setup：如果项目需要 Google OAuth、Supabase 等外部集成，Auto Pilot 会在执行前一次性收集缺失的 `.env` 值，并把状态写入 `autopilot/secrets-status.json`。
