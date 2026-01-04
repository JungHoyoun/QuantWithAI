@echo off
REM 키움 브로커 서버 실행 (32비트 Python)
REM 이 스크립트는 64비트 메인 애플리케이션 시작 전에 실행해야 합니다.

echo [키움 브로커 서버 시작]
echo.

set PROJECT_ROOT=%~dp0..
cd /d %PROJECT_ROOT%

REM 32비트 가상환경 활성화
if exist ".venv-kiwoom-32\Scripts\activate.bat" (
    call .venv-kiwoom-32\Scripts\activate.bat
) else (
    echo [오류] 32비트 가상환경을 찾을 수 없습니다.
    echo 먼저 다음 명령을 실행하세요:
    echo   C:\Python311-32\python.exe -m venv .venv-kiwoom-32
    echo   .venv-kiwoom-32\Scripts\pip install -r requirements-kiwoom.txt
    pause
    exit /b 1
)

REM 서버 실행
echo 키움 서버 시작 중... (종료: Ctrl+C)
python -m src.broker.kiwoom.server

pause
