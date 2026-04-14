# 개발 환경 설정

이 문서는 Windows, macOS, Linux, 라즈베리파이에서 개발 환경을 설정하는 방법을 상세히 설명합니다.

## 1. IDE/에디터 설정

### 1.1 Visual Studio Code (권장)

#### 설치

**Windows:**
```powershell
# winget으로 설치
winget install Microsoft.VisualStudioCode

# 또는 https://code.visualstudio.com/ 에서 다운로드
```

**macOS:**
```bash
# Homebrew로 설치
brew install --cask visual-studio-code

# 또는 공식 사이트에서 다운로드
```

**Linux (Ubuntu/Debian):**
```bash
# Snap으로 설치
sudo snap install code --classic

# 또는 APT로 설치
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64,arm64,armhf] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code
```

**라즈베리파이:**
```bash
# APT로 설치 (64비트 OS)
sudo apt update
sudo apt install code

# 또는 Code OSS (오픈소스 버전)
sudo apt install code-oss
```

#### 필수 확장 프로그램

| 확장 | 용도 | 설치 명령 |
|------|------|----------|
| **Python** | Python 지원 | `code --install-extension ms-python.python` |
| **Pylance** | 타입 검사, 자동완성 | `code --install-extension ms-python.vscode-pylance` |
| **Black Formatter** | 코드 포맷팅 | `code --install-extension ms-python.black-formatter` |
| **Ruff** | 빠른 린팅 | `code --install-extension charliermarsh.ruff` |
| **Python Test Explorer** | 테스트 UI | `code --install-extension LittleFoxTeam.vscode-python-test-adapter` |
| **Jinja** | Jinja2 문법 하이라이팅 | `code --install-extension wholroyd.jinja` |
| **HTMX Tags** | HTMX 속성 자동완성 | `code --install-extension otovo-oss.htmx-tags` |
| **Tailwind CSS IntelliSense** | TailwindCSS 자동완성 | `code --install-extension bradlc.vscode-tailwindcss` |

**한 번에 설치:**
```bash
code --install-extension ms-python.python \
     --install-extension ms-python.vscode-pylance \
     --install-extension ms-python.black-formatter \
     --install-extension charliermarsh.ruff \
     --install-extension wholroyd.jinja \
     --install-extension otovo-oss.htmx-tags \
     --install-extension bradlc.vscode-tailwindcss
```

#### VS Code 설정 파일

**`.vscode/settings.json`** (프로젝트 설정):

```json
{
    // Python 설정
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,

    // 포맷팅 설정
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },

    // Ruff 린팅
    "ruff.enable": true,
    "ruff.lint.args": ["--config=pyproject.toml"],

    // Jinja/HTML 설정
    "[jinja-html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "files.associations": {
        "*.html": "jinja-html"
    },

    // 파일 제외
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".ruff_cache": true,
        ".mypy_cache": true,
        "*.egg-info": true
    },

    // 에디터 설정
    "editor.rulers": [88, 120],
    "editor.tabSize": 4,
    "editor.insertSpaces": true,

    // 터미널 설정 (Windows)
    "terminal.integrated.defaultProfile.windows": "PowerShell",

    // 터미널 설정 (macOS/Linux)
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.defaultProfile.linux": "bash"
}
```

> **Windows 사용자**: `python.defaultInterpreterPath`를 `"${workspaceFolder}/venv/Scripts/python.exe"`로 변경하세요.

**`.vscode/launch.json`** (디버그 설정):

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI 서버",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--port", "8001"
            ],
            "jinja": true,
            "justMyCode": false,
            "env": {
                "PYTHONDONTWRITEBYTECODE": "1"
            }
        },
        {
            "name": "현재 파일 테스트",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["${file}", "-v", "-s"],
            "console": "integratedTerminal"
        },
        {
            "name": "전체 테스트",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

**`.vscode/extensions.json`** (권장 확장):

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "wholroyd.jinja",
        "otovo-oss.htmx-tags",
        "bradlc.vscode-tailwindcss"
    ]
}
```

### 1.2 PyCharm

#### 설치

**Windows/macOS:**
- [JetBrains 공식 사이트](https://www.jetbrains.com/pycharm/download/)에서 다운로드

**Linux:**
```bash
# Snap으로 설치
sudo snap install pycharm-community --classic

