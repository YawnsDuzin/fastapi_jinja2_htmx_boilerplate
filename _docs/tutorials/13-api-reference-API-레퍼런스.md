# API 레퍼런스

이 문서는 FastAPI + HTMX 보일러플레이트의 모든 API 엔드포인트를 설명합니다.

## API 개요

### 기본 URL

| 환경 | URL |
|------|-----|
| 개발 | `http://localhost:8001` |
| 프로덕션 | `https://your-domain.com` |

### 인증 방식

이 API는 **JWT 토큰**을 사용하며, **httpOnly 쿠키**에 저장됩니다.

```
┌─────────────────────────────────────────────────────────────┐
│                       인증 흐름                              │
├─────────────────────────────────────────────────────────────┤
│  1. POST /api/v1/auth/login → JWT 토큰 발급 (쿠키 저장)     │
│  2. 이후 요청 → 브라우저가 자동으로 쿠키 전송               │
│  3. POST /api/v1/auth/logout → 쿠키 삭제                    │
└─────────────────────────────────────────────────────────────┘
```

### 응답 형식

**성공 응답:**
```json
{
  "id": 1,
  "title": "아이템",
  ...
}
```

**에러 응답:**
```json
{
  "detail": "에러 메시지"
}
```

**검증 에러 (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 1. 인증 API (`/api/v1/auth`)

### 1.1 회원가입

새로운 사용자 계정을 생성합니다.

```
POST /api/v1/auth/register
```

**Request Body:**

| 필드 | 타입 | 필수 | 설명 | 제약 조건 |
|------|------|------|------|----------|
| `email` | string | ✅ | 이메일 주소 | 유효한 이메일 형식 |
| `username` | string | ✅ | 사용자명 | 3-50자, 영문/숫자/언더스코어 |
| `password` | string | ✅ | 비밀번호 | 최소 8자 |
| `full_name` | string | ❌ | 전체 이름 | 최대 100자 |

**예시:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**성공 응답 (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-01-17T12:00:00Z",
  "updated_at": null
}
```

**에러 응답:**

| 상태 코드 | 설명 | 응답 |
|----------|------|------|
| 409 | 이메일 중복 | `{"detail": "이미 등록된 이메일입니다"}` |
| 409 | 사용자명 중복 | `{"detail": "이미 사용 중인 사용자명입니다"}` |
| 422 | 검증 실패 | Pydantic 검증 에러 |

**curl 예시:**

```bash
# Linux/macOS
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "johndoe", "password": "password123"}'
```

```powershell
# Windows PowerShell
Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/register" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email": "user@example.com", "username": "johndoe", "password": "password123"}'
```

---

### 1.2 로그인

사용자 인증 후 JWT 토큰을 발급합니다.

```
POST /api/v1/auth/login
```

**Request Body:**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `email` | string | ✅ | 이메일 주소 |
| `password` | string | ✅ | 비밀번호 |

**예시:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**성공 응답 (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**응답 헤더 (쿠키 설정):**
```
Set-Cookie: access_token=eyJ...; HttpOnly; Path=/; SameSite=Lax; Max-Age=1800
```

**에러 응답:**

| 상태 코드 | 설명 | 응답 |
|----------|------|------|
| 401 | 잘못된 자격 증명 | `{"detail": "이메일 또는 비밀번호가 올바르지 않습니다"}` |
| 401 | 비활성화된 계정 | `{"detail": "계정이 비활성화되었습니다"}` |

**curl 예시:**

```bash
# 쿠키 저장하여 로그인
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  -c cookies.txt

# 저장된 쿠키로 인증된 요청
curl http://localhost:8001/api/v1/auth/me -b cookies.txt
```

---

### 1.3 로그아웃

JWT 토큰을 무효화하고 쿠키를 삭제합니다.

```
POST /api/v1/auth/logout
```

**인증:** 필요

**성공 응답 (200 OK):**
```json
{
  "message": "로그아웃되었습니다"
}
```

**응답 헤더:**
```
Set-Cookie: access_token=; HttpOnly; Path=/; Max-Age=0
```

---

### 1.4 현재 사용자 정보

현재 로그인된 사용자의 정보를 반환합니다.

```
GET /api/v1/auth/me
```

**인증:** 필요

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-01-17T12:00:00Z",
  "updated_at": "2025-01-17T14:30:00Z"
}
```

