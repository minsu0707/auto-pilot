# Auto Pilot

> 한 번 묻고, 브리프를 잠그고, 계속 만들어갑니다.

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](./README.md) | 한국어 | [日本語](./README.ja.md) | [中文](./README.zh.md) | [العربية](./README.ar.md)

Auto Pilot은 `가계부 앱 만들어줘` 같은 짧은 요청을 intake 우선 실행 흐름으로 바꾸는 로컬 Codex 플러그인입니다.

Auto Pilot은 중간중간 멈춰서 컨텍스트를 다시 묻는 대신:

- 필요한 입력을 한 번만 수집하고
- 재사용 가능한 프로젝트 계약을 저장하며
- spec, progress, next-step, runtime state 파일을 만들고
- Codex가 장시간 실행을 재개할 수 있는 구조를 제공합니다

## Why It Exists

짧은 프롬프트는 편하지만, 장시간 자율 실행에는 보통 정보가 부족합니다.

Auto Pilot은 이 문제를 다음 요소로 보완합니다.

- 질문을 하나씩 하는 intake
- 명시적인 definition of done
- blocker 정책
- 재개 가능한 프로젝트 상태

목표는 단순합니다. babysitting은 줄이고, 전진은 늘리는 것입니다.

## What It Does

- 짧은 프로젝트 요청을 구조화된 intake 세션으로 바꿉니다
- `1. Question` / `Questions remaining: N` UX를 사용합니다
- `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, `autopilot/blockers.json`을 작성합니다
- 다음 Codex 세션이 중단 지점부터 다시 시작할 수 있도록 충분한 상태를 남깁니다
- 플러그인 매니페스트와 repo-local marketplace wiring을 함께 제공합니다

## Quick Start

새 intake 세션을 시작합니다.

```bash
python3 auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

현재 질문에 답합니다.

```bash
python3 auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

현재 모드와 상태를 확인합니다.

```bash
python3 auto-pilot/scripts/autopilot.py status \
  --workspace /tmp/my-project
```

마지막 답변이 들어가면 Auto Pilot은 아래 파일을 생성합니다.

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 짧은 프롬프트가 intake를 시작합니다.
2. Auto Pilot이 질문을 하나씩 합니다.
3. 답변을 프로젝트 계약으로 정규화합니다.
4. 이후 실행과 재개를 위한 runtime state를 만듭니다.
5. Codex는 컨텍스트를 다시 추론하지 않고 저장된 파일에서 이어서 진행할 수 있습니다.

## Repository Layout

- [auto-pilot](./auto-pilot): plugin root
- [auto-pilot/.codex-plugin/plugin.json](./auto-pilot/.codex-plugin/plugin.json): plugin manifest
- [auto-pilot/scripts](./auto-pilot/scripts): CLI and helper scripts
- [auto-pilot/skills](./auto-pilot/skills): orchestration, intake, and resume skills
- [.agents/plugins/marketplace.json](./.agents/plugins/marketplace.json): repo-local marketplace config

## Current Status

현재 이 저장소는 아래 항목에 집중하고 있습니다.

- intake UX
- spec 및 state bootstrapping
- resume-friendly file structure
- multilingual README entry points

다음으로 가장 자연스러운 단계는 플러그인을 home-level marketplace에 자동 등록하는 one-command installer입니다.
