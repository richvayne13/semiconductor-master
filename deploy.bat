@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [SK하이닉스 양산기술 포털] GitHub Pages 자동 배포 스크립트
echo  - 8대 공정 면접 마스터 (index.html)
echo  - 심화 소자·도감 백과 (semiconductor2.html)
echo  - 159 강의 아카이브 (archive_159.html)
echo ======================================================================
echo.

set "REPO_DIR=%~dp0"
cd /d "%REPO_DIR%"

echo [1/3] 변경 사항 스테이징 중...
git add index.html semiconductor2.html archive_159.html README.md deploy.bat

echo [2/3] 커밋 생성 중...
git commit -m "Deploy 8-process master dashboard and semiconductor_2 deep encyclopedia"

echo [3/3] GitHub 원격 저장소에 푸시 중...
git push -u origin main

echo.
echo ======================================================================
echo  배포 완료! 온라인 주소에서 확인하세요:
echo  1. 8대 공정 마스터: https://richvayne13.github.io/semiconductor-master/
echo  2. 반도체_2 심화백과: https://richvayne13.github.io/semiconductor-master/semiconductor2.html
echo  3. 159 원천 아카이브: https://richvayne13.github.io/semiconductor-master/archive_159.html
echo ======================================================================
pause
