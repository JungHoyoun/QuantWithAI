# 젠포트 백테스트 실행

젠포트 웹사이트에서 전략 파라미터를 변경하고 백테스트를 실행합니다.

## 사전 조건

- 젠포트 계정 로그인 상태
- 테스트할 전략이 젠포트에 저장되어 있어야 함

## 실행 절차

### 1. 젠포트 접속 및 로그인

```
1. https://www.genport.co.kr 접속
2. 로그인 페이지로 이동
3. 아이디/비밀번호 입력
4. 로그인 버튼 클릭
5. 대시보드 페이지 로딩 확인
```

### 2. 전략 페이지 이동

```
1. 내 전략 메뉴 클릭
2. 테스트할 전략 선택
3. 전략 상세 페이지 로딩 확인
```

### 3. 백테스트 파라미터 설정

설정 가능한 파라미터:
- **시작일/종료일**: 백테스트 기간
- **초기 자본금**: 시뮬레이션 시작 금액
- **수수료율**: 매매 수수료 (보통 0.015%)
- **최대 보유 종목 수**: 동시 보유 가능 종목 수

### 4. 백테스트 실행

```
1. "백테스트 실행" 버튼 클릭
2. 로딩 스피너 표시됨
3. 결과 페이지 로딩 대기 (최대 5분)
```

### 5. 결과 추출

추출할 지표:
- 총 수익률
- 연환산 수익률 (CAGR)
- 샤프 비율
- 최대 낙폭 (MDD)
- 승률
- 거래 횟수

## MCP Browser 사용 예시

```javascript
// 1. 젠포트 접속
await browser_navigate({ url: "https://www.genport.co.kr/login" });

// 2. 로그인
await browser_fill_form({
  fields: [
    { name: "아이디", ref: "input[name='userId']", type: "textbox", value: "your_id" },
    { name: "비밀번호", ref: "input[name='password']", type: "textbox", value: "your_pw" }
  ]
});
await browser_click({ element: "로그인 버튼", ref: "button[type='submit']" });

// 3. 전략 페이지 이동
await browser_navigate({ url: "https://www.genport.co.kr/strategy/{strategy_id}" });

// 4. 백테스트 실행
await browser_click({ element: "백테스트 실행", ref: "button:has-text('백테스트')" });

// 5. 결과 대기 및 스크린샷
await browser_wait_for({ text: "수익률" });
await browser_take_screenshot({ filename: "backtest_result.png" });
```

## 파라미터 스윕 자동화

여러 파라미터 조합을 자동으로 테스트:

```python
# genport/backtest.py 사용
params = BacktestParams(
    start_date=date(2020, 1, 1),
    end_date=date(2024, 12, 31),
    initial_capital=10_000_000,
)

param_grid = {
    "max_holdings": [5, 10, 15, 20],
    "commission_rate": [0.00015, 0.0003],
}

results = await backtest.run_parameter_sweep(strategy_id, params, param_grid)
```

## 주의사항

- 젠포트 서버 부하로 인해 백테스트가 느릴 수 있음
- 연속 실행 시 적절한 대기 시간 필요 (rate limiting)
- 로그인 세션 만료 시 재로그인 필요

