@echo off
echo Installing Python dependencies for websocket script...
py -m pip install websockets soundfile numpy

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies. Please check your Python and pip installation.
    echo You might need to install Microsoft C++ Build Tools if numpy fails.
    echo For soundfile issues, ensure libsndfile is accessible or correctly installed.
) else (
    echo.
    echo Dependencies installed successfully.
)

echo.
pause 