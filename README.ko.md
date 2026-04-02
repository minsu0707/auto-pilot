# auto-pilot

[English](./README.md) | 한국어 | [日本語](./README.ja.md) | [中文](./README.zh.md) | [العربية](./README.ar.md)

`오토파일럿` 로컬 Codex 플러그인 저장소입니다.

## 포함 내용

- [오토파일럿 플러그인 루트](/Users/minsu/Documents/Codex/auto-pilot)
- [repo-local marketplace 설정](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- intake, 상태 생성, 재개 흐름용 스크립트

## 핵심 기능

- 짧은 프로젝트 요청을 intake 세션으로 변환
- 질문을 한 번에 하나씩 표시
- `1. 질문` / `Questions remaining: N` UX 사용
- 마지막 답변 후 `docs/spec.md`, `docs/progress.md`, `docs/next.md`, `autopilot/state.json`, `autopilot/blockers.json` 자동 생성
- 다음 Codex 세션에서 이어서 실행할 수 있는 상태 구조 제공
