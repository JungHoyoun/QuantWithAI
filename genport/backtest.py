"""젠포트 백테스트 자동화 모듈."""

from dataclasses import dataclass
from datetime import date
from typing import Any, Optional

from .browser import GenportBrowser
from .parser import GenportResultParser


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


class GenportBacktest:
    """젠포트 백테스트 실행기."""

    def __init__(self, browser: GenportBrowser):
        """
        Args:
            browser: 젠포트 브라우저 인스턴스.
        """
        self.browser = browser
        self.parser = GenportResultParser()

    async def run(
        self,
        strategy_id: str,
        params: BacktestParams,
    ) -> BacktestResult:
        """백테스트를 실행합니다.

        Args:
            strategy_id: 젠포트 전략 ID.
            params: 백테스트 파라미터.

        Returns:
            백테스트 결과.
        """
        page = self.browser.page

        # 전략 페이지로 이동
        await self.browser.navigate_to_strategy(strategy_id)

        # 백테스트 파라미터 설정
        await self._set_parameters(params)

        # 백테스트 실행
        await page.click('button:has-text("백테스트 실행")')

        # 결과 대기 (최대 5분)
        await page.wait_for_selector(".backtest-result", timeout=300000)

        # 결과 파싱
        result_html = await page.inner_html(".backtest-result")
        return self.parser.parse(result_html)

    async def _set_parameters(self, params: BacktestParams) -> None:
        """백테스트 파라미터를 설정합니다."""
        page = self.browser.page

        # 날짜 설정
        await page.fill('input[name="startDate"]', params.start_date.isoformat())
        await page.fill('input[name="endDate"]', params.end_date.isoformat())

        # 초기 자본금
        await page.fill('input[name="initialCapital"]', str(params.initial_capital))

        # 수수료율
        await page.fill('input[name="commissionRate"]', str(params.commission_rate * 100))

        # 최대 보유 종목 수
        await page.fill('input[name="maxHoldings"]', str(params.max_holdings))

    async def run_parameter_sweep(
        self,
        strategy_id: str,
        base_params: BacktestParams,
        param_grid: dict[str, list[Any]],
    ) -> list[tuple[dict[str, Any], BacktestResult]]:
        """파라미터 스윕을 실행합니다.

        Args:
            strategy_id: 젠포트 전략 ID.
            base_params: 기본 파라미터.
            param_grid: 스윕할 파라미터 그리드. 예: {"max_holdings": [5, 10, 15]}

        Returns:
            (파라미터, 결과) 튜플 리스트.
        """
        results = []

        # 간단한 그리드 서치 구현
        # TODO: itertools.product를 사용한 전체 그리드 서치로 확장
        for param_name, values in param_grid.items():
            for value in values:
                params = BacktestParams(
                    start_date=base_params.start_date,
                    end_date=base_params.end_date,
                    initial_capital=base_params.initial_capital,
                    commission_rate=base_params.commission_rate,
                    slippage=base_params.slippage,
                    max_holdings=base_params.max_holdings,
                )
                setattr(params, param_name, value)

                result = await self.run(strategy_id, params)
                results.append(({param_name: value}, result))

        return results

