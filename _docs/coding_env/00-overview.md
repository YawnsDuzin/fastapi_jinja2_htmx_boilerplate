# FastAPI + HTMX 스택 — Claude Code 최적화 매뉴얼

> 보일러플레이트 기반 추가 개발을 위한 에이전트·스킬·오케스트레이터·훅 설정 가이드

---

## 대상 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| Backend | FastAPI | 0.115+ | 비동기 웹 프레임워크 |
| Template | Jinja2 | 3.1+ | 서버사이드 렌더링 |
| Frontend | HTMX | 2.0+ | AJAX/동적 UI |
| UI | Alpine.js | 3.x | 클라이언트 상호작용 |
| CSS | TailwindCSS | 3.4+ | 스타일링 (CDN) |
| Database | SQLAlchemy | 2.0+ | 비동기 ORM |
| Auth | python-jose | 3.3+ | JWT 인증 |

---

## 문서 구성

| # | 문서 | 내용 |
|---|------|------|
| 00 | **본 문서** | 전체 개요, 설치 순서, 빠른 시작 |
| 01 | [CLAUDE.md 템플릿](01-claude-md-template.md) | 프로젝트 루트에 배치할 CLAUDE.md 완성본 |
| 02 | [공통 코딩 에이전트·스킬](02-common-agents.md) | 스택에 무관한 범용 에이전트 12종 + 스킬 8종 |
| 03 | [스택 전용 에이전트](03-stack-agents.md) | FastAPI·HTMX·SQLAlchemy 등 기술별 전문 에이전트 10종 |
| 04 | [오케스트레이터](04-orchestrator.md) | 멀티 에이전트 파이프라인 3종 (기능개발/버그수정/리팩토링) |
| 05 | [슬래시 커맨드 & 훅](05-commands-hooks.md) | `/slash` 커맨드 7종 + 이벤트 훅 5종 설정법 |
| 06 | [실전 워크플로우 예제](06-workflow-examples.md) | 6가지 시나리오별 복붙 프롬프트 |

---

## 빠른 시작 (5분)

### 1단계: CLAUDE.md 배치

```bash
# 01-claude-md-template.md 내용을 프로젝트 루트에 복사
cp _docs/01-claude-md-template.md ./CLAUDE.md
# 또는 직접 편집하여 프로젝트에 맞게 커스터마이즈
```

### 2단계: 에이전트 설치

```bash
# 공통 에이전트 (02-common-agents.md 참고)
mkdir -p ~/.claude/agents
# 필요한 에이전트 .md 파일을 ~/.claude/agents/ 에 복사

# 프로젝트 전용 에이전트 (03-stack-agents.md 참고)
mkdir -p .claude/agents
# 프로젝트 전용 에이전트 .md 파일을 .claude/agents/ 에 복사
```

### 3단계: 커맨드 & 훅 설정

```bash
# 슬래시 커맨드 (05-commands-hooks.md 참고)
mkdir -p .claude/commands
# 커맨드 .md 파일을 .claude/commands/ 에 복사

# 훅은 settings.json 에 추가
```

### 4단계: 확인

```
# Claude Code 세션에서
> /help          # 등록된 커맨드 확인
> @fastapi-dev   # 에이전트 호출 테스트
```

---

## 설치 위치 요약

| 자산 유형 | 글로벌 (모든 프로젝트) | 프로젝트 전용 |
|----------|---------------------|-------------|
| 에이전트 | `~/.claude/agents/` | `.claude/agents/` |
| 스킬 | `~/.claude/skills/` | `.claude/skills/` |
| 커맨드 | `~/.claude/commands/` | `.claude/commands/` |
| 훅 | `~/.claude/settings.json` | `.claude/settings.json` |
| 지시사항 | `~/.claude/CLAUDE.md` | `CLAUDE.md` (프로젝트 루트) |

> **우선순위**: 프로젝트 전용 > 글로벌. 같은 이름이면 프로젝트 전용이 우선.

---

## 핵심 원칙

1. **필요한 것만 설치** — 에이전트를 전부 깔면 컨텍스트 충돌·토큰 낭비 발생
2. **CLAUDE.md가 기반** — 에이전트·스킬은 CLAUDE.md의 규칙을 상속받음
3. **점진적 도입** — 공통 에이전트 → 스택 전용 에이전트 → 오케스트레이터 순서로 확장
4. **읽기 전용 먼저** — 새 에이전트는 "파일 수정 금지" 모드로 먼저 테스트
