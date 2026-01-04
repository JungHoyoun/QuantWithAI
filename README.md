# Trading System

> AI-Powered Quantitative Trading System  
> 개발: Claude Code + Antigravity  
> 목표: 2026년 연 15%+ 수익률

---

## 🎯 프로젝트 개요

알고리즘 트레이딩 시스템으로 한국 주식, 미국 주식, 암호화폐 시장에서 퀀트 전략을 실행합니다.

### 타겟 시장
- 🇰🇷 **한국 주식**: 키움증권 API (30% 비중)
- 🇺🇸 **미국 주식**: NH투자증권 API (60% 비중)
- ₿ **암호화폐**: Upbit API (10% 비중)

### 핵심 전략
1. **모멘텀 전략**: 추세 추종
2. **평균회귀 전략**: 과매도/과매수 구간 활용
3. **변동성 전략**: 볼린저 밴드, ATR

---

## 📂 프로젝트 구조

```
trading-system/
├── strategies/              # 트레이딩 전략
│   ├── __init__.py
│   ├── README.md
│   ├── momentum.py          # (TODO)
│   ├── mean_reversion.py    # (TODO)
│   └── volatility.py        # (TODO)
│
├── backtesting/             # 백테스팅 엔진
│   ├── __init__.py
│   ├── README.md
│   ├── engine.py            # (TODO)
│   ├── portfolio.py         # (TODO)
│   └── performance.py       # (TODO)
│
├── docs/                    # 참고 문서 (Google Drive 동기화)
│   ├── README.md
│   ├── 2026_자산관리_계획.md
│   ├── 퀀트_트레이딩_가이드.md
│   ├── 퀀트_트레이딩_상세_계획.md
│   ├── 알고리즘_트레이딩_시스템_구축.md
│   ├── 레버리지_전략.md
│   ├── 트레이딩_시작_가이드.md
│   └── AI_Trading_Agent_Prompt.md
│
├── data/                    # 시장 데이터 (gitignored)
├── logs/                    # 거래 로그 (gitignored)
├── notebooks/               # 분석용 Jupyter notebooks
├── tests/                   # 테스트 코드
│
├── .env                     # API 키 & 설정 (gitignored)
├── .env.example             # 환경 변수 템플릿
├── pyproject.toml           # uv 의존성 관리
├── sync_docs.sh             # 문서 동기화 스크립트
└── README.md                # 현재 파일
```

---

## 🚀 시작하기

### 1. 환경 설정

```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 API 키 입력

# Python 환경 (uv 자동 관리)
# 별도 설치 불필요 - uv가 자동으로 처리
```

### 2. 백테스팅 실행

```bash
# 전략 백테스트
uv run backtesting/engine.py --strategy momentum --start 2024-01-01 --end 2025-12-31

# 결과는 logs/backtest/에 저장됨
```

### 3. Paper Trading

```bash
# .env에서 PAPER_TRADING=true 설정 후
uv run main.py --mode paper
```

### 4. 실전 거래 (2026 Q3 예정)

```bash
# .env에서 PAPER_TRADING=false 설정 후
uv run main.py --mode live
```

---

## 📊 2026년 로드맵

| Quarter | 목표 | 상태 |
|---------|------|:----:|
| Q1 (1-3월) | 시스템 개발 & 백테스팅 | 🔨 진행중 |
| Q2 (4-6월) | Paper Trading & 최적화 | ⬜ 예정 |
| Q3-Q4 (7-12월) | 실전 투입 & 자본 확대 | ⬜ 예정 |

**성공 기준**: 연 15%+ 수익률 달성 (2026년 말)

---

## 🔗 관련 문서

### 문서 구조

**코드 저장소** (현재 위치): `~/HY/trading-system/`
- 실제 코드, Git 버전 관리
- `docs/` - Google Drive 문서 스냅샷 (자동 동기화)

**문서 저장소** (Google Drive): `~/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles/`
- `Areas/Rich/알고리즘 트레이딩/` - 전략, 계획, 학습 자료 (원본)
- `Projects/알고리즘-트레이딩/` - 개발 진행 상황, 회고

### 주요 문서 (로컬 복사본)
- [docs/2026_자산관리_계획.md](./docs/2026_자산관리_계획.md) - 전체 투자 계획
- [docs/퀀트_트레이딩_가이드.md](./docs/퀀트_트레이딩_가이드.md) - 퀀트 기초 지식
- [docs/퀀트_트레이딩_상세_계획.md](./docs/퀀트_트레이딩_상세_계획.md) - 개발 계획
- [docs/알고리즘_트레이딩_시스템_구축.md](./docs/알고리즘_트레이딩_시스템_구축.md) - 시스템 구축 가이드
- [docs/AI_Trading_Agent_Prompt.md](./docs/AI_Trading_Agent_Prompt.md) - Antigravity 프롬프트

**문서 동기화**: `./sync_docs.sh` 실행 (Google Drive → 로컬)

---

## 🛠️ 기술 스택

- **언어**: Python 3.11+
- **패키지 관리**: uv (PEP 723 inline dependencies)
- **데이터**: pandas, numpy
- **백테스팅**: backtrader, vectorbt
- **API**: 키움 OpenAPI, NH투자증권 API, Upbit API
- **AI 도구**: Claude Code, Antigravity

---

## ⚠️ 리스크 관리

- **손절선**: -2% (자동 실행)
- **일일 최대 손실**: -5%
- **포지션 사이즈**: 계좌의 10% 이하
- **레버리지**: Paper Trading 검증 후 2027년부터

---

## 📝 라이센스

개인 프로젝트 - All Rights Reserved

---

**최종 수정**: 2026-01-04  
**개발자**: Hoyoun Jung

