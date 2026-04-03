# Auto Pilot

> 一次提问，锁定简报，然后持续构建。

[English](../../README.md) | [한국어](./ko.md) | [日本語](./ja.md) | 中文 | [العربية](./ar.md)

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

稳定安装请使用 `v0.1.1`。stable release tag 应当始终安装它自己对应的版本；如果你想提前验证即将进入下一个 stable tag 的改动，再使用 `develop`。

## 在 Codex 中运行

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

公开主入口是 `$auto-pilot`。
安装后请重启一次 Codex，让 skill 被正确加载。
安装一次后，新项目会自动进入 intake，已有项目会自动走 resume 流程。
重启后，也可以使用 `Build a diary app my friend Dohyeon would love ap` 这样的自然语言快捷写法。

此文件夹是 `Auto Pilot` Codex 插件的正式根目录。该插件会把 `Build me a budgeting app` 这样的短请求转换为 intake-first 执行工作流。

Auto Pilot 不会每走几步就停下来重新追问上下文，而是会：

- 一次性收集最小必要输入
- 保存可复用的项目契约
- 生成 spec、progress、next-step 和 runtime state 文件
- 让下一次 Codex 会话也能从中断位置继续

## Why It Exists

短提示很方便，但通常不足以支撑长时间自治工作。

Auto Pilot 通过以下能力填补这个缺口：

- 一次只问一个问题的 intake
- 明确的 definition of done
- 默认 blocker policy
- 可恢复的项目状态

目标很简单：少 babysitting，多推进。

## What It Does

- 把简短项目请求转换成结构化 intake 会话
- 使用 `1. Question` / `Questions remaining: N` UX 模式
- 写入 `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json`
- 对 user-facing 项目还会生成 `docs/design.md`，让 UI 从明确的设计简报开始，而不是 generic 默认布局
- 保留足够状态，让下一次 Codex 会话从停止处继续
- 设计说明表示会生成基于 curated references 的设计简报，并不假装已经完成了广泛网页调研
- 将正式插件代码、文档和安装逻辑统一放在仓库根目录下

## Quick Start

启动新的 intake 会话：

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a diary app my friend Dohyeon would love"
```

回答当前问题：

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "想要一个温暖、私密、可以每天装饰的日记应用的年轻用户"
```

查看当前模式和状态：

```bash
python3 scripts/autopilot.py status \
  --workspace /tmp/my-project
```

最后一个回答提交后，Auto Pilot 会生成以下文件：

- `docs/spec.md`
- `docs/design.md`（仅限 user-facing 项目）
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 一个简短提示启动 intake。
2. Auto Pilot 一次只问一个问题。
3. 回答会被归一化为项目契约。
4. 对 user-facing 项目，还会根据 theme、vibe 和 design direction 生成 `docs/design.md`。
5. 为后续执行和恢复创建 runtime state。
6. Codex 不需要重新摸索上下文，直接从保存的文件继续。

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/05-how-it-works.md`: 用图示整理 intake、state 和 resume 流程
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: secondary plugin command entry point
- `skills/auto-pilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates
- `install.sh`: canonical installer
- `uninstall.sh`: canonical uninstaller

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Usage

可以这样发起请求：

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`
- `Build a diary app my friend Dohyeon would love ap`

新项目的 intake 遵循以下 UX：

- 每次只显示一个问题
- 使用 `1. Question` 格式
- 下一行显示 `Questions remaining: N`
- 最后一个回答后总结契约，并开始 spec lock 与执行

底层脚本仍然可用：

- `init_intake.py`
- `record_answer.py`
- `status.py`

## Current Status

此仓库根目录就是插件根目录、文档根目录和安装脚本的基准位置。

面对普通用户，推荐流程是先用 one-line installer 安装，重启一次 Codex，再在 Codex 中使用 `$auto-pilot`。
