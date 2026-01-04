# Backtesting Engine

전략을 과거 데이터로 검증하는 백테스팅 엔진입니다.

## 주요 컴포넌트

### 1. engine.py
백테스트 실행 엔진
- 데이터 로드
- 전략 실행
- 주문 시뮬레이션
- 결과 저장

### 2. portfolio.py
포트폴리오 관리
- 현금 관리
- 포지션 추적
- 자산 배분
- 리밸런싱

### 3. performance.py
성과 분석 및 리포팅
- 수익률 계산
- 샤프 비율, MDD
- 차트 생성
- 리포트 출력

## 사용 예제

```python
from backtesting import engine
from strategies.momentum import MomentumStrategy

# 백테스트 설정
config = {
    'start_date': '2024-01-01',
    'end_date': '2025-12-31',
    'initial_capital': 10000000,
    'commission': 0.0015
}

# 전략 로드
strategy = MomentumStrategy(params={'rsi_period': 14})

# 백테스트 실행
results = engine.run(strategy, config)

# 결과 분석
print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
```

## 백테스트 체크리스트

- [ ] 과거 데이터 품질 확인
- [ ] 수수료/슬리피지 반영
- [ ] 생존 편향 제거
- [ ] Look-ahead bias 제거
- [ ] 적절한 샘플 기간 (최소 3년)
- [ ] Out-of-sample 테스트

---

**목표**: 백테스트 샤프 비율 1.5+ 달성

