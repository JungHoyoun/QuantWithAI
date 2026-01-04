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
│   ├── momentum.py
│   ├── mean_reversion.py
│   └── volatility.py
│
├── backtesting/             # 백테스팅 엔진
│   ├── engine.py
│   ├── portfolio.py
│   └── performance.py
│
├── data/                    # 시장 데이터 (gitignored)
│   ├── korean_stocks/
│   ├── us_stocks/
│   └── crypto/
│
├── logs/                    # 거래 로그 (gitignored)
│   ├── backtest/
│   ├── paper/
│   └── live/
│
├── notebooks/               # 분석용 Jupyter notebooks
│   └── strategy_analysis.ipynb
│
├── tests/                   # 테스트 코드
│   └── test_strategies.py
│
├── .env                     # API 키 & 설정 (gitignored)
├── .env.example             # 환경 변수 템플릿
├── pyproject.toml           # uv 의존성 관리
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

### Google Drive 워크스페이스
```
~/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles/
├── Areas/Rich/알고리즘 트레이딩/          # 전략, 계획, 학습 자료
└── Projects/알고리즘-트레이딩/             # 개발 진행 상황, 회고
```

### 주요 문서
- [2026_자산관리_계획.md](../DriveSyncFiles/Areas/Rich/2026_자산관리_계획.md)
- [퀀트_트레이딩_상세_계획.md](../DriveSyncFiles/Areas/Rich/알고리즘 트레이딩/퀀트_트레이딩_상세_계획.md)
- [개발_로그.md](../DriveSyncFiles/Projects/알고리즘-트레이딩/개발_로그.md)

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

