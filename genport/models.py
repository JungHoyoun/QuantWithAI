"""젠포트 데이터 모델."""

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class BacktestParams:
    """백테스트 파라미터."""

    start_date: date
    end_date: date
    initial_capital: int = 10_000_000  # 초기 자본금 (원)
    commission_rate: float = 0.00015  # 수수료율 (0.015%)
    slippage: float = 0.001  # 슬리피지 (0.1%)
    max_holdings: int = 10  # 최대 보유 종목 수


@dataclass
class BacktestResult:
    """백테스트 결과."""

    total_return: float  # 총 수익률
    cagr: float  # 연환산 수익률
    sharpe_ratio: float  # 샤프 비율
    max_drawdown: float  # 최대 낙폭
    win_rate: float  # 승률
    trade_count: int  # 총 거래 횟수
    raw_data: dict[str, Any]  # 원본 데이터
