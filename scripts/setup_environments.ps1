# 듀얼 Python 환경 설정 스크립트
# PowerShell에서 실행: .\scripts\setup_environments.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "===== Trading System 환경 설정 =====" -ForegroundColor Cyan
Write-Host ""

# 1. Python 설치 확인
Write-Host "[1/5] Python 설치 확인..." -ForegroundColor Yellow

$Python64 = "C:\Python311-64\python.exe"
$Python32 = "C:\Python311-32\python.exe"

if (-not (Test-Path $Python64)) {
    Write-Host "  [오류] Python 3.11 64비트를 찾을 수 없습니다: $Python64" -ForegroundColor Red
    Write-Host "  https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe 에서 다운로드하세요." -ForegroundColor Gray
    exit 1
}
Write-Host "  [OK] Python 64비트: $Python64" -ForegroundColor Green

if (-not (Test-Path $Python32)) {
    Write-Host "  [오류] Python 3.11 32비트를 찾을 수 없습니다: $Python32" -ForegroundColor Red
    Write-Host "  https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe 에서 다운로드하세요." -ForegroundColor Gray
    exit 1
}
Write-Host "  [OK] Python 32비트: $Python32" -ForegroundColor Green

# 2. uv 설치 확인
Write-Host ""
Write-Host "[2/5] uv 설치 확인..." -ForegroundColor Yellow

$uvPath = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvPath) {
    Write-Host "  uv가 설치되어 있지 않습니다. 설치 중..." -ForegroundColor Gray
    irm https://astral.sh/uv/install.ps1 | iex

    # PATH 새로고침
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
Write-Host "  [OK] uv 설치 완료" -ForegroundColor Green

# 3. 64비트 메인 환경 설정
Write-Host ""
Write-Host "[3/5] 64비트 메인 환경 설정..." -ForegroundColor Yellow

Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    Write-Host "  가상환경 생성 중..." -ForegroundColor Gray
    uv venv --python $Python64
}

Write-Host "  의존성 설치 중..." -ForegroundColor Gray
uv sync

Write-Host "  [OK] 64비트 환경 준비 완료" -ForegroundColor Green

# 4. 32비트 키움 환경 설정
Write-Host ""
Write-Host "[4/5] 32비트 키움 환경 설정..." -ForegroundColor Yellow

if (-not (Test-Path ".venv-kiwoom-32")) {
    Write-Host "  가상환경 생성 중..." -ForegroundColor Gray
    & $Python32 -m venv .venv-kiwoom-32
}

Write-Host "  의존성 설치 중..." -ForegroundColor Gray
& ".\.venv-kiwoom-32\Scripts\pip.exe" install -q -r requirements-kiwoom.txt

Write-Host "  [OK] 32비트 환경 준비 완료" -ForegroundColor Green

# 5. Playwright 브라우저 설치
Write-Host ""
Write-Host "[5/5] Playwright 브라우저 설치..." -ForegroundColor Yellow
uv run playwright install chromium
Write-Host "  [OK] Playwright 준비 완료" -ForegroundColor Green

# 완료
Write-Host ""
Write-Host "===== 설정 완료 =====" -ForegroundColor Cyan
Write-Host ""
Write-Host "사용 방법:" -ForegroundColor White
Write-Host "  1. 키움 서버 시작: .\scripts\start_kiwoom_server.bat" -ForegroundColor Gray
Write-Host "  2. 메인 환경 활성화: .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  3. 테스트 실행: uv run pytest" -ForegroundColor Gray
Write-Host ""
