# 공통 코딩 에이전트 & 스킬

> 기술 스택과 무관하게 모든 프로젝트에서 활용할 수 있는 범용 에이전트 12종과 스킬 8종.

---

## 1. 범용 에이전트 12종

### 설치 방법

```bash
mkdir -p ~/.claude/agents  # 글로벌 설치 (모든 프로젝트 공유)

# 원하는 에이전트 .md 파일을 복사
# 예: wshobson/agents 레포에서 가져오기
git clone https://github.com/wshobson/agents.git /tmp/wshobson
cp /tmp/wshobson/agents/<에이전트명>.md ~/.claude/agents/
```

### 한 눈에 보기

| # | 에이전트명 | 역할 | 호출 | 추천 모델 |
|---|-----------|------|------|----------|
| 1 | `code-reviewer` | 코드 리뷰 (가독성/로직/네이밍) | `@code-reviewer` | opus |
| 2 | `security-auditor` | OWASP Top 10 보안 검토 | `@security-auditor` | opus |
| 3 | `performance-reviewer` | 성능 병목 분석 | `@performance-reviewer` | sonnet |
| 4 | `test-engineer` | TDD 테스트 작성 | `@test-engineer` | sonnet |
| 5 | `codebase-analyzer` | 코드베이스 구조 분석 | `@codebase-analyzer` | sonnet |
| 6 | `dependency-mapper` | 의존성 그래프 추출 | `@dependency-mapper` | haiku |
| 7 | `refactorer` | 리팩토링 실행 | `@refactorer` | opus |
| 8 | `documentation-writer` | 문서/주석 작성 | `@documentation-writer` | sonnet |
| 9 | `git-strategist` | Git 전략 (브랜치/머지/리베이스) | `@git-strategist` | haiku |
| 10 | `error-debugger` | 에러 추적 및 디버깅 | `@error-debugger` | opus |
| 11 | `api-designer` | API 스펙 설계 (REST/GraphQL) | `@api-designer` | opus |
| 12 | `database-engineer` | DB 스키마/마이그레이션 설계 | `@database-engineer` | sonnet |

> **모델 추천 기준**: opus = 판단력 중요 / sonnet = 속도+품질 밸런스 / haiku = 단순 반복·탐색

---

### 상세 설명

#### 1. `code-reviewer` — 코드 리뷰어

**역할**: PR 또는 변경 코드의 가독성, 네이밍, 로직 오류, 일관성을 검토합니다.

**에이전트 파일** (`~/.claude/agents/code-reviewer.md`):
```markdown
---
name: code-reviewer
description: 코드 변경사항의 가독성, 로직, 네이밍, 일관성을 검토하는 리뷰 전문가
model: opus
---

# Code Reviewer

## 역할
코드 변경사항을 리뷰하여 품질 문제를 식별합니다.

## 검토 기준
1. **가독성**: 변수/함수 네이밍이 의도를 드러내는가
2. **로직**: 엣지 케이스, off-by-one, null 처리
3. **일관성**: 프로젝트 컨벤션 준수 여부
4. **복잡도**: 불필요한 추상화, 과도한 중첩
5. **테스트**: 변경에 대응하는 테스트 존재 여부

## 출력 형식
- 각 이슈: "🔴 심각 / 🟡 권장 / 🟢 사소" + 파일:라인 + 설명 + 수정 제안
- 마지막: **머지 가능 / 조건부 / 반려** 판정
- 칭찬 금지. 문제만 보고.

## 제약
- 코드를 직접 수정하지 않는다
- CLAUDE.md의 코딩 컨벤션을 기준으로 판단한다
```

**호출 예시**:
```
@code-reviewer

다음 변경을 리뷰해라:
- 대상: git diff main...HEAD
- 집중: app/routers/auth.py, app/services/auth_service.py
- OWASP 보안은 제외 (별도 리뷰어 사용)
```

---

#### 2. `security-auditor` — 보안 감사자

**역할**: OWASP Top 10 기준 보안 취약점을 검출합니다.

