@echo off

:: Exit on error
set -e

:: Check Python version is 3.10 or higher
for /f "tokens=2" %%v in ('python -V 2^>^&1') do (
    for /f "tokens=1,2 delims=." %%x in ("%%v") do (
        if %%x LSS 3 (
            if %%y LSS 10 (
                echo Python version must be 3.10 or higher
                exit /b 1
            )
        )
    )
)

:: Check Node version is 16 or higher
for /f "tokens=2 delims=v." %%v in ('node -v 2^>^&1') do (
    if %%v LSS 16 (
        echo Node version must be 16 or higher
        exit /b 1
    )
)

:: Create virtual environment
cd src
python -m venv venv
call venv\Scripts\activate.bat
pip install rich fastapi pydantic watchfiles

cd socket-server
npm install

cd ../ui
npm install

:: Run the server
:: cd ../src
:: start "" /b cmd /c "uvicorn app:app --reload"

:: Run the socket server in a new terminal
:: start "" /b cmd /c "cd ../socket-server & node server.js"

:: Run the UI on a separate terminal
:: start "" /b cmd /c "cd ../ui & npm start"
