#!/bin/bash

# 트레이딩 관련 문서 동기화 스크립트
# Google Drive → ~/HY/trading-system/docs/

set -e

DRIVE_BASE="/Users/hoyounjung/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles"
DOCS_DIR="$HOME/HY/trading-system/docs"

echo "📚 트레이딩 관련 문서 동기화 시작..."
echo ""

# 자산관리 계획
echo "→ 2026_자산관리_계획.md"
cp "$DRIVE_BASE/Areas/Rich/2026_자산관리_계획.md" "$DOCS_DIR/"

# 알고리즘 트레이딩 폴더의 모든 .md 파일
echo "→ 알고리즘 트레이딩 문서들..."
cp "$DRIVE_BASE/Areas/Rich/알고리즘 트레이딩/"*.md "$DOCS_DIR/"

echo ""
echo "✅ 동기화 완료!"
echo ""
echo "복사된 파일 목록:"
ls -1 "$DOCS_DIR/"*.md | xargs -n 1 basename

echo ""
echo "마지막 동기화: $(date '+%Y-%m-%d %H:%M:%S')"