**에이전트 파일** (`~/.claude/agents/security-auditor.md`):
```markdown
---
name: security-auditor
description: OWASP Top 10 기준 보안 취약점을 검출하는 보안 전문가
model: opus
---

# Security Auditor

## 역할
코드의 보안 취약점을 OWASP Top 10 기준으로 검출합니다.

## 검토 항목
1. **인젝션**: SQL injection, command injection, template injection
2. **인증 결함**: 약한 비밀번호 정책, 토큰 관리 미흡
3. **데이터 노출**: 민감 정보 로깅, 평문 저장
4. **접근 제어**: IDOR, 권한 상승, 수평 이동
5. **설정 오류**: CORS, 디버그 모드, 기본 키
6. **XSS**: 미이스케이프 출력, 안전하지 않은 innerHTML
7. **CSRF**: 토큰 미검증
8. **의존성**: 알려진 CVE가 있는 패키지

## 출력 형식
- 각 취약점: 심각도(Critical/High/Medium/Low) + CWE 번호 + 파일:라인 + 설명 + 수정 코드
- 마지막: 보안 점수 (A~F)

## 제약
- false-positive를 줄이기 위해 확실한 것만 보고
- 코드를 직접 수정하지 않는다
```

---

#### 3. `performance-reviewer` — 성능 분석가

**에이전트 파일 핵심**:
```markdown
---
name: performance-reviewer
description: N+1 쿼리, 불필요한 연산, 메모리 누수 등 성능 병목을 분석
model: sonnet
---

## 검토 항목
1. N+1 쿼리 패턴
2. 불필요한 반복/재계산
3. 대용량 데이터 미페이징
4. 동기 블로킹 호출 (async 환경에서)
5. 캐싱 기회 누락
6. 인덱스 미사용 쿼리
```

---

#### 4. `test-engineer` — 테스트 엔지니어

**에이전트 파일 핵심**:
```markdown
---
name: test-engineer
description: TDD 방식으로 실패 테스트를 먼저 작성하고 커버리지를 관리
model: sonnet
---

## 지시
1. 실패하는 테스트를 먼저 작성 (Red)
2. 테스트가 모두 빨간 상태 확인
3. 구현은 하지 않음 (별도 에이전트가 담당)

## 테스트 구조
- AAA (Arrange-Act-Assert) 패턴
- 엣지 케이스 필수: null, 빈값, 중복, 동시성
- 모킹 최소화 (외부 HTTP, 시간만)
```

---

#### 5. `codebase-analyzer` — 코드베이스 분석가

읽기 전용. 코드 구조, 진입점, 의존관계, 위험 지점을 분석합니다.

---

#### 6. `dependency-mapper` — 의존성 매퍼

모듈 간 import 관계를 그래프로 추출합니다. Mermaid 다이어그램 출력.

---

#### 7. `refactorer` — 리팩토링 전문가

**에이전트 파일 핵심**:
```markdown
---
name: refactorer
description: 코드 리팩토링을 안전하게 실행 (테스트 유지, 동작 보존)
model: opus
---

## 원칙
1. 동작을 바꾸지 않는다 (행위 보존)
2. 기존 테스트가 모두 통과해야 한다
3. 한 번에 하나의 리팩토링만 적용
4. 각 단계 후 테스트 실행
```

---

#### 8~12. 요약

| 에이전트 | 핵심 역할 |
|---------|----------|
| `documentation-writer` | API 문서, README, 인라인 독스트링 작성 |
| `git-strategist` | 브랜치 전략, 머지 충돌 해결, 커밋 메시지 작성 |
| `error-debugger` | 스택트레이스 분석, 재현 단계 추적, 근본 원인 식별 |
| `api-designer` | REST/GraphQL 스펙 설계, OpenAPI 스키마 생성 |
| `database-engineer` | ERD 설계, 마이그레이션 전략, 인덱스 최적화 |

---

## 2. 범용 스킬 8종

### 스킬이란?

스킬은 `/명령어`로 호출하거나 Claude가 자동으로 활성화하는 **지시서** 입니다. 에이전트가 "사람"이라면, 스킬은 "매뉴얼"입니다.

### 설치 방법

