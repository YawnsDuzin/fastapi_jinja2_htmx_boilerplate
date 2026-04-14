# 슬래시 커맨드 & 훅 설정

> 사용자가 `/명령`으로 호출하는 커맨드 7종과, 이벤트 기반으로 자동 실행되는 훅 5종의 설정 가이드.

---

## 1. 슬래시 커맨드

### 개념

슬래시 커맨드는 `.claude/commands/` 디렉토리에 `.md` 파일로 정의하며, Claude Code 세션에서 `/파일명`으로 호출합니다.

```bash
# 디렉토리 생성
mkdir -p .claude/commands

# 커맨드 파일 생성
# .claude/commands/test.md → /test 로 호출
```

### 커맨드 파일 형식

```markdown
# 커맨드 설명 (첫 줄이 도움말에 표시됨)

[Claude에게 전달할 지시 내용]

$ARGUMENTS  ← 사용자가 /test 뒤에 입력한 텍스트가 여기에 삽입됨
```

---

### 커맨드 1: `/test` — 테스트 실행

`.claude/commands/test.md`:
```markdown
# 테스트를 실행하고 결과를 분석합니다

다음 명령어로 테스트를 실행하고 결과를 분석해라:

```bash
pytest $ARGUMENTS -v --tb=short
```

실행 결과:
1. 전체 통과 시: "✅ N개 테스트 통과" 출력
2. 실패 시: 실패한 테스트별로
   - 파일:라인
   - assert 비교값
   - 실패 원인 추정 (1줄)
   - 수정 제안
3. 마지막: 전체 커버리지 요약 (있다면)

수정이 필요하면 제안만 하고, 내 승인 후에 수정해라.
```

**사용 예시**:
```
/test                           # 전체 테스트
/test tests/test_auth.py        # 특정 파일
/test -k "test_login"           # 특정 테스트
```

---

### 커맨드 2: `/migrate` — DB 마이그레이션 생성

`.claude/commands/migrate.md`:
```markdown
# Alembic 마이그레이션을 생성하고 검증합니다

다음 순서로 마이그레이션을 처리해라:

1. `app/models/` 의 변경사항을 확인
2. 마이그레이션 생성:
   ```bash
   alembic revision --autogenerate -m "$ARGUMENTS"
   ```
3. 생성된 마이그레이션 파일을 검토:
   - upgrade() / downgrade() 양방향 확인
   - 데이터 손실 위험 (DROP COLUMN 등) 경고
   - 인덱스 추가/삭제 확인
4. 검토 결과를 보여주고 내 승인을 기다려라
5. 승인 후:
   ```bash
   alembic upgrade head
   ```
6. 마이그레이션 결과 확인
```

**사용 예시**:
```
/migrate "add favorites table"
/migrate "add index on users email"
```

---

### 커맨드 3: `/route` — 새 API 라우트 생성

`.claude/commands/route.md`:
```markdown
# 새 API 라우트를 표준 패턴으로 생성합니다

다음 요구사항에 맞는 API 라우트를 생성해라:

$ARGUMENTS

생성할 파일들:
1. `app/schemas/[이름].py` — Pydantic 스키마 (Create/Update/Response)
2. `app/services/[이름]_service.py` — 비즈니스 로직
3. `app/routers/[이름].py` — FastAPI 라우터

규칙:
- 모든 함수는 async def
- DB 쿼리는 서비스 레이어에서만
- HTMX 요청 분기 처리 포함
- Depends()로 인증/DB 세션 주입
- 기존 라우터 스타일 (`app/routers/` 참고) 따르기

생성 후 `app/main.py`에 라우터 등록 코드도 추가해라.
```

**사용 예시**:
```
/route "즐겨찾기 CRUD — POST/GET/DELETE /api/v1/favorites, 인증 필수"
/route "댓글 CRUD — 항목별 댓글 목록/작성/삭제, 페이지네이션"
```

---

### 커맨드 4: `/page` — 새 HTMX 페이지 생성

