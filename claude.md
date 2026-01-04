# Trading System

한국장 알고리즘 트레이딩 시스템. 젠포트 자동화 + 키움증권 API + Rust 고속 백테스트 엔진.

## 프로젝트 개요

- **목표**: 2026년 연 15%+ 수익률 달성
- **시장**: 한국 주식 (키움증권), 추후 코인/미국장 확장
- **핵심 기능**:
  - 젠포트 백테스트 자동화 (브라우저 제어)
  - 키움증권 OpenAPI+ 연동 (실시간 데이터 + 자동매매)
  - Rust 기반 고속 백테스트 엔진 (젠포트 대비 100배+ 속도)
  - 스캘핑/데이트레이딩 지원

## 기술 스택

| 구분 | 기술 | 용도 |
|------|------|------|
| 메인 언어 | Python 3.11+ | 전략 로직, API 연동, 자동화 |
| 백테스트 | Rust | 고속 백테스트 엔진 |
| 브라우저 | Playwright | 젠포트 웹 자동화 |
| 증권 API | 키움 OpenAPI+ | 한국장 데이터/주문 (win32 COM) |
| 패키지 관리 | uv | Python 의존성 관리 |

## 프로젝트 구조

```
trading-system/
├── src/                         # Python 메인 코드
│   ├── broker/                  # 증권사 API 연동
│   │   ├── kiwoom/              # 키움 OpenAPI+ (PyQt5 기반)
│   │   └── interface.py         # 공통 인터페이스
│   ├── data/                    # 데이터 수집/관리
│   ├── strategy/                # 트레이딩 전략
│   └── utils/                   # 유틸리티
│
├── genport/                     # 젠포트 연동
│   ├── browser.py               # Playwright 브라우저 제어
│   ├── backtest.py              # 백테스트 실행 자동화
│   └── parser.py                # 결과 파싱
│
├── backtesting-rs/              # Rust 고속 백테스트 엔진
│   ├── Cargo.toml
│   └── src/
│
├── skills/                      # Claude Code MCP Skills
├── data/                        # 시장 데이터 (gitignored)
├── logs/                        # 로그 (gitignored)
├── docs/                        # 문서
└── tests/                       # 테스트
```

## 주요 컴포넌트

### 1. 젠포트 자동화 (`genport/`)

Playwright를 사용한 웹 자동화:
- 로그인, 전략 페이지 이동
- 백테스트 파라미터 설정 및 실행
- 결과 스크래핑 및 파싱
- 검증된 전략 실전 배포

### 2. 키움 API (`src/broker/kiwoom/`)

win32 COM 기반 PyQt5 연동:
- 실시간 시세 수신
- 주문 제출/취소/조회
- 잔고/포지션 조회
- 과거 데이터 조회

### 3. Rust 백테스트 엔진 (`backtesting-rs/`)

고속 백테스트 실행:
- 멀티스레드 병렬 처리
- 메모리 효율적 데이터 구조
- Python 바인딩 (PyO3)

## 코딩 컨벤션

### Python
- 포맷터: `black` (line-length: 100)
- 린터: `ruff`
- 타입 힌트: 필수 (mypy strict)
- 네이밍: snake_case (함수/변수), PascalCase (클래스)
- Docstring: Google 스타일

### Rust
- 포맷터: `rustfmt`
- 린터: `clippy`
- 네이밍: 표준 Rust 컨벤션

## 환경 변수

`.env` 파일에 설정 (`.env.example` 참고):

```
# 젠포트
GENPORT_USER_ID=your_id
GENPORT_PASSWORD=your_password

# 키움증권
KIWOOM_ACCOUNT=your_account_number

# 설정
PAPER_TRADING=true
LOG_LEVEL=INFO
```

## 실행 방법

```bash
# Python 환경 설정 (uv 사용)
uv sync

# 젠포트 백테스트 실행
uv run python -m genport.backtest --strategy <strategy_id>

# Rust 백테스트 (빌드 후)
cd backtesting-rs && cargo run --release

# 개발 모드
uv run pytest
uv run black .
uv run ruff check .
```

## 주의사항

- 키움 API는 **Windows 전용** (win32 COM)
- 젠포트 자동화 시 **로그인 세션 유지** 필요
- 실거래 전 **Paper Trading** 필수
- 민감 정보는 **절대 커밋 금지** (.env, API 키 등)

