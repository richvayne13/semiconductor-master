@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [반도체 159 훈련과정 원문인라인 도해 대시보드 v2.0 재생성 파이프라인]
echo ======================================================================
echo.

set "TOOL_DIR=%~dp0"
set "BASE_DIR=%TOOL_DIR%..\..\"

echo [1/2] 원문 도해-텍스트 인라인 결합 및 영문 코드 분류 중...
python "%TOOL_DIR%build_content.py"

echo [2/2] v2.0 대시보드 HTML 빌드 및 이미지 동기화 중...
python "%TOOL_DIR%build_dashboard.py"

echo.
echo ======================================================================
echo  빌드 완료! 브라우저에서 아래 대시보드를 실행합니다:
echo  %BASE_DIR%result\index.html
echo ======================================================================
start "" "%BASE_DIR%result\index.html"
pause
