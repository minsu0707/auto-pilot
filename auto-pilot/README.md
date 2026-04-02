# 오토파일럿 문서

이 폴더는 짧은 프로젝트 요청을 intake 기반 장기 자율 실행 워크플로우로 바꾸는 Codex 플러그인 `오토파일럿`의 초기 문서 패키지입니다.

## 파일 목록

- `01-product-brief.md`: 제품 개요
- `02-prd.md`: 기능 요구사항과 운영 모델
- `03-plugin-spec.md`: 플러그인 구조와 상태 모델
- `04-mvp-roadmap.md`: MVP 구현 순서
- `.codex-plugin/plugin.json`: Codex 플러그인 매니페스트
- `skills/autopilot/SKILL.md`: 시작용 오케스트레이터 스킬
- `skills/autopilot-intake/SKILL.md`: 질문을 하나씩 받는 intake 스킬
- `skills/autopilot-resume/SKILL.md`: 재개용 스킬
- `scripts/autopilot.py`: 추천 CLI 진입점
- `scripts/*.py`: intake 진행, 답변 저장, 상태 확인 스크립트
- `templates/*.json`: 상태 파일 템플릿

## 현재 작업명

- 제품명: `오토파일럿`
- 플러그인 슬러그: `auto-pilot`

## 현재 상태

이 폴더 자체가 플러그인 루트다. repo-local marketplace는 [marketplace.json](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)에 연결되어 있다.

## 사용 방법

다음처럼 요청하면 된다.

- `오토파일럿으로 이 프로젝트 시작해줘`
- `autopilot으로 SaaS MVP 만들어줘`
- `오토파일럿 계속 진행해줘`

새 프로젝트 시작 시 intake는 아래 UX를 따른다.

- 한 번에 하나의 질문만 표시
- `1. 질문` 형식 사용
- 다음 줄에 `남은 질문: N개` 표시
- 마지막 답변 후 요약하고 바로 spec lock 및 실행 시작

## 스크립트 사용 예시

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py start \
  --workspace /path/to/project \
  --prompt "프리랜서를 위한 가계부 앱 만들어줘"

python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py answer \
  --workspace /path/to/project \
  --text "프리랜서와 1인 사업자"

python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py status \
  --workspace /path/to/project
```

마지막 답변이 들어가면 아래 파일들이 자동 생성된다.

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

하위 스크립트도 그대로 사용할 수 있다.

- `init_intake.py`
- `record_answer.py`
- `status.py`

현재 세션의 플러그인 목록은 즉시 갱신되지 않을 수 있다. 새 세션이나 새 작업에서 이 workspace를 다시 열면 plugin discovery가 더 안정적이다.
