@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [반도체 159 마스터] GitHub Pages 자동 배포 스크립트
echo ======================================================================
echo.

set "REPO_DIR=%~dp0"
cd /d "%REPO_DIR%"

echo [1/3] 변경 사항 스테이징 중...
git add index.html images/ README.md deploy.bat context/ tool/ result/

echo [2/3] 커밋 생성 중...
git commit -m "Deploy semiconductor 159 master dashboard v2.0"

echo [3/3] GitHub 원격 저장소에 푸시 중...
git push -u origin main

echo.
echo ======================================================================
echo  배포 완료! 온라인 주소에서 확인하세요:
echo  https://richvayne13.github.io/semiconductor-master/
echo ======================================================================
pause
