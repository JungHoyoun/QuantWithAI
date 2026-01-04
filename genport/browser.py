"""젠포트 브라우저 제어 모듈.

Playwright를 사용하여 젠포트 웹사이트를 자동화합니다.
"""

import os
from typing import Optional

from playwright.async_api import Browser, Page, async_playwright


class GenportBrowser:
    """젠포트 브라우저 자동화 클래스."""

    GENPORT_URL = "https://www.genport.co.kr"

    def __init__(self, headless: bool = False):
        """
        Args:
            headless: 헤드리스 모드 실행 여부. False면 브라우저 UI 표시.
        """
        self.headless = headless
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self) -> None:
        """브라우저를 시작합니다."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._page = await self._browser.new_page()

    async def close(self) -> None:
        """브라우저를 종료합니다."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    @property
    def page(self) -> Page:
        """현재 페이지 객체를 반환합니다."""
        if not self._page:
            raise RuntimeError("브라우저가 시작되지 않았습니다. start()를 먼저 호출하세요.")
        return self._page

    async def login(self, user_id: Optional[str] = None, password: Optional[str] = None) -> bool:
        """젠포트에 로그인합니다.

        Args:
            user_id: 젠포트 아이디. None이면 환경변수 GENPORT_USER_ID 사용.
            password: 젠포트 비밀번호. None이면 환경변수 GENPORT_PASSWORD 사용.

        Returns:
            로그인 성공 여부.
        """
        user_id = user_id or os.getenv("GENPORT_USER_ID")
        password = password or os.getenv("GENPORT_PASSWORD")

        if not user_id or not password:
            raise ValueError(
                "로그인 정보가 필요합니다. "
                "환경변수 GENPORT_USER_ID, GENPORT_PASSWORD를 설정하거나 직접 전달하세요."
            )

        await self.page.goto(f"{self.GENPORT_URL}/login")
        await self.page.fill('input[name="userId"]', user_id)
        await self.page.fill('input[name="password"]', password)
        await self.page.click('button[type="submit"]')

        # 로그인 성공 확인 (예: 대시보드 페이지로 이동 확인)
        try:
            await self.page.wait_for_url("**/dashboard**", timeout=10000)
            return True
        except Exception:
            return False

    async def navigate_to_strategy(self, strategy_id: str) -> None:
        """특정 전략 페이지로 이동합니다."""
        await self.page.goto(f"{self.GENPORT_URL}/strategy/{strategy_id}")

    async def screenshot(self, path: str) -> None:
        """현재 페이지 스크린샷을 저장합니다."""
        await self.page.screenshot(path=path)

