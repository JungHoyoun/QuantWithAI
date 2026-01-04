"""공통 브로커 인터페이스 정의."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class OrderSide(Enum):
    """주문 방향."""

    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """주문 유형."""

    MARKET = "market"  # 시장가
    LIMIT = "limit"  # 지정가


@dataclass
class Order:
    """주문 정보."""

    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: Optional[Decimal] = None  # 지정가 주문시 필수
    order_id: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Position:
    """포지션 정보."""

    symbol: str
    quantity: int
    avg_price: Decimal
    current_price: Decimal
    unrealized_pnl: Decimal


@dataclass
class OHLCV:
    """캔들 데이터."""

    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class BrokerInterface(ABC):
    """브로커 API 공통 인터페이스.

    모든 브로커 구현체는 이 인터페이스를 상속받아야 합니다.
    """

    @abstractmethod
    def connect(self) -> bool:
        """브로커 서버에 연결합니다."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """브로커 서버 연결을 해제합니다."""
        pass

    @abstractmethod
    def get_balance(self) -> Decimal:
        """계좌 잔고를 조회합니다."""
        pass

    @abstractmethod
    def get_positions(self) -> list[Position]:
        """보유 포지션 목록을 조회합니다."""
        pass

    @abstractmethod
    def submit_order(self, order: Order) -> str:
        """주문을 제출하고 주문 ID를 반환합니다."""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """주문을 취소합니다."""
        pass

    @abstractmethod
    def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """과거 시세 데이터를 조회합니다."""
        pass

