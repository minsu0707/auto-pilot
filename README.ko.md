# Auto Pilot

<p align="center">
  <img src="./assets/auto-pilot.png" alt="Auto Pilot mascot" width="260" />
</p>

> 한 번 묻고, 브리프를 잠그고, 계속 만들어갑니다.

이 마스코트는 [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) 창시자의 히어로 아이콘 스타일에서 영감을 받아 제작했습니다.

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](./README.md) | 한국어 | [日本語](./README.ja.md)

## 한줄로 설치하기

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

안정적으로 설치하려면 `v0.1.1`을 사용하고, stable release tag는 반드시 그 태그 자체를 설치하도록 유지하세요. 아래 예시는 다음 stable release에 반영될 현재 저장소 워크플로를 설명하므로, 다음 태그 전에 미리 검증할 때만 `develop`을 사용하세요.
다음 stable tag를 만들 때는 install URL, 설치 예시, baked-in stable ref를 함께 갱신해야 합니다.

## Codex에서 실행하기

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

공개 기본 진입점은 `$auto-pilot`입니다.
설치 후에는 skill이 보이도록 Codex를 한 번 다시 시작하면 됩니다.
한 번 설치한 뒤에는 새 프로젝트면 intake로 보내고, 기존 프로젝트면 자동으로 resume 흐름으로 이어집니다.
재시작 후에는 `Build a diary app my friend Dohyeon would love ap` 같은 자연어 숏컷도 사용할 수 있습니다.

## What It Is

Auto Pilot은 짧은 제품 요청을 resumable execution workflow로 바꾸는 Codex 플러그인입니다.

- 중요한 입력만 한 번 수집하고
- 재사용 가능한 프로젝트 계약을 저장하고
- 진짜 human-only blocker가 나오기 전까지 계속 진행하고
- 저장된 상태를 바탕으로 다음 세션에서 다시 이어갑니다

## Why It Exists

짧은 프롬프트는 편하지만, 장시간 자율 작업에는 보통 정보가 부족합니다.

Auto Pilot은 이 간극을 아래 요소로 메웁니다.

- 질문 하나씩 intake
- 명확한 definition of done
- 기본 blocker 정책
- resume 가능한 프로젝트 상태

목표는 단순합니다. 덜 붙잡고, 더 계속 전진하는 것.

## Core Features

- 짧은 프로젝트 요청을 구조화된 intake 세션으로 바꿉니다
- `1. Question` / `Questions remaining: N` 패턴으로 상호작용합니다
- `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, `autopilot/blockers.json`를 생성합니다
- user-facing 프로젝트에서는 generic 기본 UI 대신 구체적인 디자인 브리프로 시작하도록 `docs/design.md`도 생성합니다
- 다음 Codex 세션이 멈춘 지점부터 이어갈 수 있을 만큼 상태를 남깁니다
- 디자인 관련 설명은 broad web research를 끝냈다는 뜻이 아니라, curated reference stack을 바탕으로 한 디자인 브리프를 만든다는 뜻입니다
- 정식 플러그인 코드, 문서, 설치 로직을 모두 저장소 루트에 둡니다

## Quick Start

새 intake 세션 시작:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a diary app my friend Dohyeon would love"
```

현재 질문에 답변:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "매일 꾸미며 비밀스럽게 기록하고 싶은 10대 사용자"
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
- user-facing 프로젝트라면 `docs/design.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 짧은 프롬프트가 intake를 시작합니다.
2. Auto Pilot은 질문을 하나씩 묻습니다.
3. 답변은 프로젝트 계약으로 정규화됩니다.
4. user-facing 프로젝트라면 선택한 theme, vibe, design direction을 바탕으로 `docs/design.md` 브리프도 생성됩니다.
5. 이후 실행과 재개를 위한 runtime state가 생성됩니다.
6. Codex는 맥락을 다시 찾지 않고 저장된 파일에서 이어갑니다.

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/05-how-it-works.md`: intake, state, resume 흐름을 그림으로 정리한 문서
- `docs/06-usage-guide.md`: 설치, 실행, resume, CLI, 팀 오케스트레이션 사용법 가이드
- `docs/i18n/*`: localized README files
- `assets/auto-pilot.png`: mascot image
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

## Current Status

이 저장소 루트가 플러그인 루트이자 문서 루트, 설치 스크립트 기준 위치입니다.

일반 유저 기준 추천 흐름은 one-line installer로 설치한 뒤 Codex를 한 번 재시작하고 `$auto-pilot`을 사용하는 것입니다.
더 자세한 사용 흐름은 `docs/06-usage-guide.md`에서 확인할 수 있습니다.
