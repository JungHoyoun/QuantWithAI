# 참고 문서

이 폴더는 Google Drive에 있는 트레이딩 관련 문서들의 **스냅샷**입니다.  
Claude Code가 컨텍스트로 활용할 수 있도록 복사해두었습니다.

---

## 📚 문서 목록

### 계획 & 전략
- **2026_자산관리_계획.md** - 전체 자산 관리 계획, 월급 배분, 로드맵
- **퀀트_트레이딩_상세_계획.md** - 시스템 개발 상세 계획, 체크리스트
- **레버리지_전략.md** - 주담대 준비, 리스크 관리, 시뮬레이션

### 학습 자료
- **퀀트_트레이딩_가이드.md** - 퀀트 트레이딩 기초 지식
- **알고리즘_트레이딩_시스템_구축.md** - 시스템 구축 가이드
- **트레이딩_시작_가이드.md** - 실전 트레이딩 시작 가이드

### AI 도구
- **AI_Trading_Agent_Prompt.md** - Antigravity용 프롬프트

---

## 🔄 동기화 방법

### 자동 동기화 (추천)

프로젝트 루트에 동기화 스크립트 실행:

```bash
cd ~/HY/trading-system
./sync_docs.sh
```

### 수동 동기화

원본이 업데이트되면 다시 복사:

```bash
cp "/Users/hoyounjung/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles/Areas/Rich/2026_자산관리_계획.md" ~/HY/trading-system/docs/

cp "/Users/hoyounjung/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles/Areas/Rich/알고리즘 트레이딩/"*.md ~/HY/trading-system/docs/
```

---

## ⚠️ 주의사항

1. **이 폴더의 문서는 읽기 전용으로 사용**
   - 수정 사항은 원본(Google Drive)에서 해야 함
   - 이 폴더는 단순 참고용 스냅샷

2. **원본 위치**
   ```
   ~/Library/CloudStorage/GoogleDrive-ghdbsl98@gmail.com/내 드라이브/DriveSyncFiles/
   ├── Areas/Rich/
   │   ├── 2026_자산관리_계획.md
   │   └── 알고리즘 트레이딩/
   │       ├── 퀀트_트레이딩_가이드.md
   │       ├── 퀀트_트레이딩_상세_계획.md
   │       ├── 알고리즘_트레이딩_시스템_구축.md
   │       ├── 레버리지_전략.md
   │       ├── AI_Trading_Agent_Prompt.md
   │       └── 트레이딩_시작_가이드.md
   ```

3. **정기적으로 동기화**
   - 원본 문서가 업데이트되면 `sync_docs.sh` 실행
   - 또는 주 1회 정도 수동 동기화

---

**최종 동기화**: 2026-01-04  
**다음 동기화**: 필요 시 or 주 1회

