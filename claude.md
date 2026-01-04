# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

한국장 알고리즘 트레이딩 시스템. 세 가지 핵심 컴포넌트:
- **젠포트 자동화** (`genport/`): Playwright 기반 웹 백테스트 자동화
- **키움 API** (`src/broker/kiwoom/`): 32비트 COM 기반, ZeroMQ IPC로 64비트 메인과 통신
- **Rust 백테스트 엔진** (`backtesting-rs/`): 고속 병렬 백테스트, PyO3로 Python 바인딩 지원

## 듀얼 Python 환경

키움 API는 32비트 COM 객체이므로 프로세스 분리 아키텍처 사용:

```
64비트 Python (메인)          32비트 Python (키움)
┌─────────────────────┐       ┌─────────────────────┐
│ .venv/ (uv 관리)     │◄─────►│ .venv-kiwoom-32/    │
│ - 데이터 분석        │  ZMQ  │ - 키움 OpenAPI+     │
│ - 백테스팅          │       │ - PyQt5 + pywin32   │
│ - 젠포트 자동화     │       │                     │
└─────────────────────┘       └─────────────────────┘
```

### 환경 설정

```powershell
# 전체 설정 (권장)
.\scripts\setup_environments.ps1

# 또는 수동 설정:
# 1. Python 3.11 64비트 설치 → C:\Python311-64\
# 2. Python 3.11 32비트 설치 → C:\Python311-32\
# 3. uv 설치: irm https://astral.sh/uv/install.ps1 | iex
# 4. 64비트 환경: uv venv --python C:\Python311-64\python.exe && uv sync
# 5. 32비트 환경: C:\Python311-32\python.exe -m venv .venv-kiwoom-32
#                 .\.venv-kiwoom-32\Scripts\pip install -r requirements-kiwoom.txt
```

### 키움 서버 실행

```powershell
# 터미널 1: 키움 서버 (32비트)
.\scripts\start_kiwoom_server.bat

# 터미널 2: 메인 애플리케이션 (64비트)
uv run python -m src.main
```

## 개발 명령어

```bash
# Python 환경 (uv 사용)
uv sync                              # 의존성 설치
uv run pytest                        # 테스트 실행
uv run pytest tests/test_foo.py -k "test_name"  # 단일 테스트
uv run black .                       # 포맷팅
uv run ruff check --fix .            # 린트

# Rust 백테스트 엔진
cd backtesting-rs && cargo build --release
cd backtesting-rs && cargo test
cd backtesting-rs && cargo run --release -- --data ../data/sample.csv --strategy momentum

# 젠포트 백테스트 실행
uv run python -m genport.backtest --strategy <strategy_id>

# Playwright 브라우저 설치 (최초 1회)
uv run playwright install chromium
```

## 코드 아키텍처

### 브로커 인터페이스 (`src/broker/interface.py`)
모든 브로커 구현체가 따라야 하는 `BrokerInterface` ABC 정의. 핵심 타입:
- `Order`, `Position`, `OHLCV` dataclass
- `OrderSide`, `OrderType` enum
- 필수 메서드: `connect`, `get_balance`, `get_positions`, `submit_order`, `cancel_order`, `get_historical_data`

### Rust 백테스트 엔진 (`backtesting-rs/src/`)
- `lib.rs`: 모듈 진입점, PyO3 바인딩 (`feature = "python"`)
- `engine.rs`: `BacktestEngine` 구현, `BacktestConfig` 설정, `BacktestResult` 성과 지표
- `strategy.rs`: `Strategy` trait, 기본 전략 구현 (`SmaCrossover`, `Momentum`, `MeanReversion`)
- `data.rs`: 시장 데이터 로딩

### 젠포트 자동화 (`genport/`)
- `browser.py`: `GenportBrowser` 클래스 - async context manager, Playwright 제어
- `backtest.py`: 백테스트 실행 자동화
- `parser.py`: 결과 파싱

### 키움 IPC 아키텍처 (`src/broker/kiwoom/`)
- `server.py`: 32비트 Python에서 실행, 키움 COM 객체 직접 제어, ZeroMQ REP 소켓
- `client.py`: 64비트에서 사용, `BrokerInterface` 구현, ZeroMQ REQ 소켓
- 메시지 포맷: JSON (IPCMessage/IPCResponse)

## 코딩 컨벤션

### Python
- 포맷터: black (line-length: 100)
- 린터: ruff
- 타입 힌트 필수 (mypy strict)
- Docstring: Google 스타일

### Rust
- rustfmt, clippy 사용
- rust_decimal로 금융 계산 (부동소수점 사용 금지)

## 환경 변수 (`.env`)

```
GENPORT_USER_ID=       # 젠포트 로그인
GENPORT_PASSWORD=
KIWOOM_ACCOUNT=        # 키움증권 계좌번호
KIWOOM_IPC_PORT=5555   # 키움 IPC 포트 (기본: 5555)
PAPER_TRADING=true     # 실거래 전 필수
```

## 플랫폼 제약

- 키움 API는 **Windows 전용** (win32 COM)
- 젠포트 자동화 시 로그인 세션 유지 필요
