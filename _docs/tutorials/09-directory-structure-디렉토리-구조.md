# 디렉토리 구조

이 문서는 프로젝트의 전체 파일/폴더 구조와 각 파일의 역할을 상세히 설명합니다.

## 1. 전체 프로젝트 구조

```
fastapi-htmx-boilerplate/
│
├── 📁 app/                        # 🔷 애플리케이션 메인 패키지
│   ├── __init__.py               # 패키지 초기화, 버전 정보
│   ├── main.py                   # FastAPI 앱 엔트리포인트
│   │
│   ├── 📁 api/                   # REST API 라우터
│   │   ├── __init__.py
│   │   ├── deps.py               # ⭐ 공통 의존성 (인증, DB 세션)
│   │   └── 📁 v1/                # API 버전 1
│   │       ├── __init__.py       # 라우터 통합
│   │       ├── auth.py           # 인증 엔드포인트
│   │       ├── users.py          # 사용자 엔드포인트
│   │       └── items.py          # 아이템 엔드포인트
│   │
│   ├── 📁 pages/                 # HTML 페이지 라우터
│   │   ├── __init__.py           # 라우터 통합
│   │   ├── home.py               # 홈, 소개 페이지
│   │   ├── auth.py               # 로그인/회원가입 페이지
│   │   └── dashboard.py          # 대시보드, 아이템 페이지
│   │
│   ├── 📁 partials/              # HTMX 파셜 라우터
│   │   ├── __init__.py           # 라우터 통합
│   │   ├── items.py              # 아이템 CRUD 파셜
│   │   ├── modals.py             # 모달 파셜
│   │   └── toasts.py             # 토스트 알림 파셜
│   │
│   ├── 📁 models/                # SQLAlchemy ORM 모델
│   │   ├── __init__.py           # 모델 export
│   │   ├── base.py               # 베이스 모델, 믹스인
│   │   ├── user.py               # 사용자 모델
│   │   └── item.py               # 아이템 모델
│   │
│   ├── 📁 schemas/               # Pydantic 스키마
│   │   ├── __init__.py           # 스키마 export
│   │   ├── common.py             # 공통 스키마 (페이지네이션 등)
│   │   ├── auth.py               # 인증 스키마
│   │   ├── user.py               # 사용자 스키마
│   │   └── item.py               # 아이템 스키마
│   │
│   ├── 📁 services/              # 비즈니스 로직
│   │   ├── __init__.py           # 서비스 export
│   │   ├── auth.py               # 인증 서비스
│   │   ├── user.py               # 사용자 서비스
│   │   └── item.py               # 아이템 서비스
│   │
│   └── 📁 core/                  # 핵심 유틸리티
│       ├── __init__.py
│       ├── config.py             # ⭐ 환경 설정 (Pydantic Settings)
│       ├── database.py           # ⭐ DB 연결 설정
│       ├── security.py           # JWT, 비밀번호 해싱
│       ├── exceptions.py         # 커스텀 예외
│       └── templating.py         # Jinja2 설정
│
├── 📁 templates/                 # 🔷 Jinja2 템플릿
│   ├── base.html                 # ⭐ 기본 레이아웃
│   │
│   ├── 📁 components/            # 재사용 컴포넌트
│   │   ├── navbar.html           # 네비게이션 바
│   │   ├── sidebar.html          # 사이드바
│   │   ├── footer.html           # 푸터
│   │   ├── modal.html            # 모달 컴포넌트
│   │   └── toast.html            # 토스트 컴포넌트
│   │
│   ├── 📁 pages/                 # 전체 페이지 템플릿
│   │   ├── home.html             # 홈페이지
│   │   ├── about.html            # 소개 페이지
│   │   ├── login.html            # 로그인
│   │   ├── register.html         # 회원가입
│   │   ├── dashboard.html        # 대시보드
│   │   ├── items/
│   │   │   ├── index.html        # 아이템 목록
│   │   │   └── detail.html       # 아이템 상세
│   │   ├── profile.html          # 프로필
│   │   ├── settings.html         # 설정
│   │   ├── 404.html              # 404 에러 페이지
│   │   └── 500.html              # 500 에러 페이지
│   │
│   └── 📁 partials/              # HTMX 파셜 템플릿
│       ├── 📁 items/
│       │   ├── list.html         # 아이템 목록
│       │   ├── item.html         # 단일 아이템
│       │   ├── form.html         # 생성/수정 폼
│       │   └── empty.html        # 빈 상태
│       ├── 📁 modals/
│       │   ├── confirm.html      # 확인 모달
│       │   ├── alert.html        # 알림 모달
│       │   └── form.html         # 폼 모달
│       └── 📁 toasts/
│           ├── success.html      # 성공 토스트
│           ├── error.html        # 에러 토스트
│           ├── info.html         # 정보 토스트
│           └── warning.html      # 경고 토스트
│
├── 📁 static/                    # 🔷 정적 파일
│   ├── 📁 css/
│   │   └── custom.css            # 커스텀 스타일
│   ├── 📁 js/
│   │   └── app.js                # 앱 JavaScript
│   └── 📁 img/                   # 이미지
│       ├── logo.svg
│       └── favicon.ico
│
├── 📁 tests/                     # 🔷 테스트
│   ├── __init__.py
│   ├── conftest.py               # ⭐ 테스트 설정, 픽스처
│   ├── 📁 test_api/
│   │   ├── __init__.py
│   │   ├── test_auth.py          # 인증 API 테스트
│   │   ├── test_users.py         # 사용자 API 테스트
│   │   └── test_items.py         # 아이템 API 테스트
│   ├── 📁 test_pages/
│   │   ├── __init__.py
│   │   └── test_home.py          # 페이지 테스트
│   └── 📁 test_services/
│       ├── __init__.py
│       └── test_item.py          # 서비스 테스트
│
├── 📁 alembic/                   # 🔷 DB 마이그레이션
│   ├── env.py                    # Alembic 환경 설정
│   ├── script.py.mako            # 마이그레이션 템플릿
│   └── 📁 versions/              # 마이그레이션 파일들
│       └── 001_initial.py
│
├── 📁 docs/                      # 🔷 문서
│   ├── README.md                 # 문서 인덱스
│   ├── 01-project-overview.md
│   ├── 02-quick-start.md
│   └── ...
│
├── 📄 .env.example               # 환경변수 예시
├── 📄 .env                       # 환경변수 (git 무시)
├── 📄 .gitignore                 # Git 무시 파일
├── 📄 .dockerignore              # Docker 무시 파일
├── 📄 alembic.ini                # Alembic 설정
├── 📄 Dockerfile                 # Docker 이미지 빌드
├── 📄 docker-compose.yml         # Docker Compose 설정
├── 📄 pyproject.toml             # 프로젝트 메타데이터 (Black, Ruff 등)
├── 📄 requirements.txt           # 프로덕션 의존성
├── 📄 requirements-dev.txt       # 개발 의존성
├── 📄 run.py                     # 개발 서버 실행 스크립트
├── 📄 CLAUDE.md                  # Claude Code 가이드
└── 📄 README.md                  # 프로젝트 README
```

