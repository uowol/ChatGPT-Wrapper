@echo off
@REM :: Step 1: Install pyenv
@REM echo Installing pyenv...
@REM git clone https://github.com/pyenv-win/pyenv-win.git .pyenv
@REM if %ERRORLEVEL% NEQ 0 (
@REM     echo Error installing pyenv. Exiting.
@REM     exit /b %ERRORLEVEL%
@REM )

@REM :: Step 2: Configure environment variables for pyenv
@REM echo Configuring environment variables for pyenv...
@REM set PYENV_ROOT=%USERPROFILE%\.pyenv\pyenv-win
@REM set PATH=%PYENV_ROOT%\bin;%PYENV_ROOT%\shims;%PATH%

@REM :: Step 3: Install Python 3.10.11 and set it as global
@REM echo Installing Python 3.10.11 with pyenv...
@REM %PYENV_ROOT%\bin\pyenv install 3.10.11
@REM if %ERRORLEVEL% NEQ 0 (
@REM     echo Error installing Python 3.10.11. Exiting.
@REM     exit /b %ERRORLEVEL%
@REM )
@REM %PYENV_ROOT%\bin\pyenv global 3.10.11

:: Step 4: Install Poetry
echo Installing Poetry...
curl -sSL https://install.python-poetry.org | python -
if %ERRORLEVEL% NEQ 0 (
    echo Error installing Poetry. Exiting.
    exit /b %ERRORLEVEL%
)

:: Step 5: Use Python from pyenv in Poetry
echo Configuring Poetry to use Python installed by pyenv...
poetry env use %PYENV_ROOT%\versions\3.10.11\python.exe
if %ERRORLEVEL% NEQ 0 (
    echo Error configuring Poetry environment. Exiting.
    exit /b %ERRORLEVEL%
)

:: Step 6: Install dependencies using Poetry
echo Installing dependencies with Poetry...
poetry install
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies with Poetry. Exiting.
    exit /b %ERRORLEVEL%
)

echo Installation complete!
pause
