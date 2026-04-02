# Auto Pilot Docs

> 한 번 묻고, 브리프를 잠그고, 계속 만들어갑니다.

[English](../../README.md) | 한국어 | [日本語](./ja.md) | [中文](./zh.md) | [العربية](./ar.md)

## 한줄로 설치하기

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## Codex에서 실행하기

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

공개 진입점은 `/auto-pilot:autopilot` 하나로 보면 됩니다.
설치 후에는 slash command가 보이도록 Codex를 한 번 다시 시작하면 됩니다.
한 번 설치한 뒤에는 새 프로젝트면 intake로 보내고, 기존 프로젝트면 자동으로 resume 흐름으로 이어집니다.

이 폴더는 `Auto Pilot` Codex 플러그인의 초기 문서 패키지를 담고 있습니다. 이 플러그인은 짧은 프로젝트 요청을 intake 기반 장기 자율 실행 워크플로우로 바꿉니다.

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

이 폴더는 plugin root입니다. repo-local marketplace는 [marketplace.json](../../../.agents/plugins/marketplace.json)을 통해 연결됩니다.

## Usage

다음과 같이 요청할 수 있습니다.

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`

새 프로젝트에서는 intake가 아래 UX를 따릅니다.

- 질문을 한 번에 하나씩 표시
- `1. Question` 형식 사용
- 다음 줄에 `Questions remaining: N` 표시
- 마지막 답변 후 계약을 요약하고 spec lock 및 실행 시작

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

마지막 답변 후 아래 파일이 생성됩니다.

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

하위 스크립트도 그대로 사용할 수 있습니다.

- `init_intake.py`
- `record_answer.py`
- `status.py`

일반 유저 기준 추천 흐름은 one-line installer로 설치한 뒤 Codex를 한 번 재시작하고 `/auto-pilot:autopilot`을 사용하는 것입니다.