## 2. 주요 파일 상세 설명

### 2.1 애플리케이션 엔트리포인트

#### `app/main.py` - FastAPI 앱 생성

```python
"""
FastAPI 애플리케이션 메인 엔트리포인트

역할:
1. FastAPI 앱 인스턴스 생성
2. 미들웨어 등록 (CORS, GZip 등)
3. 라우터 등록 (API, Pages, Partials)
4. 예외 핸들러 등록
5. 정적 파일 마운트
6. 시작/종료 이벤트 처리
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import api_router
from app.pages import pages_router
from app.partials import partials_router
from app.core.config import settings

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI + Jinja2 + HTMX 보일러플레이트",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # 프로덕션에서 API 문서 숨김
    redoc_url="/redoc" if settings.DEBUG else None,
)

# 미들웨어 등록
# ... CORS, GZip, 세션 등

# 라우터 등록
app.include_router(api_router, prefix="/api/v1")
app.include_router(pages_router)
app.include_router(partials_router, prefix="/partials")

# 정적 파일
app.mount("/static", StaticFiles(directory="static"), name="static")
```

#### `run.py` - 개발 서버 실행

```python
"""
개발 서버 실행 스크립트

- 직접 실행: python run.py
- uvicorn으로 실행: uvicorn app.main:app --reload --port 8001
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # 코드 변경 시 자동 재시작
    )
```