`.claude/commands/page.md`:
```markdown
# HTMX 페이지와 partial fragment를 생성합니다

다음 요구사항에 맞는 페이지를 생성해라:

$ARGUMENTS

생성할 파일들:
1. `app/templates/pages/[이름].html` — 전체 페이지 (base.html 상속)
2. `app/templates/components/_[이름]-*.html` — Partial fragment(s)
3. `app/routers/pages.py`에 페이지 라우트 추가 (또는 신규 파일)

규칙:
- 전체 페이지는 `{% extends "base.html" %}` 사용
- Partial fragment는 `<html>/<body>` 태그 금지
- TailwindCSS 클래스만 사용 (인라인 style 금지)
- HTMX 속성으로 동적 로딩 구현
- 빈 상태 (empty state) 처리 포함
- 로딩 인디케이터 포함

HX-Request 분기:
- HTMX 요청 → partial fragment 반환
- 일반 요청 → 전체 페이지 반환
```

**사용 예시**:
```
/page "대시보드 — 최근 활동 목록 + 통계 카드 3개"
/page "프로필 설정 — 탭 3개 (기본정보/보안/알림)"
```

---

### 커맨드 5: `/review` — 코드 리뷰

`.claude/commands/review.md`:
```markdown
# 현재 변경사항을 리뷰합니다

다음 변경사항을 리뷰해라:

```bash
git diff $ARGUMENTS
```

리뷰 관점 (3가지 병렬):
1. **코드 품질**: 가독성, 네이밍, 일관성, 복잡도
2. **보안**: OWASP Top 10 (특히 인젝션, 인증 결함, XSS)
3. **성능**: N+1 쿼리, 동기 블로킹, 불필요한 연산

출력 형식:
- 각 이슈: 심각도 (🔴/🟡/🟢) + 파일:라인 + 설명 + 수정 제안
- 마지막: **머지 가능 / 조건부 / 반려** + 이유
- 칭찬 금지

FastAPI 스택 특화 검사:
- async def 사용 여부
- Depends() 적절한 사용
- HTMX partial fragment에 전체 페이지 태그 포함 여부
- SQLAlchemy N+1 패턴
- JWT 토큰 처리 안전성
```

**사용 예시**:
```
/review                    # 전체 unstaged 변경
/review --staged           # staged 변경만
/review main...HEAD        # 브랜치 전체 변경
```

---

### 커맨드 6: `/check` — 프로젝트 상태 점검

`.claude/commands/check.md`:
```markdown
# 프로젝트 상태를 점검합니다

다음 항목을 순서대로 점검하고 결과를 보고해라:

1. **린트**: `ruff check app/` (또는 프로젝트 린터)
2. **테스트**: `pytest -v --tb=short`
3. **마이그레이션**: `alembic check` (pending 마이그레이션 확인)
4. **의존성**: requirements.txt vs 실제 import 불일치
5. **보안**: .env 파일이 .gitignore에 포함되어 있는지
6. **Git**: uncommitted 변경, 브랜치 상태

결과 형식:
- ✅ 통과 / ❌ 실패 / ⚠️ 경고
- 실패/경고 항목은 수정 방법 제안
```

**사용 예시**:
```
/check          # 전체 점검
```

---

### 커맨드 7: `/scaffold` — 새 기능 스캐폴딩

`.claude/commands/scaffold.md`:
```markdown
# 새 기능의 파일 구조를 한 번에 생성합니다

다음 기능에 필요한 파일들을 스캐폴딩해라:

$ARGUMENTS

생성할 파일 목록:
1. `app/models/[이름].py` — SQLAlchemy 모델 (기본 필드만)
2. `app/schemas/[이름].py` — Pydantic 스키마 (Create/Update/Response)
3. `app/services/[이름]_service.py` — 서비스 레이어 (함수 시그니처만)
4. `app/routers/[이름].py` — FastAPI 라우터 (엔드포인트 시그니처만)
5. `app/templates/pages/[이름].html` — 빈 페이지 템플릿
6. `app/templates/components/_[이름]-list.html` — 빈 목록 fragment
7. `tests/test_[이름].py` — 빈 테스트 파일 (fixture만)
8. `alembic revision --autogenerate -m "add [이름] table"`

규칙:
- 각 파일에 TODO 주석으로 구현해야 할 내용 표시
- 실제 구현은 하지 않고 구조만 생성
- app/main.py에 라우터 등록 추가
- 생성 완료 후 파일 목록 출력
```

**사용 예시**:
```
/scaffold "상품(Product) — 이름, 가격, 설명, 카테고리. CRUD + 검색"
/scaffold "알림(Notification) — 사용자별 알림 목록, 읽음 처리"
```

---

## 2. 훅 (Hooks)

### 개념

