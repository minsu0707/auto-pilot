# 오토파일럿 플러그인 명세

## 플러그인 역할

오토파일럿은 단일 도구가 아니라 Codex 위에 얹는 orchestration 레이어입니다. 주요 기능은 아래 다섯 가지입니다.

- intake
- planning
- execution
- recovery
- blocker handling

## 제안 구조

```text
plugins/auto-pilot/
  .codex-plugin/plugin.json
  skills/
    project-intake/SKILL.md
    project-execution/SKILL.md
    blocker-triage/SKILL.md
    resume-from-state/SKILL.md
    done-check/SKILL.md
  scripts/
    bootstrap-state.ts
    choose-next-task.ts
    classify-blocker.ts
    summarize-status.ts
  hooks.json
  .mcp.json
  .app.json
  assets/
```

## 책임 분리

### `project-intake`

- 짧은 프로젝트 요청 감지
- intake 질문 실행
- 프로젝트 브리프 저장
- 완료 기준 확정

### `project-execution`

- 현재 상태 읽기
- 다음 작업 선택
- 구현 및 검증 수행
- progress와 next 파일 갱신

### `blocker-triage`

- blocker 분류
- retry, defer, escalate 중 하나 결정

### `resume-from-state`

- timeout, 세션 재시작, 자동화 재실행 이후에도 이어서 진행

### `done-check`

- 계속 진행할지 종료할지 판정

## Hook 전략

hook은 무거운 로직을 처리하지 않고 라우팅만 담당한다.

### 예시 트리거

- 사용자 프롬프트에 `build`, `make`, `create`, `launch`, `ship`, `만들어줘` 같은 표현이 있음
- 단일 수정이 아니라 프로젝트 생성형 요청으로 보임
- 잠긴 spec이 없으면 intake로 보냄
- spec은 있고 미완료 상태면 resume로 보냄

## 상태 계약

### 필수 파일

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

### `autopilot/state.json`

권장 구조:

```json
{
  "projectName": "오토파일럿",
  "status": "running",
  "currentMilestone": "MVP foundation",
  "currentTask": "Set up Next.js app shell",
  "retryCount": 0,
  "lastSuccessfulStep": "Created project brief",
  "definitionOfDoneMet": false
}
```

### `autopilot/blockers.json`

권장 구조:

```json
{
  "active": [],
  "resolved": []
}
```

## Intake 데이터 모델

추천 저장 필드:

- `product_summary`
- `target_user`
- `core_features`
- `non_goals`
- `stack_preferences`
- `auth_mode`
- `payments_mode`
- `admin_required`
- `design_direction`
- `deploy_target`
- `data_store`
- `blocker_policy`
- `definition_of_done`

## 실행 규칙

1. 행동 전 항상 상태를 읽는다.
2. 정책상 안전한 기본값이 있으면 질문하지 않는다.
3. 가장 작은 배포 가능 단위를 우선한다.
4. 구현 후 반드시 검증한다.
5. 각 루프 후 상태를 저장한다.
6. done을 만족하거나 human-required blocker가 활성화될 때만 멈춘다.

## 권장 연동

- GitHub: 이슈, PR, 커밋 가시성
- Vercel: 배포와 preview 검증
- Notification provider: blocker 알림
- 선택적 docs 또는 프로젝트 트래킹 연동