### 2.2 핵심 설정 파일

#### `app/config.py` - 환경 설정

```python
"""
환경 설정 관리

- Pydantic Settings 사용
- .env 파일에서 환경 변수 로드
- 타입 검증 및 기본값 설정
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 앱 설정
    APP_NAME: str = "FastAPI-HTMX-Boilerplate"
    APP_ENV: str = "development"  # development, production, testing
    DEBUG: bool = True

    # 보안
    SECRET_KEY: str = "change-me-in-production"
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 데이터베이스
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

settings = Settings()
```

#### `app/database.py` - 데이터베이스 설정

```python
"""
SQLAlchemy 비동기 데이터베이스 설정

- AsyncEngine 생성
- AsyncSession 팩토리
- 의존성 주입용 get_db 함수
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL 로깅 (개발 모드에서만)
    pool_pre_ping=True,   # 연결 유효성 검사
)

# 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 의존성 주입용
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### 2.3 의존성 주입

#### `app/api/deps.py` - 공통 의존성

```python
"""
공통 의존성 정의

이 파일에서 정의된 의존성은 라우터에서 Depends()로 주입됩니다.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User

# ============================================
# 데이터베이스 세션 의존성
# ============================================
DbSession = Annotated[AsyncSession, Depends(get_db)]

# ============================================
# 인증 의존성
# ============================================
async def get_current_user(
    db: DbSession,
    access_token: str | None = Cookie(default=None),
) -> User:
    """
    현재 인증된 사용자 반환 (필수)

    - 토큰 없음 → 401 Unauthorized
    - 토큰 무효 → 401 Unauthorized
    - 사용자 없음 → 401 Unauthorized
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다",
        )
    # ... 토큰 검증 및 사용자 조회
    return user

# 타입 별칭으로 사용
CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_user_optional(
    db: DbSession,
    access_token: str | None = Cookie(default=None),
) -> User | None:
    """
    현재 인증된 사용자 반환 (선택적)

    - 토큰 없거나 무효 → None 반환
    - 인증된 경우 → User 반환
    """
    if not access_token:
        return None
    # ...
    return user

CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
```

**라우터에서 사용 예시**:

```python
# 인증 필수
@router.get("/items")
async def get_items(
    current_user: CurrentUser,  # ← 인증 없으면 401
    db: DbSession,
):
    # current_user는 항상 User 객체
    ...

# 인증 선택
@router.get("/")
async def home(
    current_user: CurrentUserOptional,  # ← 인증 없어도 OK
):
    # current_user는 User 또는 None
    if current_user:
        return f"안녕하세요, {current_user.username}님"
    return "안녕하세요, 게스트님"
```

### 2.4 라우터 구조

#### API 라우터 (`app/api/v1/`)

```
app/api/v1/
├── __init__.py       # 라우터 통합
├── auth.py          # POST /api/v1/auth/login, /register, /logout
├── users.py         # GET/PATCH /api/v1/users/me
└── items.py         # GET/POST/PATCH/DELETE /api/v1/items
```

**`app/api/v1/__init__.py`** - 라우터 통합:

```python
from fastapi import APIRouter
from app.api.v1 import auth, users, items

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
```

#### Pages 라우터 (`app/pages/`)

```
app/pages/
├── __init__.py       # 라우터 통합
├── home.py          # GET /, /about
├── auth.py          # GET /login, /register
└── dashboard.py     # GET /dashboard, /items, /profile
```

#### Partials 라우터 (`app/partials/`)

```
app/partials/
├── __init__.py       # 라우터 통합
├── items.py         # GET/POST/PATCH/DELETE /partials/items
├── modals.py        # 모달 HTML 반환
└── toasts.py        # 토스트 HTML 반환
```

### 2.5 모델과 스키마

#### `app/models/base.py` - 베이스 모델

```python
"""
모든 모델의 베이스 클래스

- 공통 타임스탬프 필드
- 공통 메서드
"""
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """모든 모델의 베이스"""
    pass

