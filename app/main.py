"""
FastAPI Application Entry Point
FastAPI 애플리케이션 진입점

이 파일은 FastAPI 애플리케이션의 시작점입니다.
웹 서버(uvicorn)가 이 파일의 'app' 객체를 로드하여 실행합니다.

실행 방법:
    uvicorn app.main:app --reload

주요 역할:
    1. 애플리케이션 인스턴스 생성
    2. 미들웨어 설정 (CORS, 인증 등)
    3. 라우터 등록 (API, 페이지, 파셜)
    4. 정적 파일 서빙 설정
    5. 수명주기(lifespan) 관리 (DB 연결 등)
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.templates import templates
from app.database import close_db, ensure_database_exists, init_db
from app.pages.router import pages_router
from app.partials.router import partials_router


# =============================================================================
# 수명주기(Lifespan) 관리
# =============================================================================
# FastAPI의 lifespan은 앱 시작/종료 시 실행되는 코드를 정의합니다.
# - 시작 시: 데이터베이스 연결, 캐시 초기화, 외부 서비스 연결 등
# - 종료 시: 연결 정리, 리소스 해제 등
#
# @asynccontextmanager 데코레이터:
# - 'yield' 이전 코드: 앱 시작 시 실행 (startup)
# - 'yield' 이후 코드: 앱 종료 시 실행 (shutdown)
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    애플리케이션 수명주기 관리

    시작 시 데이터베이스 초기화, 종료 시 연결 정리를 담당합니다.

    흐름:
        1. 서버 시작 → init_db() 실행 → DB 테이블 생성
        2. yield → 앱이 요청을 처리하는 동안 대기
        3. 서버 종료 신호 → close_db() 실행 → DB 연결 정리

    Note:
        이전 버전의 @app.on_event("startup")/@app.on_event("shutdown") 방식은
        deprecated 되었으며, lifespan 방식이 권장됩니다.
    """
    # =========================================================================
    # Startup (앱 시작 시 실행)
    # =========================================================================
    print("🚀 애플리케이션 시작 중...")
    await ensure_database_exists()  # PostgreSQL DB 자동 생성
    await init_db()  # DB 엔진 생성 및 테이블 초기화
    print("✅ 데이터베이스 초기화 완료")

    yield  # 앱이 실행되는 동안 여기서 대기

    # =========================================================================
    # Shutdown (앱 종료 시 실행)
    # =========================================================================
    print("🛑 애플리케이션 종료 중...")
    await close_db()  # DB 연결 풀 정리
    print("✅ 데이터베이스 연결 종료 완료")


# =============================================================================
# 애플리케이션 팩토리 패턴
# =============================================================================
# 팩토리 패턴을 사용하면:
# - 테스트 시 다른 설정으로 앱을 생성할 수 있음
# - 여러 앱 인스턴스를 만들 수 있음
# - 설정을 주입받아 유연하게 앱을 구성할 수 있음
# =============================================================================


