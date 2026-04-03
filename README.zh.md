# Auto Pilot

正式文档和插件主体现在都在仓库根目录下。

- 完整文档: [README.md](./README.md)
- 详细使用指南: [docs/06-usage-guide.md](./docs/06-usage-guide.md)
- 한국어: [README.ko.md](./README.ko.md)
- 日本語: [README.ja.md](./README.ja.md)
- 中文: [docs/i18n/zh.md](./docs/i18n/zh.md)
- العربية: [docs/i18n/ar.md](./docs/i18n/ar.md)

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

稳定安装请使用 `v0.1.1`。stable release tag 应当始终安装它自己对应的版本；如果你想提前验证即将进入下一个 stable tag 的改动，再使用 `develop`。

## 在 Codex 中运行

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

公开主入口是 `$auto-pilot`。安装后请重启一次 Codex，让 skill 正常加载。

安装一次后，新项目会自动进入 intake，已有项目会自动走 resume 流程。重启后也可以使用自然语言快捷写法：

```text
Build a diary app my friend Dohyeon would love ap
```
