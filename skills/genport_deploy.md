# 젠포트 전략 배포

검증된 전략을 젠포트에서 실전 적용합니다.

## 사전 조건

- 백테스트 완료 및 성과 검증
- 샤프 비율 > 1.5 권장
- MDD < 20% 권장
- Paper Trading 최소 1개월 권장

## 배포 체크리스트

### 1. 전략 검증

```
[ ] 백테스트 기간: 최소 3년 이상
[ ] 다양한 시장 상황 포함 (상승장, 하락장, 횡보장)
[ ] 샤프 비율: 1.5 이상
[ ] 최대 낙폭: 20% 이하
[ ] 승률: 50% 이상
[ ] 거래 횟수: 통계적 유의성 확보 (100회 이상)
```

### 2. 리스크 관리 설정

```
[ ] 손절선 설정: -2% ~ -5%
[ ] 일일 최대 손실: -5%
[ ] 포지션 사이즈: 계좌의 10% 이하
[ ] 최대 보유 종목 수: 10개 이하
```

### 3. 실전 적용 설정

```
[ ] 초기 자본금 설정
[ ] 매매 시간 설정 (장 시작 후 30분 ~ 장 마감 30분 전)
[ ] 알림 설정 (카카오톡/텔레그램)
```

## 배포 절차

### Step 1: 전략 설정 페이지 이동

```javascript
// 전략 관리 페이지
await browser_navigate({ url: "https://www.genport.co.kr/strategy/{strategy_id}/settings" });
```

### Step 2: 실전 투자 설정

```javascript
// 실전 모드 활성화
await browser_click({ element: "실전 투자 탭", ref: ".tab-live-trading" });

// 자본금 설정
await browser_fill_form({
  fields: [
    { name: "투자금액", ref: "input[name='investAmount']", type: "textbox", value: "10000000" },
    { name: "종목당 최대금액", ref: "input[name='maxPerStock']", type: "textbox", value: "1000000" },
  ]
});

// 리스크 관리 설정
await browser_fill_form({
  fields: [
    { name: "손절선", ref: "input[name='stopLoss']", type: "textbox", value: "-2" },
    { name: "익절선", ref: "input[name='takeProfit']", type: "textbox", value: "10" },
  ]
});
```

### Step 3: 매매 계좌 연동

```javascript
// 증권사 계좌 연동 (키움증권)
await browser_click({ element: "계좌 연동", ref: ".btn-connect-account" });
await browser_fill_form({
  fields: [
    { name: "계좌번호", ref: "input[name='accountNumber']", type: "textbox", value: "XXXXXXXX" },
  ]
});
```

### Step 4: 전략 활성화

```javascript
// 전략 활성화
await browser_click({ element: "전략 시작", ref: ".btn-start-strategy" });

// 확인 다이얼로그
await browser_handle_dialog({ accept: true });

// 활성화 확인
await browser_wait_for({ text: "운영 중" });
await browser_take_screenshot({ filename: "strategy_deployed.png" });
```

## 모니터링 설정

### 알림 설정

```javascript
// 알림 설정 페이지
await browser_navigate({ url: "https://www.genport.co.kr/settings/notifications" });

// 텔레그램 알림 활성화
await browser_click({ element: "텔레그램 알림", ref: "input[name='telegramEnabled']" });
await browser_fill_form({
  fields: [
    { name: "Bot Token", ref: "input[name='telegramToken']", type: "textbox", value: "YOUR_BOT_TOKEN" },
    { name: "Chat ID", ref: "input[name='telegramChatId']", type: "textbox", value: "YOUR_CHAT_ID" },
  ]
});
```

### 알림 받을 이벤트

- 매수 체결
- 매도 체결
- 손절 발동
- 일일 리포트
- 에러 발생

## 긴급 정지

```javascript
// 전략 긴급 정지
await browser_navigate({ url: "https://www.genport.co.kr/strategy/{strategy_id}" });
await browser_click({ element: "긴급 정지", ref: ".btn-emergency-stop" });
await browser_handle_dialog({ accept: true });

// 보유 종목 전량 매도 (선택)
await browser_click({ element: "전량 청산", ref: ".btn-liquidate-all" });
```

## 성과 추적

### 일일 리포트 확인

```javascript
await browser_navigate({ url: "https://www.genport.co.kr/strategy/{strategy_id}/report" });
await browser_snapshot();
```

### 추적 지표

- 일일 수익률
- 누적 수익률
- 실현 손익
- 미실현 손익
- 매매 횟수
- 슬리피지

## 주의사항

- **실전 투자는 손실 위험이 있습니다**
- 반드시 Paper Trading 기간을 거친 후 실전 적용
- 초기에는 소액으로 시작 (500만원 이하)
- 실전 성과가 백테스트와 크게 다를 수 있음 (슬리피지, 유동성 문제)
- 정기적인 성과 리뷰 및 전략 조정 필요