**에러 응답:**

| 상태 코드 | 설명 | 응답 |
|----------|------|------|
| 401 | 미인증 | `{"detail": "인증이 필요합니다"}` |
| 401 | 토큰 만료 | `{"detail": "토큰이 만료되었습니다"}` |

---

### 1.5 비밀번호 변경

현재 사용자의 비밀번호를 변경합니다.

```
POST /api/v1/auth/change-password
```

**인증:** 필요

**Request Body:**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `current_password` | string | ✅ | 현재 비밀번호 |
| `new_password` | string | ✅ | 새 비밀번호 (최소 8자) |

**예시:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newsecurepassword456"
}
```

**성공 응답 (200 OK):**
```json
{
  "message": "비밀번호가 변경되었습니다"
}
```

**에러 응답:**

| 상태 코드 | 설명 |
|----------|------|
| 400 | 현재 비밀번호 불일치 |
| 422 | 새 비밀번호 검증 실패 |

---

## 2. 사용자 API (`/api/v1/users`)

### 2.1 프로필 조회

현재 사용자의 프로필을 조회합니다.

```
GET /api/v1/users/me
```

**인증:** 필요

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "bio": "소프트웨어 개발자입니다",
  "avatar_url": null,
  "is_active": true,
  "created_at": "2025-01-17T12:00:00Z",
  "updated_at": "2025-01-17T14:30:00Z"
}
```

---

### 2.2 프로필 수정

현재 사용자의 프로필을 수정합니다.

```
PATCH /api/v1/users/me
```

**인증:** 필요

**Request Body:** (모든 필드 선택적)

| 필드 | 타입 | 설명 |
|------|------|------|
| `username` | string | 사용자명 (3-50자) |
| `full_name` | string | 전체 이름 |
| `bio` | string | 자기소개 (최대 500자) |

**예시:**
```json
{
  "full_name": "John Smith",
  "bio": "풀스택 개발자입니다"
}
```

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Smith",
  "bio": "풀스택 개발자입니다",
  ...
}
```

---

## 3. 아이템 API (`/api/v1/items`)

### 3.1 아이템 목록 조회

현재 사용자의 아이템 목록을 조회합니다.

```
GET /api/v1/items
```

**인증:** 필요

**Query Parameters:**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `skip` | integer | 0 | 건너뛸 개수 (offset) |
| `limit` | integer | 20 | 조회 개수 (최대 100) |
| `search` | string | - | 제목/설명 검색어 |
| `is_active` | boolean | - | 활성 상태 필터 |

**예시 요청:**
```
GET /api/v1/items?skip=0&limit=10&search=할일&is_active=true
```

**성공 응답 (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "할일 아이템",
      "description": "설명입니다",
      "is_active": true,
      "owner_id": 1,
      "created_at": "2025-01-17T12:00:00Z",
      "updated_at": null
    },
    {
      "id": 2,
      "title": "두번째 할일",
      ...
    }
  ],
  "total": 25,
  "skip": 0,
  "limit": 10
}
```

---

### 3.2 아이템 상세 조회

특정 아이템의 상세 정보를 조회합니다.

```
GET /api/v1/items/{item_id}
```

**인증:** 필요

