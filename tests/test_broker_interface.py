"""브로커 인터페이스 테스트."""

from decimal import Decimal

from src.broker.interface import OHLCV, Order, OrderSide, OrderType, Position


def test_order_creation() -> None:
    """Order 생성 테스트."""
    order = Order(
        symbol="005930",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        quantity=10,
        price=Decimal("70000"),
    )
    assert order.symbol == "005930"
    assert order.side == OrderSide.BUY
    assert order.quantity == 10


def test_position_creation() -> None:
    """Position 생성 테스트."""
    position = Position(
        symbol="005930",
        quantity=100,
        avg_price=Decimal("70000"),
        current_price=Decimal("72000"),
        unrealized_pnl=Decimal("200000"),
    )
    assert position.symbol == "005930"
    assert position.quantity == 100
    assert position.unrealized_pnl == Decimal("200000")


def test_order_side_values() -> None:
    """OrderSide enum 값 테스트."""
    assert OrderSide.BUY.value == "buy"
    assert OrderSide.SELL.value == "sell"


def test_order_type_values() -> None:
    """OrderType enum 값 테스트."""
    assert OrderType.MARKET.value == "market"
    assert OrderType.LIMIT.value == "limit"
