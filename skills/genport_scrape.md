# 젠포트 결과 스크래핑

젠포트 백테스트 결과를 스크래핑하여 분석합니다.

## 추출 대상 데이터

### 1. 성과 지표

| 지표 | 설명 | 위치 |
|------|------|------|
| 총 수익률 | 전체 기간 수익률 | `.result-summary .total-return` |
| CAGR | 연환산 수익률 | `.result-summary .cagr` |
| 샤프 비율 | 리스크 대비 수익 | `.result-summary .sharpe` |
| MDD | 최대 낙폭 | `.result-summary .mdd` |
| 승률 | 수익 거래 비율 | `.result-summary .win-rate` |
| 거래 횟수 | 총 매매 횟수 | `.result-summary .trade-count` |

### 2. 거래 내역

```
날짜 | 종목코드 | 종목명 | 매수/매도 | 수량 | 가격 | 수익률
```

### 3. 자산 곡선 데이터

```
날짜 | 자산가치 | 벤치마크(KOSPI)
```

## 스크래핑 방법

### MCP Browser 사용

```javascript
// 1. 결과 페이지 스냅샷
const snapshot = await browser_snapshot();

// 2. 성과 지표 추출
// snapshot에서 필요한 데이터 파싱

// 3. 거래 내역 테이블 스크래핑
await browser_click({ element: "거래내역 탭", ref: ".tab-trade-history" });
const tradeSnapshot = await browser_snapshot();

// 4. 자산 곡선 데이터 (차트에서 추출이 어려우면 API 호출 확인)
await browser_network_requests(); // API 엔드포인트 확인
```

### Python 파서 사용

```python
from genport.parser import GenportResultParser

parser = GenportResultParser()

# HTML에서 결과 파싱
result = parser.parse(html_content)
print(f"총 수익률: {result.total_return}%")
print(f"샤프 비율: {result.sharpe_ratio}")
print(f"MDD: {result.max_drawdown}%")

# 거래 내역 파싱
trades = parser.parse_trade_history(trade_html)
for trade in trades:
    print(f"{trade['date']} {trade['symbol']} {trade['side']} {trade['return']}")
```

## 데이터 저장

### CSV 형식

```python
import pandas as pd

# 결과를 DataFrame으로 변환
df = pd.DataFrame([{
    "strategy_id": strategy_id,
    "params": str(params),
    "total_return": result.total_return,
    "cagr": result.cagr,
    "sharpe_ratio": result.sharpe_ratio,
    "max_drawdown": result.max_drawdown,
    "win_rate": result.win_rate,
    "trade_count": result.trade_count,
    "timestamp": datetime.now().isoformat(),
}])

df.to_csv("data/backtest_results.csv", mode="a", header=False, index=False)
```

### JSON 형식

```python
import json

result_dict = {
    "strategy_id": strategy_id,
    "params": params.__dict__,
    "metrics": result.__dict__,
    "timestamp": datetime.now().isoformat(),
}

with open(f"data/results/{strategy_id}_{timestamp}.json", "w") as f:
    json.dump(result_dict, f, indent=2, ensure_ascii=False)
```

## 분석 자동화

### 여러 전략 비교

```python
import pandas as pd
import matplotlib.pyplot as plt

# 결과 로드
df = pd.read_csv("data/backtest_results.csv")

# 샤프 비율 기준 정렬
top_strategies = df.sort_values("sharpe_ratio", ascending=False).head(10)
print(top_strategies[["strategy_id", "total_return", "sharpe_ratio", "max_drawdown"]])

# 시각화
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].bar(top_strategies["strategy_id"], top_strategies["total_return"])
axes[0, 0].set_title("Total Return by Strategy")
# ... 추가 차트
plt.savefig("analysis/strategy_comparison.png")
```

## 주의사항

- 젠포트 HTML 구조 변경 시 파서 업데이트 필요
- 차트 데이터는 직접 추출이 어려울 수 있음 (네트워크 요청 확인)
- 대량 스크래핑 시 rate limiting 고려

