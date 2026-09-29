@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ======================================================================
echo [AGY 원클릭 재현 실행기] 파이프라인 자동 실행 및 결과 생성
echo ======================================================================
echo.

:: 1. 디렉터리 경로 설정
set "SCRIPT_DIR=%~dp0"
set "BASE_DIR=%SCRIPT_DIR%..\..\"
set "CONTEXT_DIR=%BASE_DIR%context\"
set "RESULT_DIR=%BASE_DIR%result\"

echo [1/3] 작업 환경 및 경로 검증 중...
echo  - Tool 경로: %SCRIPT_DIR%
echo  - Context 경로: %CONTEXT_DIR%
echo  - Result 경로: %RESULT_DIR%
echo.

:: 2. Python 환경 감지
set "PY_CMD=python"
where %PY_CMD% >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        set "PY_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    ) else (
        echo [오류] 시스템에서 Python 실행 파일을 찾을 수 없습니다.
        pause
        exit /b 1
    )
)

echo [2/3] 파이프라인 스크립트 실행 중... (%PY_CMD%)
if exist "%SCRIPT_DIR%main.py" (
    "%PY_CMD%" "%SCRIPT_DIR%main.py"
) else (
    echo [안내] main.py가 아직 생성되지 않았습니다. 단일 테스트 또는 스크립트를 배치하세요.
)
echo.

echo [3/3] 실행 완료! 산출물은 %RESULT_DIR% 에 저장되었습니다.
echo ======================================================================
pause