# 또는 JetBrains Toolbox 사용
```

#### PyCharm 설정

1. **인터프리터 설정**
   - File → Settings → Project → Python Interpreter
   - 가상환경 선택 또는 Add Interpreter

2. **Black 포맷터 설정**
   - File → Settings → Tools → Black
   - On code reformat: 활성화
   - On save: 활성화

3. **Ruff 설정**
   - File → Settings → Plugins → Ruff 설치
   - File → Settings → Tools → Ruff → Enable

4. **FastAPI 실행 구성**
   - Run → Edit Configurations → Add New → Python
   - Script path: uvicorn
   - Parameters: `app.main:app --reload --port 8001`

### 1.3 Vim/Neovim (고급 사용자)

```bash
# pyright (타입 검사)
pip install pyright

# LSP 설정 (init.lua 또는 .vimrc에 추가)
# nvim-lspconfig 플러그인 필요
```

## 2. 코드 품질 도구 설정

### 2.1 Black (코드 포맷터)

**설치:**
```bash
pip install black
```

**사용법:**
```bash
# 포맷팅 실행
black app tests

# 검사만 (변경 없이)
black --check app tests

# 변경 사항 미리보기
black --diff app tests
```

**설정** (`pyproject.toml`):

```toml
[tool.black]
line-length = 88
target-version = ['py311', 'py312']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | alembic/versions
)/
'''
```

### 2.2 isort (import 정렬)

**설치:**
```bash
pip install isort
```

**사용법:**
```bash
# import 정렬
isort app tests

# 검사만
isort --check-only app tests
```

**설정** (`pyproject.toml`):

```toml
[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["app"]
skip = ["alembic/versions"]
```

### 2.3 Ruff (빠른 린터)

**설치:**
```bash
pip install ruff
```

**사용법:**
```bash
# 린트 검사
ruff check app tests

# 자동 수정
ruff check --fix app tests

# 포맷팅 (Black 대체 가능)
ruff format app tests
```

**설정** (`pyproject.toml`):

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [
    ".git",
    ".venv",
    "alembic/versions",
    "__pycache__",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line too long (black handles this)
    "B008",   # do not perform function calls in argument defaults
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG001"]  # Unused function argument in tests
```

### 2.4 mypy (타입 검사)

**설치:**
```bash
pip install mypy
```

**사용법:**
```bash
# 타입 검사
mypy app

# 특정 파일
mypy app/services/auth.py
```

**설정** (`pyproject.toml`):

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
ignore_missing_imports = true
exclude = ["alembic/", "tests/"]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### 2.5 pre-commit (Git 훅)

**설치:**
```bash
pip install pre-commit
```

**초기화:**
```bash
# 훅 설치
pre-commit install

# 모든 파일에 수동 실행
pre-commit run --all-files
```

**`.pre-commit-config.yaml`**:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - sqlalchemy[mypy]
```

## 3. 테스트 환경 설정

### 3.1 pytest 설정

**설치:**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**설정** (`pyproject.toml`):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
filterwarnings = [
    "ignore::DeprecationWarning",
]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```

### 3.2 테스트 실행

```bash
# 전체 테스트
pytest

# 상세 출력
pytest -v

# 특정 파일
pytest tests/test_api/test_auth.py

# 특정 테스트
pytest tests/test_api/test_auth.py::test_login -v

# 키워드로 필터
pytest -k "login or register"

# 실패한 테스트만 재실행
pytest --lf

# 첫 실패 시 중단
pytest -x

# print 출력 보기
pytest -s

# 병렬 실행 (pytest-xdist 필요)
pytest -n auto
```

### 3.3 커버리지 측정

```bash
# 커버리지와 함께 테스트
pytest --cov=app

# HTML 리포트 생성
pytest --cov=app --cov-report=html

# 커버리지 80% 미만 시 실패
pytest --cov=app --cov-fail-under=80

# 특정 파일 제외
pytest --cov=app --cov-omit="app/config.py"
```

**설정** (`pyproject.toml`):

```toml
[tool.coverage.run]
source = ["app"]
omit = [
    "app/config.py",
    "*/tests/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## 4. 데이터베이스 도구

### 4.1 DB Browser for SQLite

개발용 SQLite 데이터베이스를 GUI로 확인할 수 있습니다.

**Windows:**
```powershell
winget install DBBrowserForSQLite.DBBrowserForSQLite
```

**macOS:**
```bash
brew install --cask db-browser-for-sqlite
```

**Linux:**
```bash
sudo apt install sqlitebrowser
```

**라즈베리파이:**
```bash
sudo apt install sqlitebrowser
```

### 4.2 DBeaver (다양한 DB 지원)

**Windows:**
```powershell
winget install dbeaver.dbeaver
```

**macOS:**
```bash
brew install --cask dbeaver-community
```

**Linux:**
```bash
sudo snap install dbeaver-ce
```

### 4.3 Alembic 마이그레이션 명령어

```bash
# 현재 마이그레이션 상태 확인
alembic current

# 마이그레이션 히스토리
alembic history

# 새 마이그레이션 생성 (자동)
alembic revision --autogenerate -m "add users table"

# 새 마이그레이션 생성 (수동)
alembic revision -m "add custom migration"

# 최신 버전으로 업그레이드
alembic upgrade head

# 한 단계 업그레이드
alembic upgrade +1

# 한 단계 다운그레이드
alembic downgrade -1

# 특정 버전으로 이동
alembic upgrade abc123
alembic downgrade abc123

# 모든 마이그레이션 롤백
alembic downgrade base
```

## 5. API 테스트 도구

### 5.1 Swagger UI (내장)

서버 실행 후 자동으로 제공됩니다.

| URL | 설명 |
|-----|------|
| http://localhost:8001/docs | Swagger UI (인터랙티브) |
| http://localhost:8001/redoc | ReDoc (문서용) |
| http://localhost:8001/openapi.json | OpenAPI 스키마 |

### 5.2 curl 명령어 예시

**Windows (PowerShell):**
```powershell
# 회원가입
Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"email": "test@example.com", "username": "testuser", "password": "password123"}'

# 로그인 (쿠키 저장)
$response = Invoke-WebRequest -Uri "http://localhost:8001/api/v1/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"email": "test@example.com", "password": "password123"}' `
    -SessionVariable session

# 인증된 요청
Invoke-RestMethod -Uri "http://localhost:8001/api/v1/users/me" `
    -WebSession $session
```

**macOS/Linux:**
```bash
# 회원가입
curl -X POST http://localhost:8001/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "username": "testuser", "password": "password123"}'

# 로그인 (쿠키 저장)
curl -X POST http://localhost:8001/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' \
    -c cookies.txt

# 인증된 요청
curl http://localhost:8001/api/v1/users/me -b cookies.txt

# 아이템 생성
curl -X POST http://localhost:8001/api/v1/items \
    -H "Content-Type: application/json" \
    -d '{"title": "새 아이템", "description": "설명"}' \
    -b cookies.txt
```

### 5.3 HTTPie (사용하기 쉬운 대안)

**설치:**
```bash
pip install httpie
```

**사용법:**
```bash
# GET 요청
http GET localhost:8001/api/v1/items

# POST 요청
http POST localhost:8001/api/v1/auth/register \
    email=test@example.com \
    username=testuser \
    password=password123

# 세션 사용
http --session=./session.json POST localhost:8001/api/v1/auth/login \
    email=test@example.com \
    password=password123

http --session=./session.json GET localhost:8001/api/v1/users/me
```

### 5.4 Postman / Insomnia

GUI 기반 API 테스트 도구입니다.

- **Postman**: https://www.postman.com/downloads/
- **Insomnia**: https://insomnia.rest/download

## 6. 개발 서버 실행 옵션

### 6.1 기본 실행

```bash
# run.py 사용
python run.py

# uvicorn 직접 실행
uvicorn app.main:app --reload --port 8001

# 모든 인터페이스에서 접속 허용 (다른 기기에서 접속 시)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 6.2 디버그 모드

```bash
# 상세 로깅
uvicorn app.main:app --reload --log-level debug

# SQL 쿼리 로깅 (.env에서 DEBUG=true 설정)
```

### 6.3 프로덕션 모드 테스트

```bash
# 리로드 없이 실행
uvicorn app.main:app --host 0.0.0.0 --port 8001

# 워커 수 지정 (멀티 프로세스)
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4

# Gunicorn 사용 (Linux/macOS)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

## 7. 환경 변수 관리

### 7.1 개발용 `.env` 예시

```env
# 앱 설정
APP_NAME=FastAPI-HTMX-Dev
APP_ENV=development
DEBUG=true

# 보안 (개발용 - 프로덕션에서는 반드시 변경!)
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 데이터베이스 (개발용 SQLite)
DATABASE_URL=sqlite+aiosqlite:///./app.db

# 로깅
LOG_LEVEL=DEBUG
```

### 7.2 테스트용 `.env.test` 예시

```env
APP_ENV=testing
DEBUG=true
SECRET_KEY=test-secret-key
JWT_SECRET_KEY=test-jwt-secret
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

### 7.3 환경 변수 검증

```bash
# Python에서 확인
python -c "from app.core.config import settings; print(settings.model_dump())"
```

## 8. 유용한 명령어 모음

### 8.1 가상환경 관리

**Windows (PowerShell):**
```powershell
# 가상환경 생성
python -m venv venv

# 활성화
.\venv\Scripts\Activate.ps1

# 비활성화
deactivate

# 가상환경 삭제
Remove-Item -Recurse -Force venv
```

**macOS/Linux:**
```bash
# 가상환경 생성
python3 -m venv venv

# 활성화
source venv/bin/activate

# 비활성화
deactivate

# 가상환경 삭제
rm -rf venv
```

### 8.2 의존성 관리

```bash
# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 의존성 업데이트
pip install --upgrade -r requirements.txt

# 현재 의존성 목록 저장
pip freeze > requirements-current.txt

# 특정 패키지 버전 확인
pip show fastapi

# 오래된 패키지 확인
pip list --outdated
```

### 8.3 캐시 정리

**Windows (PowerShell):**
```powershell
# Python 캐시 삭제
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force

# pytest 캐시 삭제
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue

# mypy 캐시 삭제
Remove-Item -Recurse -Force .mypy_cache -ErrorAction SilentlyContinue

# ruff 캐시 삭제
Remove-Item -Recurse -Force .ruff_cache -ErrorAction SilentlyContinue
```

**macOS/Linux:**
```bash
# Python 캐시 삭제
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# 모든 캐시 삭제
rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
```

### 8.4 포트 관리

**Windows:**
```powershell
# 포트 사용 확인
netstat -ano | findstr :8001

# 프로세스 종료
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# 포트 사용 확인
lsof -i :8001

# 프로세스 종료
kill $(lsof -t -i:8001)

# 또는 강제 종료
kill -9 $(lsof -t -i:8001)
```

### 8.5 데이터베이스 관리

```bash
# 데이터베이스 초기화 (SQLite)
rm -f app.db  # Linux/macOS
del app.db    # Windows

# 마이그레이션 재적용
alembic upgrade head

# 테스트 데이터베이스 초기화
rm -f test.db  # Linux/macOS
del test.db    # Windows
```

## 9. 문제 해결

### 9.1 ImportError: No module named 'app'

**원인**: Python 경로에 프로젝트가 없음

**해결 (Windows PowerShell):**
```powershell
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
```

**해결 (macOS/Linux):**
```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### 9.2 Permission denied (실행 정책 오류)

**Windows PowerShell:**
```powershell
# 현재 사용자에 대해 스크립트 실행 허용
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 9.3 가상환경 활성화 안됨

**확인:**
```bash
# 현재 Python 경로 확인
which python   # macOS/Linux
where python   # Windows

# 가상환경 Python이어야 함
# 예: /path/to/project/venv/bin/python
```

### 9.4 포트 이미 사용 중

**해결:** 다른 포트 사용
```bash
uvicorn app.main:app --reload --port 8002
```

### 9.5 마이그레이션 충돌

```bash
# 마이그레이션 히스토리 확인
alembic history

# 충돌하는 마이그레이션 수동 수정 또는
# 마이그레이션 초기화 (개발 환경에서만!)
rm -rf alembic/versions/*
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### 9.6 라즈베리파이 메모리 부족

```bash
# 스왑 메모리 증가
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=2048 으로 변경
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# pip 설치 시 메모리 제한
pip install --no-cache-dir -r requirements.txt
```

## 10. 다음 단계

- 📖 [API 레퍼런스](./13-api-reference-API-레퍼런스.md) - API 문서