class TimestampMixin:
    """생성/수정 시간 자동 관리 믹스인"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
```

#### `app/models/user.py` - 사용자 모델

```python
"""
사용자 모델

테이블: users
역할: 인증, 프로필 정보 저장
"""
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # 관계
    items: Mapped[list["Item"]] = relationship(back_populates="owner")
```

#### `app/schemas/user.py` - 사용자 스키마

```python
"""
사용자 Pydantic 스키마

- 요청 데이터 검증
- 응답 데이터 직렬화
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# === 요청 스키마 ===
class UserCreate(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """프로필 수정 요청"""
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None

# === 응답 스키마 ===
class UserResponse(BaseModel):
    """사용자 정보 응답"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    is_active: bool
```

### 2.6 서비스 레이어

#### `app/services/item.py` - 아이템 서비스

```python
"""
아이템 비즈니스 로직

- CRUD 작업
- 비즈니스 규칙 적용
- DB 트랜잭션 관리
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, item_id: int) -> Item | None:
        """ID로 아이템 조회"""
        return await self.db.get(Item, item_id)

    async def get_by_owner(
        self,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Item]:
        """소유자의 아이템 목록 조회"""
        stmt = (
            select(Item)
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, item_in: ItemCreate, owner_id: int) -> Item:
        """아이템 생성"""
        item = Item(**item_in.model_dump(), owner_id=owner_id)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, item_in: ItemUpdate) -> Item:
        """아이템 수정"""
        for field, value in item_in.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        """아이템 삭제"""
        await self.db.delete(item)
        await self.db.commit()
```

### 2.7 템플릿 구조

#### `templates/base.html` - 기본 레이아웃

```html
<!DOCTYPE html>
<html lang="ko" x-data="{ darkMode: false }">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title | default('FastAPI-HTMX') }}{% endblock %}</title>

    <!-- TailwindCSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>

    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <!-- 커스텀 CSS -->
    <link rel="stylesheet" href="{{ url_for('static', path='css/custom.css') }}">

    {% block head %}{% endblock %}
</head>
<body class="bg-gray-50 dark:bg-gray-900">
    <!-- 네비게이션 -->
    {% include "components/navbar.html" %}

    <!-- 메인 컨텐츠 -->
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <!-- 푸터 -->
    {% include "components/footer.html" %}

    <!-- 토스트 컨테이너 -->
    {% include "components/toast.html" %}

    <!-- 커스텀 JS -->
    <script src="{{ url_for('static', path='js/app.js') }}"></script>

    {% block scripts %}{% endblock %}
</body>
</html>
```

#### 템플릿 상속 예시

**`templates/pages/items.html`**:

```html
{% extends "base.html" %}