**Path Parameters:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `item_id` | integer | 아이템 ID |

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "title": "아이템 제목",
  "description": "상세 설명입니다",
  "is_active": true,
  "owner_id": 1,
  "created_at": "2025-01-17T12:00:00Z",
  "updated_at": "2025-01-17T14:30:00Z"
}
```

**에러 응답:**

| 상태 코드 | 설명 |
|----------|------|
| 404 | 아이템을 찾을 수 없음 |
| 403 | 접근 권한 없음 (다른 사용자의 아이템) |

---

### 3.3 아이템 생성

새로운 아이템을 생성합니다.

```
POST /api/v1/items
```

**인증:** 필요

**Request Body:**

| 필드 | 타입 | 필수 | 설명 | 제약 조건 |
|------|------|------|------|----------|
| `title` | string | ✅ | 아이템 제목 | 1-200자 |
| `description` | string | ❌ | 설명 | 최대 5000자 |

**예시:**
```json
{
  "title": "새로운 아이템",
  "description": "이것은 새로운 아이템입니다"
}
```

**성공 응답 (201 Created):**
```json
{
  "id": 3,
  "title": "새로운 아이템",
  "description": "이것은 새로운 아이템입니다",
  "is_active": true,
  "owner_id": 1,
  "created_at": "2025-01-17T15:00:00Z",
  "updated_at": null
}
```

**curl 예시:**

```bash
curl -X POST http://localhost:8001/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"title": "새 아이템", "description": "설명"}' \
  -b cookies.txt
```

---

### 3.4 아이템 수정

기존 아이템을 수정합니다.

```
PATCH /api/v1/items/{item_id}
```

**인증:** 필요 (소유자만 가능)

**Path Parameters:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `item_id` | integer | 아이템 ID |

**Request Body:** (모든 필드 선택적)

| 필드 | 타입 | 설명 |
|------|------|------|
| `title` | string | 아이템 제목 |
| `description` | string | 설명 |
| `is_active` | boolean | 활성 상태 |

**예시:**
```json
{
  "title": "수정된 제목",
  "is_active": false
}
```

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "title": "수정된 제목",
  "description": "기존 설명",
  "is_active": false,
  "owner_id": 1,
  "created_at": "2025-01-17T12:00:00Z",
  "updated_at": "2025-01-17T16:00:00Z"
}
```

---

### 3.5 아이템 삭제

아이템을 삭제합니다.

```
DELETE /api/v1/items/{item_id}
```

**인증:** 필요 (소유자만 가능)

**Path Parameters:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `item_id` | integer | 아이템 ID |

**성공 응답 (200 OK):**
```json
{
  "message": "아이템이 삭제되었습니다"
}
```

**에러 응답:**

| 상태 코드 | 설명 |
|----------|------|
| 404 | 아이템을 찾을 수 없음 |
| 403 | 삭제 권한 없음 |

---

### 3.6 아이템 활성 상태 토글

아이템의 활성/비활성 상태를 토글합니다.

```
POST /api/v1/items/{item_id}/toggle
```

**인증:** 필요 (소유자만 가능)

**성공 응답 (200 OK):**
```json
{
  "id": 1,
  "title": "아이템",
  "is_active": false,
  ...
}
```

---

## 4. HTMX 파셜 엔드포인트 (`/partials`)

파셜 엔드포인트는 HTML 조각을 반환하며, HTMX와 함께 사용됩니다.

### 4.1 아이템 파셜

| 메서드 | 엔드포인트 | 설명 | 응답 |
|--------|-----------|------|------|
| `GET` | `/partials/items` | 아이템 목록 HTML | HTML 조각 |
| `GET` | `/partials/items/form` | 아이템 생성 폼 | 모달용 HTML |
| `GET` | `/partials/items/{id}` | 단일 아이템 HTML | HTML 조각 |
| `GET` | `/partials/items/{id}/edit` | 아이템 수정 폼 | 모달용 HTML |
| `POST` | `/partials/items` | 아이템 생성 | HTML + HX-Trigger |
| `PUT` | `/partials/items/{id}` | 아이템 수정 | HTML + HX-Trigger |
| `DELETE` | `/partials/items/{id}` | 아이템 삭제 | 빈 HTML + HX-Trigger |

### 4.2 HX-Trigger 헤더

파셜 응답에는 클라이언트 이벤트를 트리거하는 헤더가 포함될 수 있습니다.

**성공 시:**
```
HX-Trigger: {"showToast": {"type": "success", "message": "아이템이 생성되었습니다"}, "closeModal": true}
```

**에러 시:**
```
HX-Trigger: {"showToast": {"type": "error", "message": "오류가 발생했습니다"}}
```

