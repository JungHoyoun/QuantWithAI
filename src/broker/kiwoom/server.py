"""키움증권 32비트 브로커 서버.

32비트 Python에서 실행되며, 64비트 메인 프로세스와 ZeroMQ로 통신합니다.
키움 OpenAPI+는 32비트 COM 객체이므로 반드시 32비트 Python에서 실행해야 합니다.

실행 방법:
    .venv-kiwoom-32\\Scripts\\python.exe -m src.broker.kiwoom.server
"""

import json
import os
import sys
from datetime import datetime
from decimal import Decimal
from typing import Any

import zmq
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel

# PyQt5는 키움 API 이벤트 루프에 필요
from PyQt5.QtWidgets import QApplication

load_dotenv()

# 서버 설정
DEFAULT_PORT = 5555
BIND_ADDRESS = f"tcp://127.0.0.1:{os.getenv('KIWOOM_IPC_PORT', DEFAULT_PORT)}"


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


class KiwoomServer:
    """키움 API 브로커 서버.

    ZeroMQ REP 소켓으로 명령을 수신하고,
    키움 OpenAPI+를 통해 실행 후 결과를 반환합니다.
    """

    def __init__(self, bind_address: str = BIND_ADDRESS) -> None:
        self.bind_address = bind_address
        self._context: zmq.Context | None = None
        self._socket: zmq.Socket | None = None
        self._kiwoom: Any = None  # TODO: KiwoomAPI 인스턴스
        self._running = False

    def start(self) -> None:
        """서버를 시작합니다."""
        logger.info(f"키움 브로커 서버 시작: {self.bind_address}")

        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(self.bind_address)

        # TODO: 키움 API 초기화
        # self._kiwoom = KiwoomAPI()
        # self._kiwoom.connect()

        self._running = True
        logger.info("서버 준비 완료, 요청 대기 중...")

        self._run_loop()

    def stop(self) -> None:
        """서버를 중지합니다."""
        self._running = False
        if self._socket:
            self._socket.close()
        if self._context:
            self._context.term()
        logger.info("서버 종료")

    def _run_loop(self) -> None:
        """메인 이벤트 루프."""
        while self._running:
            try:
                # 요청 수신 (타임아웃 1초)
                if self._socket.poll(1000):
                    message = self._socket.recv_string()
                    response = self._handle_request(message)
                    self._socket.send_string(response)
            except zmq.ZMQError as e:
                logger.error(f"ZMQ 오류: {e}")
            except KeyboardInterrupt:
                logger.info("키보드 인터럽트 수신")
                break

        self.stop()

    def _handle_request(self, raw_message: str) -> str:
        """요청을 처리하고 응답을 반환합니다."""
        try:
            msg = IPCMessage.model_validate_json(raw_message)
            logger.debug(f"요청 수신: {msg.method}")

            # 메서드 라우팅
            handler = getattr(self, f"_handle_{msg.method}", None)
            if handler is None:
                return IPCResponse(
                    success=False,
                    error=f"알 수 없는 메서드: {msg.method}",
                    request_id=msg.request_id,
                ).model_dump_json()

            result = handler(msg.params)
            return IPCResponse(
                success=True,
                data=result,
                request_id=msg.request_id,
            ).model_dump_json()

        except Exception as e:
            logger.exception(f"요청 처리 오류: {e}")
            return IPCResponse(
                success=False,
                error=str(e),
            ).model_dump_json()

    # === 핸들러 메서드 ===

    def _handle_ping(self, params: dict) -> dict:
        """연결 테스트."""
        return {"pong": True, "timestamp": datetime.now().isoformat()}

    def _handle_connect(self, params: dict) -> dict:
        """키움 API 연결."""
        # TODO: 실제 키움 API 연결 구현
        logger.info("키움 API 연결 요청")
        return {"connected": True}

    def _handle_disconnect(self, params: dict) -> dict:
        """키움 API 연결 해제."""
        # TODO: 실제 키움 API 연결 해제 구현
        logger.info("키움 API 연결 해제 요청")
        return {"disconnected": True}

    def _handle_get_balance(self, params: dict) -> dict:
        """계좌 잔고 조회."""
        # TODO: 실제 구현
        logger.info("잔고 조회 요청")
        return {"balance": "0", "currency": "KRW"}

    def _handle_get_positions(self, params: dict) -> list:
        """보유 포지션 조회."""
        # TODO: 실제 구현
        logger.info("포지션 조회 요청")
        return []

    def _handle_submit_order(self, params: dict) -> dict:
        """주문 제출."""
        # TODO: 실제 구현
        logger.info(f"주문 제출 요청: {params}")
        return {"order_id": "MOCK_ORDER_ID", "status": "submitted"}

    def _handle_cancel_order(self, params: dict) -> dict:
        """주문 취소."""
        order_id = params.get("order_id")
        # TODO: 실제 구현
        logger.info(f"주문 취소 요청: {order_id}")
        return {"order_id": order_id, "cancelled": True}

    def _handle_get_historical_data(self, params: dict) -> list:
        """과거 시세 데이터 조회."""
        symbol = params.get("symbol")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        interval = params.get("interval", "1d")
        # TODO: 실제 구현
        logger.info(f"시세 데이터 조회: {symbol} ({start_date} ~ {end_date})")
        return []


def main() -> None:
    """서버 메인 엔트리포인트."""
    # 32비트 Python 확인
    if sys.maxsize > 2**32:
        logger.warning("64비트 Python에서 실행 중입니다. 키움 API는 32비트 Python이 필요합니다.")

    # PyQt5 애플리케이션 (키움 API 이벤트 루프용)
    app = QApplication(sys.argv)

    server = KiwoomServer()

    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()


if __name__ == "__main__":
    main()
