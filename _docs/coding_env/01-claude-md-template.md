# CLAUDE.md 템플릿 — FastAPI + HTMX 스택

> 프로젝트 루트에 `CLAUDE.md`로 복사하여 사용합니다.  
> `[대괄호]` 부분을 프로젝트에 맞게 수정하세요.

---

## 템플릿 본문

아래 코드 블록 전체를 `CLAUDE.md`로 저장합니다.

````markdown
# CLAUDE.md

## 프로젝트 개요

[프로젝트 한 줄 설명 — 예: "사내 업무 관리 대시보드"]

- **스택**: FastAPI 0.115+ / Jinja2 3.1+ / HTMX 2.0+ / Alpine.js 3.x / TailwindCSS 3.4+ (CDN) / SQLAlchemy 2.0+ (async) / python-jose (JWT)
- **Python**: 3.11+
- **패키지 관리**: [pip / poetry / uv]
- **배포**: [Docker / 직접 배포 / 클라우드 서비스명]

---

## 디렉토리 구조

```
[프로젝트명]/
├── app/
│   ├── main.py              # FastAPI 앱 팩토리
│   ├── config.py            # 환경 설정 (pydantic-settings)
│   ├── database.py          # SQLAlchemy async engine/session
│   ├── models/              # SQLAlchemy ORM 모델
│   │   ├── __init__.py
│   │   ├── base.py          # DeclarativeBase
│   │   └── user.py
│   ├── schemas/             # Pydantic 스키마 (request/response)
│   │   └── user.py
│   ├── routers/             # APIRouter 모듈
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── pages.py         # Jinja2 HTML 라우트
│   ├── services/            # 비즈니스 로직
│   │   └── auth_service.py
│   ├── dependencies.py      # Depends() 의존성
│   ├── templates/           # Jinja2 템플릿
│   │   ├── base.html
│   │   ├── components/      # HTMX partial fragments
│   │   └── pages/
│   └── static/              # CSS/JS/이미지
├── alembic/                 # DB 마이그레이션
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py          # pytest fixture (async client, test DB)
│   ├── test_auth.py
│   └── test_[기능].py
├── alembic.ini
├── pyproject.toml           # 또는 requirements.txt
├── .env                     # 환경변수 (커밋 금지)
└── CLAUDE.md
```

---

## 기술 스택 상세 규칙

### FastAPI
- 모든 엔드포인트는 **async def** 사용
- 라우터는 `app/routers/`에 기능별 파일로 분리
- 의존성 주입은 `app/dependencies.py`에서 관리
- 예외 처리는 `HTTPException` 사용, 커스텀 예외는 `app/exceptions.py`
- API 라우트 접두사: `/api/v1/`
- 페이지 라우트 접두사: `/` (Jinja2 HTML 반환)

### Jinja2 + HTMX
- 기본 레이아웃: `templates/base.html` (TailwindCSS CDN + HTMX 스크립트 포함)
- **HTMX partial fragment**: `templates/components/` 에 배치
- HTMX 요청 감지: `request.headers.get("HX-Request")`
  - HX-Request가 있으면 → partial fragment 반환
  - HX-Request가 없으면 → 전체 페이지 반환
- HTMX 속성 패턴:
  ```html
  hx-get="/api/v1/items"
  hx-target="#item-list"
  hx-swap="innerHTML"
  hx-indicator="#spinner"
  ```

### Alpine.js
- 클라이언트 상태 관리에만 사용 (서버 상태는 HTMX)
- `x-data`, `x-show`, `x-on` 등 인라인 디렉티브 사용
- 복잡한 로직은 `Alpine.store()` 또는 `Alpine.data()` 로 분리
- Alpine.js와 HTMX 이벤트 연동: `@htmx:after-swap`

### TailwindCSS
- CDN 방식 사용 (`<script src="https://cdn.tailwindcss.com">`)
- 커스텀 설정이 필요하면 `<script>tailwind.config = {...}</script>` 인라인
- 컴포넌트 스타일 재사용: Jinja2 매크로 또는 `{% include %}` 활용

### SQLAlchemy (Async)
- `async_sessionmaker` + `AsyncSession` 사용
- 모델 정의: `app/models/` (DeclarativeBase 상속)
- 관계 정의: `relationship()` + `Mapped[]` 타입 힌트
- 쿼리 패턴:
  ```python
  async with async_session() as session:
      result = await session.execute(select(User).where(User.id == user_id))
      user = result.scalar_one_or_none()
  ```
- **N+1 방지**: `selectinload()` 또는 `joinedload()` 명시
- 마이그레이션: Alembic (`alembic revision --autogenerate`)

### 인증 (python-jose + JWT)
- JWT 생성/검증: `app/services/auth_service.py`
- 토큰 저장: HttpOnly 쿠키 (localStorage 사용 금지)
- 의존성: `get_current_user = Depends(oauth2_scheme)`
- 비밀번호 해싱: passlib + bcrypt

---

## 코딩 컨벤션

- **포매터**: [ruff format / black]
- **린터**: [ruff / flake8]
- **타입 체크**: [mypy / pyright] (선택)
- **테스트**: pytest + pytest-asyncio + httpx (AsyncClient)
- **네이밍**:
  - 파일/변수/함수: `snake_case`
  - 클래스: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`
  - Jinja2 템플릿: `kebab-case.html`
  - HTMX fragment: `_partial-name.html` (언더스코어 접두사)
- **Import 순서**: stdlib → 서드파티 → 로컬
- **독스트링**: Google 스타일 (함수/클래스에 작성)

---

## 자주 쓰는 명령어

```bash
# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 테스트
pytest -v --tb=short
pytest tests/test_auth.py -v  # 특정 파일

# 린트 & 포맷
ruff check app/
ruff format app/

# DB 마이그레이션
alembic revision --autogenerate -m "설명"
alembic upgrade head
alembic downgrade -1

# 의존성
pip install -r requirements.txt  # 또는 poetry install / uv sync
```

---

## 금지 사항

- `.env` 파일을 절대 커밋하지 마라
- `sync` SQLAlchemy 세션을 사용하지 마라 (반드시 async)
- HTMX 요청에 전체 페이지를 반환하지 마라 (partial fragment만)
- Alpine.js에서 서버 데이터를 직접 fetch하지 마라 (HTMX 사용)
- 인라인 `<style>` 태그를 사용하지 마라 (TailwindCSS 클래스 사용)
- JWT 토큰을 localStorage에 저장하지 마라 (HttpOnly 쿠키)
- `SELECT *` 쿼리를 사용하지 마라 (명시적 컬럼 선택)

---

## PR / 커밋 규칙

- 커밋 메시지: `type: 한글 설명` (feat / fix / refactor / docs / test / chore)
- PR은 하나의 기능/수정 단위로 작성
- 테스트 통과 확인 후 커밋
````

---

## 커스터마이즈 체크리스트

CLAUDE.md를 프로젝트에 배치한 후 다음을 확인/수정합니다:

- [ ] `[대괄호]` 플레이스홀더를 모두 실제 값으로 교체
- [ ] 디렉토리 구조를 실제 프로젝트와 일치시킴
- [ ] 패키지 관리 도구 확정 (pip / poetry / uv)
- [ ] 포매터/린터 확정 (ruff / black / flake8)
- [ ] 배포 환경 명시
- [ ] 프로젝트별 금지 사항 추가
- [ ] 테스트 실행 명령어 확인
