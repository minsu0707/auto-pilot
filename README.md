# auto-pilot

Codex에서 사용할 수 있는 로컬 플러그인 `오토파일럿` 저장소입니다.

## 포함 내용

- [오토파일럿 플러그인 루트](/Users/minsu/Documents/Codex/auto-pilot)
- [repo-local marketplace 설정](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- intake, 상태 저장, 재개 흐름을 위한 실행 스크립트

## 핵심 기능

- 짧은 프로젝트 요청을 intake 세션으로 변환
- 질문을 한 번에 하나씩 표시
- `1. 질문` / `남은 질문: N개` 형식의 UX 제공
- 마지막 답변 후 `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, `autopilot/blockers.json` 자동 생성
- 다음 세션에서 이어서 실행할 수 있는 상태 구조 제공

## 빠른 시작

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "프리랜서를 위한 가계부 앱 만들어줘"
```

이후 답변은 한 개씩 입력한다.

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "프리랜서와 1인 사업자"
```

상태 확인:

```bash
python3 /Users/minsu/Documents/Codex/auto-pilot/scripts/autopilot.py status \
  --workspace /tmp/my-project
```