훅은 Claude Code의 특정 이벤트에 자동으로 실행되는 쉘 스크립트입니다. `settings.json`에 정의합니다.

### 이벤트 종류

| 이벤트 | 발생 시점 | 용도 |
|--------|----------|------|
| `PreToolUse` | 도구 실행 직전 | 검증, 차단 |
| `PostToolUse` | 도구 실행 직후 | 후처리, 알림 |
| `Notification` | 알림 발생 시 | 외부 알림 전송 |
| `Stop` | Claude 응답 완료 시 | 최종 검증 |
| `SubagentStop` | 서브에이전트 완료 시 | 결과 검증 |

### 설정 위치

```
# 프로젝트 전용
.claude/settings.json

# 글로벌
~/.claude/settings.json
```

---

### 훅 1: 자동 포맷팅 (PostToolUse)

파일 수정 후 자동으로 ruff format을 실행합니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "ruff format --quiet ${file_path} 2>/dev/null || true",
        "description": "Python 파일 수정 후 자동 포맷팅"
      }
    ]
  }
}
```

---

### 훅 2: .env 파일 보호 (PreToolUse)

`.env` 파일을 읽거나 수정하려는 시도를 차단합니다.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write",
        "command": "echo '${file_path}' | grep -q '\\.env' && echo 'BLOCK: .env 파일 접근 금지' && exit 1 || true",
        "description": ".env 파일 읽기/수정 차단"
      }
    ]
  }
}
```

---

### 훅 3: 마이그레이션 파일 자동 검증 (PostToolUse)

Alembic 마이그레이션 파일이 생성되면 자동으로 검증합니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "echo '${file_path}' | grep -q 'alembic/versions' && echo '⚠️ 마이그레이션 파일 생성됨 — upgrade/downgrade 확인 필요' || true",
        "description": "마이그레이션 파일 생성 알림"
      }
    ]
  }
}
```

---

### 훅 4: 테스트 자동 실행 (Stop)

Claude 응답이 완료되면 관련 테스트를 자동 실행합니다.

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "git diff --name-only HEAD | grep -q 'app/' && pytest -x -q --tb=line 2>/dev/null; exit 0",
        "description": "코드 변경 시 자동 테스트 실행"
      }
    ]
  }
}
```

---

### 훅 5: 동기 함수 경고 (PostToolUse)

`def ` (async가 아닌) 함수가 라우터에 추가되면 경고합니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "echo '${file_path}' | grep -q 'routers/' && grep -n '^def ' '${file_path}' 2>/dev/null | head -5 | while read line; do echo \"⚠️ 동기 함수 감지: $line — async def 사용 권장\"; done; exit 0",
        "description": "라우터에서 동기 함수 사용 경고"
      }
    ]
  }
}
```

---

## 3. settings.json 전체 예시

`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest*)",
      "Bash(ruff*)",
      "Bash(alembic*)",
      "Bash(uvicorn*)",
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(DROP*)",
      "Bash(git push --force*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write",
        "command": "echo '${file_path}' | grep -q '\\.env' && echo 'BLOCK: .env 파일 접근 금지' && exit 1 || true",
        "description": ".env 파일 보호"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "ruff format --quiet ${file_path} 2>/dev/null || true",
        "description": "자동 포맷팅"
      },
      {
        "matcher": "Edit|Write",
        "command": "echo '${file_path}' | grep -q 'routers/' && grep -n '^def ' '${file_path}' 2>/dev/null | head -5 | while read line; do echo \"⚠️ 동기 함수: $line\"; done; exit 0",
        "description": "동기 함수 경고"
      }
    ],
    "Stop": [
      {
        "command": "git diff --name-only HEAD | grep -q 'app/' && pytest -x -q --tb=line 2>/dev/null; exit 0",
        "description": "자동 테스트"
      }
    ]
  }
}
```

---

## 4. 커맨드 & 훅 설치 체크리스트

- [ ] `.claude/commands/` 디렉토리 생성
- [ ] 필요한 커맨드 .md 파일 복사
- [ ] `.claude/settings.json` 생성 (또는 수정)
- [ ] 훅에서 사용하는 도구 설치 확인 (`ruff`, `pytest`, `alembic`)
- [ ] `/help`로 등록된 커맨드 확인
- [ ] 각 커맨드 1회 테스트 실행
- [ ] 훅이 의도대로 동작하는지 확인 (파일 수정 후 포맷팅 등)
