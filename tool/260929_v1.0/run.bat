@echo off
chcp 65001 > nul
setlocal

echo ======================================================================
echo  [반도체 159개 훈련과정 CORE 면접 대시보드 재생성 파이프라인]
echo ======================================================================
echo.

set "TOOL_DIR=%~dp0"
set "BASE_DIR=%TOOL_DIR%..\..\"

echo [1/3] 신규 포스트 수집 및 이미지 다운로드 확인 중...
python "%TOOL_DIR%crawler_all.py"

echo [2/3] CORE 프레임워크 및 카테고리 매핑 중...
python "%TOOL_DIR%core_builder.py"

echo [3/3] 대시보드 HTML 빌드 및 이미지 동기화 중...
python "%TOOL_DIR%build_dashboard.py"

echo.
echo ======================================================================
echo  빌드 완료! 브라우저에서 아래 대시보드를 실행합니다:
echo  %BASE_DIR%result\index.html
echo ======================================================================
start "" "%BASE_DIR%result\index.html"
pause
