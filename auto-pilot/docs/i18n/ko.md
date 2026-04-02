# Auto Pilot Docs

> 한 번 묻고, 브리프를 잠그고, 계속 만들어갑니다.

[English](../../README.md) | 한국어 | [日本語](./ja.md) | [中文](./zh.md) | [العربية](./ar.md)

이 폴더는 `Auto Pilot` Codex 플러그인의 초기 문서 패키지를 담고 있습니다. 이 플러그인은 짧은 프로젝트 요청을 intake 기반 장기 자율 실행 워크플로우로 바꿉니다.

## Files

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
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

현재 세션은 플러그인 목록을 즉시 갱신하지 않을 수 있습니다. 새 세션에서 workspace를 다시 여는 것이 plugin discovery를 강제로 반영하는 가장 안전한 방법입니다.
