"""젠포트 브라우저 테스트."""

import pytest

from genport.browser import GenportBrowser


def test_genport_browser_creation() -> None:
    """GenportBrowser 생성 테스트."""
    browser = GenportBrowser(headless=True)
    assert browser.headless is True
    assert browser._browser is None
    assert browser._page is None


def test_genport_browser_url() -> None:
    """GenportBrowser URL 상수 테스트."""
    assert GenportBrowser.GENPORT_URL == "https://www.genport.co.kr"


@pytest.mark.asyncio
async def test_genport_browser_context_manager() -> None:
    """GenportBrowser context manager 테스트."""
    async with GenportBrowser(headless=True) as browser:
        assert browser._browser is not None
        assert browser._page is not None
    # context manager 종료 후 브라우저가 닫혀야 함


@pytest.mark.asyncio
async def test_genport_browser_page_property() -> None:
    """GenportBrowser page 프로퍼티 테스트."""
    browser = GenportBrowser(headless=True)

    # 시작 전 page 접근 시 에러
    with pytest.raises(RuntimeError, match="브라우저가 시작되지 않았습니다"):
        _ = browser.page

    # 시작 후 page 접근 가능
    await browser.start()
    try:
        page = browser.page
        assert page is not None
    finally:
        await browser.close()
