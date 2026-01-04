"""젠포트 결과 파싱 모듈."""

import re
from typing import Any

from .models import BacktestResult


class GenportResultParser:
    """젠포트 백테스트 결과 파서."""

    def parse(self, html: str) -> BacktestResult:
        """HTML에서 백테스트 결과를 파싱합니다.

        Args:
            html: 젠포트 백테스트 결과 HTML.

        Returns:
            파싱된 백테스트 결과.

        Note:
            실제 젠포트 HTML 구조에 맞게 수정 필요.
            현재는 예시 구현입니다.
        """
        raw_data = self._extract_raw_data(html)

        return BacktestResult(
            total_return=raw_data.get("total_return", 0.0),
            cagr=raw_data.get("cagr", 0.0),
            sharpe_ratio=raw_data.get("sharpe_ratio", 0.0),
            max_drawdown=raw_data.get("max_drawdown", 0.0),
            win_rate=raw_data.get("win_rate", 0.0),
            trade_count=raw_data.get("trade_count", 0),
            raw_data=raw_data,
        )

    def _extract_raw_data(self, html: str) -> dict[str, Any]:
        """HTML에서 원본 데이터를 추출합니다.

        Note:
            실제 젠포트 HTML 구조 분석 후 구현 필요.
        """
        data = {}

        # 예시 패턴들 (실제 젠포트 HTML에 맞게 수정 필요)
        patterns = {
            "total_return": r"총\s*수익률[:\s]*(-?\d+\.?\d*)%",
            "cagr": r"연환산\s*수익률[:\s]*(-?\d+\.?\d*)%",
            "sharpe_ratio": r"샤프\s*비율[:\s]*(-?\d+\.?\d*)",
            "max_drawdown": r"최대\s*낙폭[:\s]*(-?\d+\.?\d*)%",
            "win_rate": r"승률[:\s]*(-?\d+\.?\d*)%",
            "trade_count": r"거래\s*횟수[:\s]*(\d+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, html)
            if match:
                value = match.group(1)
                if key == "trade_count":
                    data[key] = int(value)
                else:
                    data[key] = float(value)

        return data

    def parse_trade_history(self, html: str) -> list[dict[str, Any]]:
        """거래 내역을 파싱합니다.

        Args:
            html: 거래 내역 테이블 HTML.

        Returns:
            거래 내역 리스트.
        """
        # TODO: 실제 젠포트 HTML 구조에 맞게 구현
        trades = []
        return trades

