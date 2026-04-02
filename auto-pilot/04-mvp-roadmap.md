# 오토파일럿 MVP 로드맵

## Phase 1: 문서 고정

- 제품명 확정
- PRD 고정
- intake 스키마 정의
- 상태 파일 정의
- blocker 정책 정의

## Phase 2: 플러그인 스캐폴드

- `plugins/auto-pilot/` 생성
- `plugin.json` 작성
- skill 폴더 추가
- script placeholder 추가
- 필요 시 marketplace entry 추가

## Phase 3: Intake 엔진

- 프로젝트형 프롬프트 감지
- 최소 intake 질문 실행
- `docs/spec.md` 작성
- 초기 `autopilot/state.json` 작성

## Phase 4: Execution 엔진

- 현재 상태에서 다음 작업 선택
- 구현 루프 실행
- `docs/progress.md` 갱신
- `docs/next.md` 갱신

## Phase 5: Recovery 와 알림

- 이전 상태에서 재개
- blocker 분류
- human-required 행동만 사용자에게 알림

## Phase 6: 실제 프로젝트 검증

- 실제 0 to 1 프로젝트 하나로 검증
- 중단 횟수 측정
- intake와 blocker 정책 보정

## 권장 구현 순서

1. Intake
2. 상태 파일
3. next-task selector
4. blocker classifier
5. resume flow
6. notifications
7. deploy integration

## MVP 종료 기준

- 짧은 요청이 저장 가능한 프로젝트 브리프로 바뀜
- 플러그인이 저장 상태에서 재개 가능
- 제한된 인간 개입만으로 현실적인 프로젝트 하나를 끝까지 밀어봄
- 남은 중단이 대부분 고위험 외부 작업임