{% block title %}내 아이템 - {{ super() }}{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">내 아이템</h1>

    <!-- 아이템 생성 버튼 -->
    <button
        hx-get="/partials/items/form"
        hx-target="#modal-container"
        class="btn btn-primary mb-4">
        + 새 아이템
    </button>

    <!-- 아이템 목록 (HTMX 타겟) -->
    <div id="item-list">
        {% include "partials/items/list.html" %}
    </div>
</div>

<!-- 모달 컨테이너 -->
<div id="modal-container"></div>
{% endblock %}
```

**`templates/partials/items/list.html`** (파셜):

```html
{# base.html 상속 없음 - 순수 HTML 조각 #}
{% if items %}
    <div class="space-y-4">
        {% for item in items %}
            {% include "partials/items/item.html" %}
        {% endfor %}
    </div>
{% else %}
    {% include "partials/items/empty.html" %}
{% endif %}
```

## 3. 명명 규칙

### 3.1 파일 명명

| 유형 | 규칙 | 예시 |
|------|------|------|
| **Python 모듈** | snake_case | `user_service.py`, `auth.py` |
| **테스트 파일** | test_ 접두사 | `test_auth.py`, `test_items.py` |
| **템플릿** | snake_case 또는 kebab-case | `forgot_password.html` |
| **정적 파일** | kebab-case | `custom.css`, `app.js` |

### 3.2 클래스 명명

| 유형 | 규칙 | 예시 |
|------|------|------|
| **모델** | PascalCase 단수형 | `User`, `Item`, `Comment` |
| **스키마** | PascalCase + 동작 | `UserCreate`, `ItemUpdate`, `ItemResponse` |
| **서비스** | PascalCase + Service | `AuthService`, `ItemService` |
| **예외** | PascalCase + Error/Exception | `NotFoundError`, `ValidationError` |

### 3.3 함수/메서드 명명

| 유형 | 규칙 | 예시 |
|------|------|------|
| **라우터** | 동사_목적어 | `get_items()`, `create_item()` |
| **서비스** | 동사(_by_조건) | `get()`, `get_by_email()`, `create()` |
| **의존성** | get_대상 | `get_db()`, `get_current_user()` |

### 3.4 변수 명명

| 유형 | 규칙 | 예시 |
|------|------|------|
| **일반 변수** | snake_case | `user_id`, `item_list` |
| **상수** | UPPER_SNAKE_CASE | `MAX_ITEMS`, `DEFAULT_PAGE_SIZE` |
| **타입 별칭** | PascalCase | `DbSession`, `CurrentUser` |

## 4. 폴더별 책임 요약

| 폴더 | 책임 | 의존 대상 |
|------|------|----------|
| `app/api/` | HTTP 요청 처리, JSON 응답 | services, schemas, deps |
| `app/pages/` | HTML 페이지 렌더링 | services, templates, deps |
| `app/partials/` | HTMX용 HTML 조각 렌더링 | services, templates, deps |
| `app/models/` | 데이터베이스 테이블 정의 | SQLAlchemy |
| `app/schemas/` | 데이터 검증, 직렬화 | Pydantic |
| `app/services/` | 비즈니스 로직 | models |
| `app/core/` | 공통 유틸리티 | 설정, 보안, 예외 |
| `templates/` | Jinja2 HTML 템플릿 | - |
| `static/` | CSS, JS, 이미지 | - |
| `tests/` | 테스트 코드 | pytest, app |
| `alembic/` | DB 마이그레이션 | SQLAlchemy |

## 5. 새 파일 추가 시 체크리스트

### 5.1 새 모델 추가

```
□ app/models/new_model.py 생성
□ app/models/__init__.py에 import 추가
□ alembic revision --autogenerate -m "add new_model"
□ alembic upgrade head
```

### 5.2 새 스키마 추가

```
□ app/schemas/new_schema.py 생성
□ app/schemas/__init__.py에 import 추가
```

### 5.3 새 서비스 추가

```
□ app/services/new_service.py 생성
□ app/services/__init__.py에 import 추가
```

### 5.4 새 API 엔드포인트 추가

```
□ app/api/v1/new_endpoint.py 생성
□ app/api/v1/__init__.py에 라우터 등록
□ tests/test_api/test_new_endpoint.py 테스트 작성
```

### 5.5 새 페이지 추가

```
□ app/pages/에 라우터 함수 추가 또는 새 파일 생성
□ templates/pages/new_page.html 생성
□ (필요시) templates/partials/new_page/ 폴더 생성
```

## 6. 다음 단계

- 🔧 [개발 환경 설정](./10-development-setup-개발-환경-설정.md) - IDE, 도구 설정
- 🏗️ [아키텍처](./08-architecture-아키텍처-설명.md) - 시스템 구조 이해
