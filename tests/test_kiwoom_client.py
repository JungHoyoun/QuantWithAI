"""키움 클라이언트 테스트."""

import pytest

from src.broker.kiwoom import KiwoomClient, KiwoomClientError


def test_kiwoom_client_creation() -> None:
    """KiwoomClient 생성 테스트."""
    client = KiwoomClient()
    assert client.server_address == "tcp://127.0.0.1:5555"
    assert client.timeout_ms == 5000


def test_kiwoom_client_custom_address() -> None:
    """KiwoomClient 커스텀 주소 테스트."""
    client = KiwoomClient(server_address="tcp://127.0.0.1:9999", timeout_ms=10000)
    assert client.server_address == "tcp://127.0.0.1:9999"
    assert client.timeout_ms == 10000


def test_kiwoom_client_ping_without_server() -> None:
    """서버 없이 ping 테스트 (실패 예상)."""
    client = KiwoomClient(timeout_ms=100)  # 빠른 타임아웃
    result = client.ping()
    assert result is False  # 서버가 없으므로 False
