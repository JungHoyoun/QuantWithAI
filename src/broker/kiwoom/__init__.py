"""키움증권 OpenAPI+ 연동 모듈.

32비트/64비트 분리 아키텍처:
- server.py: 32비트 Python에서 실행, 키움 API 직접 연동
- client.py: 64비트 Python에서 실행, 서버와 ZeroMQ로 통신

64비트 메인 프로세스에서는 KiwoomClient를 사용하세요:

    from src.broker.kiwoom import KiwoomClient

    client = KiwoomClient()
    if client.connect():
        balance = client.get_balance()
"""

from src.broker.kiwoom.client import KiwoomClient, KiwoomClientError

__all__ = ["KiwoomClient", "KiwoomClientError"]
