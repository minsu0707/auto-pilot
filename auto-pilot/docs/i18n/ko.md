# Auto Pilot

> 한 번 묻고, 브리프를 잠그고, 계속 만들어갑니다.

[English](../../README.md) | 한국어 | [日本語](./ja.md)

## 한줄로 설치하기

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## Codex에서 실행하기

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

공개 기본 진입점은 `/auto-pilot:autopilot`입니다.
설치 후에는 slash command가 보이도록 Codex를 한 번 다시 시작하면 됩니다.
한 번 설치한 뒤에는 새 프로젝트면 intake로 보내고, 기존 프로젝트면 자동으로 resume 흐름으로 이어집니다.
재시작 후에는 `Build a budgeting app for freelancers ap` 같은 자연어 숏컷도 사용할 수 있습니다.

이 폴더는 `Auto Pilot` Codex 플러그인의 정식 루트입니다. 이 플러그인은 `Build me a budgeting app` 같은 짧은 요청을 intake-first 실행 워크플로우로 바꿉니다.

Auto Pilot은 몇 단계마다 멈춰서 맥락을 다시 묻는 대신:

- 최소한의 필수 입력만 한 번 수집하고
- 재사용 가능한 프로젝트 계약을 저장하고
- spec, progress, next-step, runtime state 파일을 만들고
- 다음 Codex 세션에서도 이어서 진행할 수 있게 만듭니다

## Why It Exists

짧은 프롬프트는 편하지만, 장시간 자율 작업에는 보통 정보가 부족합니다.

Auto Pilot은 이 간극을 아래 요소로 메웁니다.

- 질문 하나씩 intake
- 명확한 definition of done
- blocker 정책
- resume 가능한 프로젝트 상태

목표는 단순합니다. 덜 붙잡고, 더 계속 전진하는 것.

## What It Does

- 짧은 프로젝트 요청을 구조화된 intake 세션으로 바꿉니다
- `1. Question` / `Questions remaining: N` UX 패턴을 사용합니다
- `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, `autopilot/blockers.json`를 생성합니다
- 다음 Codex 세션이 멈춘 지점부터 이어갈 수 있을 만큼 상태를 남깁니다
- 정식 플러그인 코드, 문서, 설치 로직을 모두 `auto-pilot/` 아래에 둡니다

## Quick Start

새 intake 세션 시작:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

현재 질문에 답변:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

현재 모드와 상태 확인:

```bash
python3 scripts/autopilot.py status \
  --workspace /tmp/my-project
```

마지막 답변 후 Auto Pilot은 다음 파일을 생성합니다.

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 짧은 프롬프트가 intake를 시작합니다.
2. Auto Pilot은 질문을 하나씩 묻습니다.
3. 답변은 프로젝트 계약으로 정규화됩니다.
4. 이후 실행과 재개를 위한 runtime state가 생성됩니다.
5. Codex는 맥락을 다시 찾지 않고 저장된 파일에서 이어갑니다.

## Repository Layout

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
- `install.sh`: canonical installer
- `uninstall.sh`: canonical uninstaller

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Usage

다음과 같이 요청할 수 있습니다.

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`
- `Build a budgeting app for freelancers ap`

새 프로젝트에서는 intake가 아래 UX를 따릅니다.

- 질문을 한 번에 하나씩 표시
- `1. Question` 형식 사용
- 다음 줄에 `Questions remaining: N` 표시
- 마지막 답변 후 계약을 요약하고 spec lock 및 실행 시작

하위 스크립트도 그대로 사용할 수 있습니다.

- `init_intake.py`
- `record_answer.py`
- `status.py`

## Current Status

이 폴더가 플러그인 루트이자 문서 루트, 설치 스크립트 기준 위치입니다.

일반 유저 기준 추천 흐름은 one-line installer로 설치한 뒤 Codex를 한 번 재시작하고 `/auto-pilot:autopilot`을 사용하는 것입니다.