### 4.3 파셜 사용 예시

```html
<!-- 아이템 목록 새로고침 -->
<button
    hx-get="/partials/items"
    hx-target="#item-list"
    hx-swap="innerHTML">
    새로고침
</button>

<!-- 아이템 생성 모달 -->
<button
    hx-get="/partials/items/form"
    hx-target="#modal-container"
    hx-swap="innerHTML">
    + 새 아이템
</button>

<!-- 폼 제출 -->
<form
    hx-post="/partials/items"
    hx-target="#item-list"
    hx-swap="innerHTML">
    <input type="text" name="title" required>
    <button type="submit">생성</button>
</form>

<!-- 아이템 삭제 -->
<button
    hx-delete="/partials/items/1"
    hx-target="closest .item"
    hx-swap="outerHTML"
    hx-confirm="정말 삭제하시겠습니까?">
    삭제
</button>
```

---

## 5. 에러 응답 상세

### 5.1 HTTP 상태 코드

| 코드 | 이름 | 설명 |
|------|------|------|
| 200 | OK | 성공 |
| 201 | Created | 리소스 생성 성공 |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스 없음 |
| 409 | Conflict | 리소스 충돌 |
| 422 | Unprocessable Entity | 검증 실패 |
| 500 | Internal Server Error | 서버 오류 |

### 5.2 에러 응답 형식

**일반 에러:**
```json
{
  "detail": "에러 메시지"
}
```

**검증 에러 (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "필드명"],
      "msg": "에러 메시지",
      "type": "에러 타입"
    }
  ]
}
```

### 5.3 일반적인 에러 코드

| 에러 타입 | 설명 |
|----------|------|
| `value_error.email` | 유효하지 않은 이메일 |
| `value_error.missing` | 필수 필드 누락 |
| `string_too_short` | 문자열 길이 부족 |
| `string_too_long` | 문자열 길이 초과 |
| `type_error.integer` | 정수 타입 불일치 |

---

## 6. Rate Limiting (속도 제한)

### 6.1 기본 제한

| 엔드포인트 | 제한 |
|-----------|------|
| 인증 API | 5회/분 |
| 일반 API | 100회/분 |
| 파셜 | 200회/분 |

### 6.2 제한 초과 응답

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "detail": "요청 횟수를 초과했습니다. 잠시 후 다시 시도해주세요."
}
```

---

## 7. OpenAPI 문서

개발 모드에서 자동 생성되는 인터랙티브 API 문서:

| URL | 설명 |
|-----|------|
| `http://localhost:8001/docs` | Swagger UI - 인터랙티브 테스트 가능 |
| `http://localhost:8001/redoc` | ReDoc - 문서 보기 용이 |
| `http://localhost:8001/openapi.json` | OpenAPI 3.0 스키마 (JSON) |

### 7.1 Swagger UI 사용법

1. 브라우저에서 `http://localhost:8001/docs` 접속
2. "Authorize" 버튼 클릭 (로그인 필요 시)
3. 엔드포인트 클릭하여 펼치기
4. "Try it out" 버튼 클릭
5. 파라미터 입력 후 "Execute" 클릭
6. 응답 확인

### 7.2 프로덕션에서 문서 비활성화

`.env` 파일:
```env
DEBUG=false
```

또는 `app/main.py`에서:
```python
app = FastAPI(
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)
```

---

## 8. API 버전 관리

### 8.1 현재 버전

현재 API 버전은 `v1`입니다.

```
/api/v1/auth/...
/api/v1/users/...
/api/v1/items/...
```

### 8.2 버전 정책

- **마이너 변경**: 기존 버전에 추가 (하위 호환)
- **메이저 변경**: 새 버전 생성 (`/api/v2/`)
- **지원 중단**: 최소 6개월 전 공지

---

## 9. 다음 단계

- 🏗️ [아키텍처](./08-architecture-아키텍처-설명.md) - 시스템 구조 이해
- 🔧 [개발 환경 설정](./10-development-setup-개발-환경-설정.md) - 도구 설정
