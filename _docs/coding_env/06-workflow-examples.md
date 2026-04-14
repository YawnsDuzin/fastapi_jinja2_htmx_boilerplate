# 실전 워크플로우 예제

> 6가지 작업 시나리오별 **복붙용 프롬프트**. `[대괄호]` 부분을 프로젝트에 맞게 수정하세요.

---

## 시나리오 목록

| # | 시나리오 | 사용 에이전트 | 난이도 |
|---|---------|-------------|--------|
| 1 | [프로젝트 설계](#1-프로젝트-설계) | `fastapi-architect` | 중 |
| 2 | [코드 분석](#2-코드-분석) | `codebase-analyzer` + `async-inspector` | 낮 |
| 3 | [기능 개발 (단일)](#3-기능-개발--단일-에이전트) | `fastapi-dev` + `jinja-htmx-dev` | 중 |
| 4 | [기능 개발 (멀티)](#4-기능-개발--오케스트레이터) | `feature-orchestrator` | 높 |
| 5 | [버그 수정](#5-버그-수정) | `error-debugger` + `fastapi-dev` | 중 |
| 6 | [코드 리뷰](#6-코드-리뷰) | `code-reviewer` + `security-auditor` | 낮 |

---

## 1. 프로젝트 설계

### 목적
새 프로젝트 또는 새 기능의 아키텍처를 설계합니다.

### 프롬프트

```
@fastapi-architect

목적: [한 줄 — 예: "사내 장비 관리 시스템 MVP"]

기술 스택:
- FastAPI 0.115+ (async)
- Jinja2 + HTMX 2.0 (SSR + 동적 UI)
- Alpine.js 3.x (클라이언트 상호작용)
- TailwindCSS 3.4+ (CDN)
- SQLAlchemy 2.0+ (async ORM)
- python-jose (JWT 인증)

요구사항:
- [요구사항 1 — 예: "장비 등록/수정/삭제/조회"]
- [요구사항 2 — 예: "사용자별 장비 대여 기록"]
- [요구사항 3 — 예: "관리자 대시보드"]

제약:
- 예상 사용자: [예: DAU 100, 피크 RPS 5]
- 인증: JWT + HttpOnly 쿠키
- DB: [예: SQLite (개발) / PostgreSQL (프로덕션)]

다음을 순서대로 산출:
1. 디렉토리 구조 (app/ 기준)
2. 도메인 엔티티 + ERD (Mermaid erDiagram)
3. API 엔드포인트 목록 (메서드/경로/입출력/인증)
4. 계층 다이어그램 (Mermaid flowchart: Router → Service → Model)
5. HTMX 페이지 목록 (전체 페이지 + partial fragment)
6. 리스크 Top 3 + 완화책

파일 수정은 하지 말고 텍스트로만 출력해라.
```

### 예상 산출물
- Mermaid ERD + 계층 다이어그램
- API 엔드포인트 10~20개 목록
- 페이지/fragment 구성표
- 리스크 분석

---

## 2. 코드 분석

### 목적
기존 코드베이스를 파악하거나 특정 모듈을 깊이 이해합니다.

### 프롬프트 A: 전체 구조 분석

```
@codebase-analyzer

읽기 전용 모드로 다음을 조사한다. 파일 수정 금지.

대상: app/ 전체
목표: [예: "보일러플레이트 구조를 파악하고 확장 포인트를 식별"]

출력:
1. 디렉토리 트리 (주요 파일 설명 포함)
2. 핵심 진입점 (main.py → 라우터 등록 → 미들웨어 체인)
3. 데이터 흐름 (Mermaid sequenceDiagram: 요청 → 라우터 → 서비스 → DB → 응답)
4. HTMX 흐름 (Mermaid sequenceDiagram: 브라우저 → HTMX 요청 → FastAPI → Jinja2 → partial 반환)
5. 현재 모델 목록 + 관계
6. 의존성 목록 (requirements.txt / pyproject.toml)
7. 확장 포인트: 새 기능 추가 시 수정해야 할 파일 목록
8. 위험 지점 Top 5
```

### 프롬프트 B: 비동기 패턴 점검

```
@async-inspector

읽기 전용. 파일 수정 금지.

대상: app/ 전체
목표: 비동기 패턴의 정확성을 점검

검사 항목:
1. 동기 블로킹 호출 (time.sleep, 동기 DB, 동기 파일 I/O)
2. await 누락
3. 세션 누수 (async with 없이 AsyncSession 사용)
4. SQLAlchemy lazy loading 경고 (async에서 lazy="select" 접근 시 에러)
5. 이벤트 루프 블로킹 (CPU 집약 작업)

출력: 파일:라인 + 문제 설명 + 수정 패턴
```

---

## 3. 기능 개발 — 단일 에이전트

### 목적
작은 기능을 빠르게 구현합니다 (파일 3~5개 수준).

### 프롬프트: API + UI 한 번에

```
다음 기능을 구현해라:

기능: [예: "사용자 프로필 페이지"]

요구사항:
- [GET /profile — 현재 사용자 프로필 표시]
- [PUT /api/v1/profile — 프로필 수정 (이름, 이메일)]
- [HTMX로 인라인 편집 (클릭 → 편집폼 → 저장 → 표시)]

참조:
- 기존 라우터 스타일: app/routers/auth.py
- 기존 템플릿 스타일: app/templates/pages/
- 기존 모델: app/models/user.py

구현 순서:
1. Pydantic 스키마 (app/schemas/profile.py)
2. 서비스 (app/services/profile_service.py)
3. 라우터 (app/routers/profile.py) — API + 페이지 라우트
4. 템플릿:
   - app/templates/pages/profile.html (전체 페이지)
   - app/templates/components/_profile-form.html (편집 폼 fragment)
   - app/templates/components/_profile-display.html (표시 fragment)
5. main.py에 라우터 등록

규칙:
- 모든 함수 async def
- HTMX 요청 분기 처리
- TailwindCSS 클래스만 사용
- 인증 필수 (Depends(get_current_user))
- 기존 코드 스타일을 따라라

구현 후 pytest로 기존 테스트가 깨지지 않는지 확인해라.
```

---

## 4. 기능 개발 — 오케스트레이터

### 목적
여러 계층에 걸친 큰 기능을 체계적으로 구현합니다.

### 프롬프트

```
@feature-orchestrator

기능: [예: "상품 관리 CRUD + 검색 + 페이지네이션"]

요구사항:
- AC-1: 관리자는 상품을 등록할 수 있다 (이름/가격/설명/카테고리/이미지URL)
- AC-2: 상품 목록을 페이지네이션으로 조회할 수 있다 (20개씩)
- AC-3: 상품을 이름/카테고리로 검색할 수 있다
- AC-4: 상품 상세를 조회할 수 있다
- AC-5: 관리자는 상품을 수정할 수 있다
- AC-6: 관리자는 상품을 삭제할 수 있다 (soft delete)
- AC-7: 일반 사용자는 조회만 가능
- AC-8: 비로그인 사용자도 목록/상세 조회 가능

DB:
- Product 테이블: id, name, price, description, category, image_url, is_deleted, created_at, updated_at
- Category enum: ELECTRONICS, CLOTHING, FOOD, OTHER

API:
- POST   /api/v1/products     (관리자)
- GET    /api/v1/products      (전체, 페이지네이션 + 검색)
- GET    /api/v1/products/{id} (전체)
- PUT    /api/v1/products/{id} (관리자)
- DELETE /api/v1/products/{id} (관리자, soft delete)

UI (HTMX):
- /products — 상품 목록 (검색바 + 카테고리 필터 + 무한 스크롤)
- /products/{id} — 상품 상세
- /admin/products — 관리 페이지 (CRUD 테이블)
- /admin/products/new — 등록 폼
- /admin/products/{id}/edit — 수정 폼

각 단계 완료 시 diff를 보여주고 내 승인을 기다려라.
테스트 커버리지 80% 이상.
```

---

## 5. 버그 수정

### 목적
보고된 버그를 체계적으로 추적하고 수정합니다.

### 프롬프트 A: 단순 버그

```
다음 버그를 수정해라:

증상: [예: "상품 수정 시 가격이 0으로 초기화됨"]
재현: [예: "PUT /api/v1/products/1 에 description만 보내면 price가 0이 됨"]
예상 동작: [예: "보내지 않은 필드는 기존 값 유지"]

수정 시 규칙:
1. 먼저 이 버그를 재현하는 테스트를 작성 (실패하는 상태)
2. 최소 범위로 수정
3. 테스트가 통과하는지 확인
4. 기존 테스트가 깨지지 않는지 확인

버그와 무관한 코드는 수정하지 마라.
```

### 프롬프트 B: 복잡한 버그 (오케스트레이터)

```
@bugfix-orchestrator

버그: [예: "동시에 같은 상품을 즐겨찾기하면 중복 레코드 생성"]

증상:
- 빠르게 즐겨찾기 버튼을 두 번 클릭하면 duplicate key 에러
- 또는 중복 레코드가 생성됨 (race condition)

재현 조건:
- 인증된 사용자
- 같은 상품에 대해 POST /api/v1/favorites를 거의 동시에 2번 호출
- 두 번째 요청이 첫 번째 커밋 전에 도착

환경: 개발 (SQLite에서는 재현 안 될 수 있음, PostgreSQL에서 재현)

가능한 원인 추측:
- unique constraint 미설정
- 또는 constraint 있지만 에러 처리 미흡
```

---

## 6. 코드 리뷰

### 목적
PR 또는 변경사항의 품질을 검증합니다.

### 프롬프트 A: 빠른 리뷰 (커맨드)

```
/review --staged
```

### 프롬프트 B: 상세 리뷰 (에이전트)

````
다음 변경을 3가지 관점에서 리뷰한다.

diff:
```
[git diff main...HEAD 결과 붙여넣기, 또는 "git diff main...HEAD 를 직접 실행해라"]
```

리뷰어:
1. **코드 품질**: 가독성/네이밍/로직/일관성
2. **보안**: OWASP Top 10 + JWT 안전성 + HTMX CSRF
3. **성능**: N+1 쿼리 / 동기 블로킹 / 불필요한 연산

FastAPI 스택 특화 체크:
- [ ] 모든 라우터 함수가 async def인가
- [ ] Depends()로 인증/DB 세션을 주입하는가
- [ ] HTMX partial에 <html>/<body> 태그가 없는가
- [ ] SQLAlchemy 쿼리에 eager loading이 필요한 곳에 적용되었는가
- [ ] Pydantic 스키마에 적절한 검증이 있는가
- [ ] JWT 토큰이 HttpOnly 쿠키로 관리되는가
- [ ] .env 값이 하드코딩되지 않았는가

출력:
- 각 이슈: 심각도 (🔴/🟡/🟢) + 파일:라인 + 설명 + 수정 제안
- 마지막: **머지 가능 / 조건부 / 반려** + 이유
- 칭찬 금지
````

---

## 7. 추가 활용 패턴

### HTMX 인터랙션 설계

```
@htmx-pattern

다음 UI 인터랙션을 HTMX + Alpine.js 패턴으로 설계해라:

인터랙션: [예: "댓글 작성 → 목록에 추가 → 폼 초기화 + 카운터 업데이트"]

현재 구조:
- 페이지: templates/pages/product-detail.html
- 댓글 목록: templates/components/_comment-list.html
- 댓글 폼: templates/components/_comment-form.html

산출물:
1. 시퀀스 다이어그램 (Mermaid)
2. HTML 코드 (HTMX + Alpine.js)
3. FastAPI 엔드포인트 스펙
4. 엣지 케이스 (빈 댓글, 인증 만료, 서버 에러)
```

### DB 스키마 변경

```
@sqlalchemy-dev

다음 스키마 변경을 구현해라:

변경: [예: "Product에 tags 필드 추가 (다대다 관계)"]

요구사항:
- Tag 모델 신규 생성 (id, name, slug)
- product_tags 연결 테이블
- Product.tags 관계 (selectinload)
- 기존 Product 관련 코드에 영향 최소화

구현 후:
1. @alembic-migration 으로 마이그레이션 생성
2. 마이그레이션 검증 (upgrade/downgrade)
3. 관련 Pydantic 스키마 업데이트
```

### 성능 최적화

```
@async-inspector
@performance-reviewer

대상: app/services/product_service.py

다음을 분석해라:
1. N+1 쿼리 패턴
2. 불필요한 await (이미 캐시된 결과)
3. 동기 블로킹 호출
4. 페이지네이션 최적화 기회
5. 캐싱 적용 가능 지점

각 문제에 대해:
- 현재 코드 (파일:라인)
- 문제 설명
- 수정된 코드
- 예상 개선 효과
```

---

## 시나리오별 에이전트 매핑 요약

| 시나리오 | 필수 에이전트 | 선택 에이전트 | 토큰 소모 |
|---------|------------|------------|----------|
| 설계 | `fastapi-architect` | - | 낮 |
| 분석 | `codebase-analyzer` | `async-inspector`, `dependency-mapper` | 낮 |
| 기능 (소) | `fastapi-dev`, `jinja-htmx-dev` | `pydantic-schema`, `tailwind-ui` | 중 |
| 기능 (대) | `feature-orchestrator` (전체) | - | 높 |
| 버그 (소) | `error-debugger` | `fastapi-dev` | 낮 |
| 버그 (대) | `bugfix-orchestrator` (전체) | - | 중 |
| 리뷰 | `code-reviewer` | `security-auditor`, `performance-reviewer` | 중 |
| UI 설계 | `htmx-pattern` | `tailwind-ui` | 낮 |
| DB 변경 | `sqlalchemy-dev` | `alembic-migration` | 낮 |
| 성능 | `async-inspector` | `performance-reviewer` | 낮 |
