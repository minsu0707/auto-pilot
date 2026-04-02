# Auto Pilot

> 一次提问，锁定简报，然后持续构建。

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md) | 中文 | [العربية](./README.ar.md)

## 在 Codex 中立即开始

```bash
/auto-pilot:autopilot Build a budgeting app for freelancers
/auto-pilot:autopilot-intake Build a budgeting app for freelancers
/auto-pilot:autopilot-resume Continue this project with Auto Pilot
```

Auto Pilot 是一个本地 Codex 插件，可以把 `Build me a budgeting app` 这样的简短请求转换为 intake-first 执行流程。

Auto Pilot 不会每走几步就停下来重新追问上下文，而是会：

- 一次性收集最少必需输入
- 保存可复用的项目契约
- 生成 spec、progress、next-step 和 runtime state 文件
- 给 Codex 提供可恢复的长时执行结构

## Why It Exists

简短提示词虽然方便，但通常不足以支撑长时间自治执行。

Auto Pilot 通过以下能力补足这个缺口：

- 一次一个问题的 intake
- 明确的 definition of done
- blocker policy
- 可恢复的 project state

目标很简单：减少 babysitting，增加持续推进。

## What It Does

- 将简短的项目请求转换为结构化 intake 会话
- 使用 `1. Question` / `Questions remaining: N` UX
- 写入 `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json` 和 `autopilot/blockers.json`
- 保留足够状态，让下一次 Codex 会话从中断点继续
- 自带插件清单和 repo-local marketplace wiring

## Quick Start

启动新的 intake 会话：

```bash
python3 auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

回答当前问题：

```bash
python3 auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

查看当前模式和状态：

```bash
python3 auto-pilot/scripts/autopilot.py status \
  --workspace /tmp/my-project
```

最后一个回答提交后，Auto Pilot 会生成：

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 简短提示触发 intake。
2. Auto Pilot 一次只问一个问题。
3. 回答会被规范化为项目契约。
4. 系统会为后续执行和恢复创建 runtime state。
5. Codex 可以直接从保存的文件继续，而不必重新推断上下文。

## Repository Layout

- [auto-pilot](./auto-pilot): plugin root
- [auto-pilot/.codex-plugin/plugin.json](./auto-pilot/.codex-plugin/plugin.json): plugin manifest
- [auto-pilot/scripts](./auto-pilot/scripts): CLI and helper scripts
- [auto-pilot/skills](./auto-pilot/skills): orchestration, intake, and resume skills
- [.agents/plugins/marketplace.json](./.agents/plugins/marketplace.json): repo-local marketplace config

## Current Status

当前仓库主要聚焦于：

- intake UX
- spec 与 state bootstrapping
- resume-friendly file structure
- multilingual README entry points

下一个最自然的步骤是提供 one-command installer，将插件自动注册到 home-level marketplace。