def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션 팩토리

    애플리케이션을 생성하고 필요한 설정을 적용합니다.

    Returns:
        설정이 완료된 FastAPI 인스턴스

    구성 요소:
        1. FastAPI 인스턴스 생성 (제목, 버전, API 문서 설정)
        2. CORS 미들웨어 추가
        3. 정적 파일 마운트
        4. 예외 핸들러 등록
        5. 라우터 등록 (API, 페이지, 파셜)
    """

    # =========================================================================
    # FastAPI 인스턴스 생성
    # =========================================================================
    app = FastAPI(
        title=settings.app_name,                                    # API 문서에 표시될 제목
        description="FastAPI + Jinja2 + HTMX Boilerplate",          # API 설명
        version="1.0.0",                                            # API 버전
        # 개발 모드에서만 API 문서 활성화 (보안)
        docs_url="/docs" if settings.debug else None,               # Swagger UI
        redoc_url="/redoc" if settings.debug else None,             # ReDoc
        openapi_url="/openapi.json" if settings.debug else None,    # OpenAPI 스키마
        lifespan=lifespan,                                          # 수명주기 관리자
    )

    # =========================================================================
    # CORS (Cross-Origin Resource Sharing) 미들웨어
    # =========================================================================
    # CORS는 다른 도메인에서 이 API에 접근할 수 있도록 허용합니다.
    # 예: 프론트엔드(localhost:3000)에서 백엔드(localhost:8000) API 호출
    #
    # allow_origins: 허용할 도메인 목록 (예: ["http://localhost:3000"])
    # allow_credentials: 쿠키 전송 허용 여부 (JWT 쿠키 인증에 필요)
    # allow_methods: 허용할 HTTP 메서드 (GET, POST, PUT, DELETE 등)
    # allow_headers: 허용할 HTTP 헤더
    # =========================================================================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,  # 설정 파일에서 허용 도메인 로드
        allow_credentials=True,               # 쿠키 기반 인증 사용을 위해 True
        allow_methods=["*"],                  # 모든 HTTP 메서드 허용
        allow_headers=["*"],                  # 모든 헤더 허용
    )

    # =========================================================================
    # 정적 파일 마운트
    # =========================================================================
    # /static 경로로 들어오는 요청을 static/ 디렉토리에서 처리합니다.
    # 예: /static/css/custom.css → static/css/custom.css 파일 반환
    # =========================================================================
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # =========================================================================
    # 예외 핸들러 설정
    # =========================================================================
    # 애플리케이션에서 발생하는 예외를 일관된 형식으로 처리합니다.
    # - 404 Not Found → 404 페이지 렌더링
    # - 500 Internal Server Error → 500 페이지 렌더링
    # - 커스텀 예외 → 적절한 에러 응답 반환
    # =========================================================================
    setup_exception_handlers(app)

    # =========================================================================
    # 라우터 등록
    # =========================================================================
    # FastAPI에서 라우터는 URL 경로와 처리 함수를 매핑합니다.
    #
    # 이 보일러플레이트는 3가지 유형의 라우터를 사용합니다:
    #
    # 1. API 라우터 (/api/v1/*)
    #    - JSON 응답을 반환하는 REST API
    #    - 예: /api/v1/auth/login, /api/v1/items
    #
    # 2. 페이지 라우터 (/)
    #    - HTML 페이지를 반환하는 라우터
    #    - 예: /, /login, /dashboard
    #
    # 3. 파셜 라우터 (/partials/*)
    #    - HTMX 요청에 대해 부분 HTML을 반환
    #    - 전체 페이지가 아닌 특정 영역만 업데이트
    #    - 예: /partials/items/list, /partials/toasts/success
    # =========================================================================

    # API 라우터: /api/v1 프리픽스로 등록
    app.include_router(api_router, prefix="/api/v1")

    # 페이지 라우터: 프리픽스 없이 루트에 등록
    app.include_router(pages_router)

    # 파셜 라우터: /partials 프리픽스로 등록
    app.include_router(partials_router, prefix="/partials")

    return app


# =============================================================================
# 앱 인스턴스 생성
# =============================================================================
# 이 변수가 uvicorn이 찾는 진입점입니다.
# uvicorn app.main:app 명령에서 'app'이 바로 이 변수입니다.
# =============================================================================
app = create_app()


# =============================================================================
# 헬스 체크 엔드포인트
# =============================================================================
# 서버가 정상 작동하는지 확인하는 엔드포인트입니다.
#
# 사용처:
# - 로드밸런서의 헬스 체크
# - 쿠버네티스 liveness/readiness probe
# - 모니터링 시스템
#
# 응답 예시: {"status": "healthy", "app": "FastAPI Boilerplate"}
# =============================================================================


@app.get("/health", tags=["health"])
async def health_check():
    """
    헬스 체크 엔드포인트

    서버가 정상 작동하는지 확인합니다.
    배포 환경에서 로드밸런서나 모니터링 도구가 이 엔드포인트를 주기적으로 호출합니다.

    Returns:
        dict: 서버 상태 정보
            - status: "healthy" (정상)
            - app: 애플리케이션 이름
    """
    return {"status": "healthy", "app": settings.app_name}
