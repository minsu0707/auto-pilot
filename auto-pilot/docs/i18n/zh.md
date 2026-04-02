# Auto Pilot Docs

> 一次提问，锁定简报，然后持续构建。

[English](../../README.md) | [한국어](./ko.md) | [日本語](./ja.md) | 中文 | [العربية](./ar.md)

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## 在 Codex 中运行

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

公开入口只需要使用 `/auto-pilot:autopilot`。
安装后请重启一次 Codex，让 slash command 被正确加载。
安装一次后，新项目会自动进入 intake，已有项目会自动走 resume 流程。

此文件夹包含 `Auto Pilot` Codex 插件的初始文档包。该插件会把简短的项目请求转换为 intake-driven 的长时间自治执行工作流。

## Files

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: public slash command entry point
- `skills/autopilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Current Status

此文件夹就是 plugin root。repo-local marketplace 通过 [marketplace.json](../../../.agents/plugins/marketplace.json) 连接。

## Usage

可以这样发起请求：

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`

新项目的 intake 遵循以下 UX：

- 每次只显示一个问题
- 使用 `1. Question` 格式
- 下一行显示 `Questions remaining: N`
- 最后一个回答后总结契约，并开始 spec lock 与执行

## Script Example

```bash
python3 scripts/autopilot.py start \
  --workspace /path/to/project \
  --prompt "Build a budgeting app for freelancers"

python3 scripts/autopilot.py answer \
  --workspace /path/to/project \
  --text "Freelancers and solo business owners"

python3 scripts/autopilot.py status \
  --workspace /path/to/project
```

最后一个回答提交后，会生成以下文件：

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

底层脚本仍然可用：

- `init_intake.py`
- `record_answer.py`
- `status.py`

面对普通用户，推荐流程是先用 one-line installer 安装，重启一次 Codex，再在 Codex 中使用 `/auto-pilot:autopilot`。
