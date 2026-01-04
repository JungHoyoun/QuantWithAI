# Trading Strategies

이 디렉토리에는 실제 트레이딩 전략 구현 코드가 들어갑니다.

## 구현 예정 전략

### 1. 모멘텀 전략 (momentum.py)
- **원리**: 강한 추세를 따라가는 전략
- **지표**: RSI, MACD, 이동평균선
- **시장**: 한국/미국 주식

### 2. 평균회귀 전략 (mean_reversion.py)
- **원리**: 과매도/과매수 구간에서 반대 포지션
- **지표**: 볼린저 밴드, RSI, Stochastic
- **시장**: 한국/미국 주식, 암호화폐

### 3. 변동성 전략 (volatility.py)
- **원리**: 변동성 확대/축소 구간 활용
- **지표**: ATR, 볼린저 밴드, 역사적 변동성
- **시장**: 암호화폐, 미국 주식

## 전략 개발 가이드

각 전략 파일은 다음 구조를 따릅니다:

```python
class Strategy:
    def __init__(self, params):
        """전략 초기화"""
        pass
    
    def generate_signal(self, data):
        """매수/매도 시그널 생성"""
        pass
    
    def calculate_position_size(self, signal, portfolio):
        """포지션 사이즈 계산"""
        pass
    
    def risk_management(self, position):
        """리스크 관리 (손절/익절)"""
        pass
```

---

**참고 문서**: [퀀트_트레이딩_가이드.md](../../DriveSyncFiles/Areas/Rich/알고리즘 트레이딩/퀀트_트레이딩_가이드.md)