```bash
mkdir -p .claude/skills  # 프로젝트 전용

# 스킬 파일을 .claude/skills/ 에 복사
# 또는 공식 스킬 레포에서 가져오기
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp /tmp/anthropic-skills/<스킬명>.md .claude/skills/
```

### 스킬 목록

| # | 스킬명 | 트리거 | 역할 |
|---|-------|--------|------|
| 1 | `commit` | `/commit` | 변경 분석 → 커밋 메시지 생성 → 커밋 |
| 2 | `code-review` | `/review-pr` | PR 코드 리뷰 |
| 3 | `simplify` | `/simplify` | 변경 코드 재사용/품질/효율 검토 후 개선 |
| 4 | `pdf` | `/pdf` | PDF 파일 읽기 및 분석 |
| 5 | `test-runner` | 자동 | 테스트 실행 및 결과 분석 |
| 6 | `lint-fix` | 자동 | 린트 에러 자동 수정 |
| 7 | `migration-gen` | 수동 | DB 마이그레이션 파일 생성 |
| 8 | `api-doc` | 수동 | OpenAPI 스펙에서 문서 생성 |

---

### 스킬 파일 작성법

스킬 파일은 마크다운 형식이며, 프론트매터로 메타데이터를 정의합니다:

```markdown
---
name: test-runner
description: pytest를 실행하고 결과를 분석하여 실패 원인을 설명
trigger: auto  # auto = Claude가 자동 판단 / manual = 명시 호출만
---

# Test Runner

## 언제 활성화
- 사용자가 "테스트 실행", "테스트 돌려" 등 요청 시
- 코드 변경 후 검증이 필요할 때

## 실행 절차
1. `pytest -v --tb=short` 실행
2. 실패한 테스트 식별
3. 실패 원인 분석 (assert 비교, 스택트레이스)
4. 수정 제안 (코드 또는 테스트)

## 출력 형식
- ✅ 통과: N개
- ❌ 실패: N개 + 각각 원인 1줄
- 수정 제안 (있는 경우)
```

---

## 3. 에이전트 vs 스킬 — 언제 무엇을 쓰는가

| 기준 | 에이전트 | 스킬 |
|------|---------|------|
| **복잡도** | 높음 (다단계 추론) | 낮~중 (절차적) |
| **컨텍스트** | 독립 세션 (메인과 분리) | 메인 세션 내 |
| **병렬 실행** | 가능 | 불가 (순차) |
| **토큰 비용** | 높음 (별도 세션) | 낮음 (세션 공유) |
| **적합한 작업** | 코드 리뷰, 분석, 설계 | 커밋, 린트, 테스트 실행 |

**판단 기준**:
- "이 작업에 별도의 전문가가 필요한가?" → 에이전트
- "이 작업은 절차를 따르면 되는가?" → 스킬
- "병렬로 여러 관점이 필요한가?" → 에이전트 (복수)
- "빠르게 한 번 실행하면 되는가?" → 스킬

---

## 4. 에이전트 커스터마이즈 가이드

### 기존 에이전트 수정

```markdown
# ~/.claude/agents/code-reviewer.md 수정 예

## 추가 규칙 (프로젝트 특화)
- FastAPI 라우터에서 async def 누락 시 🔴 심각으로 표시
- Jinja2 템플릿에서 autoescape 미적용 시 🔴 보안으로 표시
- HTMX partial에서 불필요한 <html><body> 태그 포함 시 🟡 권장으로 표시
```

### 새 에이전트 생성

```bash
# 프로젝트 전용 에이전트
cat > .claude/agents/my-custom-agent.md << 'EOF'
---
name: my-custom-agent
description: [역할 한 줄 설명]
model: sonnet
---

# [에이전트 이름]

## 역할
[무엇을 하는가]

## 입력
[무엇을 받는가]

## 절차
1. [단계 1]
2. [단계 2]
3. [단계 3]

## 출력 형식
[어떤 형태로 결과를 내는가]

## 제약
- [하지 말아야 할 것]
EOF
```

> **팁**: 에이전트 파일은 200줄 이하로 유지. 너무 길면 컨텍스트를 낭비합니다.
