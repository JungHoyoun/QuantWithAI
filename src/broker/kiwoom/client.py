"""키움증권 64비트 클라이언트.

64비트 메인 프로세스에서 실행되며, 32비트 키움 서버와 ZeroMQ로 통신합니다.
BrokerInterface를 구현하여 다른 브로커와 동일한 인터페이스를 제공합니다.
"""

import os
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

import zmq
from loguru import logger
from pydantic import BaseModel

from src.broker.interface import (
    OHLCV,
    BrokerInterface,
    Order,
    OrderSide,
    OrderType,
    Position,
)

# 서버 설정
DEFAULT_PORT = 5555
SERVER_ADDRESS = f"tcp://127.0.0.1:{os.getenv('KIWOOM_IPC_PORT', DEFAULT_PORT)}"
DEFAULT_TIMEOUT_MS = 5000


class IPCMessage(BaseModel):
    """IPC 메시지 포맷."""

    method: str
    params: dict[str, Any] = {}
    request_id: str | None = None


class IPCResponse(BaseModel):
    """IPC 응답 포맷."""

    success: bool
    data: Any = None
    error: str | None = None
    request_id: str | None = None


class KiwoomClientError(Exception):
    """키움 클라이언트 오류."""

    pass


class KiwoomClient(BrokerInterface):
    """키움증권 브로커 클라이언트.

    32비트 키움 서버와 ZeroMQ로 통신하여 BrokerInterface를 구현합니다.

    Example:
        ```python
        client = KiwoomClient()
        if client.connect():
            balance = client.get_balance()
            positions = client.get_positions()
        ```
    """

    def __init__(
        self,
        server_address: str = SERVER_ADDRESS,
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
    ) -> None:
        """
        Args:
            server_address: 키움 서버 주소 (기본: tcp://127.0.0.1:5555)
            timeout_ms: 요청 타임아웃 (밀리초)
        """
        self.server_address = server_address
        self.timeout_ms = timeout_ms
        self._context: zmq.Context | None = None
        self._socket: zmq.Socket | None = None
        self._connected = False

    def _ensure_socket(self) -> zmq.Socket:
        """소켓이 준비되어 있는지 확인하고 반환합니다."""
        if self._socket is None:
            self._context = zmq.Context()
            self._socket = self._context.socket(zmq.REQ)
            self._socket.setsockopt(zmq.RCVTIMEO, self.timeout_ms)
            self._socket.setsockopt(zmq.SNDTIMEO, self.timeout_ms)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.connect(self.server_address)
        return self._socket

    def _send_request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """서버에 요청을 보내고 응답을 받습니다."""
        socket = self._ensure_socket()
        request_id = str(uuid.uuid4())

        msg = IPCMessage(
            method=method,
            params=params or {},
            request_id=request_id,
        )

        try:
            socket.send_string(msg.model_dump_json())
            response_str = socket.recv_string()
            response = IPCResponse.model_validate_json(response_str)

            if not response.success:
                raise KiwoomClientError(response.error or "알 수 없는 오류")

            return response.data

        except zmq.Again:
            # 타임아웃 발생 시 소켓 재생성
            self._reset_socket()
            raise KiwoomClientError(f"요청 타임아웃: {method}")

        except zmq.ZMQError as e:
            self._reset_socket()
            raise KiwoomClientError(f"통신 오류: {e}")

    def _reset_socket(self) -> None:
        """소켓을 재설정합니다."""
        if self._socket:
            self._socket.close()
            self._socket = None

    def ping(self) -> bool:
        """서버 연결 테스트."""
        try:
            result = self._send_request("ping")
            return result.get("pong", False)
        except KiwoomClientError:
            return False

    # === BrokerInterface 구현 ===

    def connect(self) -> bool:
        """키움 API에 연결합니다."""
        try:
            result = self._send_request("connect")
            self._connected = result.get("connected", False)
            if self._connected:
                logger.info("키움 API 연결 성공")
            return self._connected
        except KiwoomClientError as e:
            logger.error(f"키움 API 연결 실패: {e}")
            return False

    def disconnect(self) -> None:
        """키움 API 연결을 해제합니다."""
        try:
            self._send_request("disconnect")
            self._connected = False
            logger.info("키움 API 연결 해제")
        except KiwoomClientError as e:
            logger.warning(f"연결 해제 중 오류: {e}")
        finally:
            self._reset_socket()
            if self._context:
                self._context.term()
                self._context = None

    def get_balance(self) -> Decimal:
        """계좌 잔고를 조회합니다."""
        result = self._send_request("get_balance")
        return Decimal(result.get("balance", "0"))

    def get_positions(self) -> list[Position]:
        """보유 포지션 목록을 조회합니다."""
        result = self._send_request("get_positions")
        positions = []
        for pos in result:
            positions.append(
                Position(
                    symbol=pos["symbol"],
                    quantity=pos["quantity"],
                    avg_price=Decimal(str(pos["avg_price"])),
                    current_price=Decimal(str(pos["current_price"])),
                    unrealized_pnl=Decimal(str(pos.get("unrealized_pnl", "0"))),
                )
            )
        return positions

    def submit_order(self, order: Order) -> str:
        """주문을 제출하고 주문 ID를 반환합니다."""
        params = {
            "symbol": order.symbol,
            "side": order.side.value,
            "order_type": order.order_type.value,
            "quantity": order.quantity,
            "price": str(order.price) if order.price else None,
        }
        result = self._send_request("submit_order", params)
        return result.get("order_id", "")

    def cancel_order(self, order_id: str) -> bool:
        """주문을 취소합니다."""
        result = self._send_request("cancel_order", {"order_id": order_id})
        return result.get("cancelled", False)

    def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """과거 시세 데이터를 조회합니다."""
        params = {
            "symbol": symbol,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "interval": interval,
        }
        result = self._send_request("get_historical_data", params)

        ohlcv_list = []
        for candle in result:
            ohlcv_list.append(
                OHLCV(
                    timestamp=datetime.fromisoformat(candle["timestamp"]),
                    open=Decimal(str(candle["open"])),
                    high=Decimal(str(candle["high"])),
                    low=Decimal(str(candle["low"])),
                    close=Decimal(str(candle["close"])),
                    volume=candle["volume"],
                )
            )
        return ohlcv_list

    def __enter__(self) -> "KiwoomClient":
        """컨텍스트 매니저 진입."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """컨텍스트 매니저 종료."""
        self.disconnect()
