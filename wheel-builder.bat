@echo off
REM Build wheel distribution for Tic Tac Toe

echo Building wheel for tictactoe...
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
)

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist src\tictactoe.egg-info rmdir /s /q src\tictactoe.egg-info

REM Build the wheel
python -m build --wheel

REM Check if build was successful
if not exist dist (
    echo ERROR: Build failed - dist folder not created
    pause
    exit /b 1
)

REM Get the actual wheel filename
for %%f in (dist\*.whl) do set WHEEL_FILE=%%~nxf

REM Copy favicon to dist
if exist src\tictactoe\assets\favicon.ico (
    copy src\tictactoe\assets\favicon.ico dist\ >nul
    echo Copied favicon.ico to dist folder
) else (
    echo WARNING: favicon.ico not found
)

REM Create installation.bat
(
echo @echo off
echo setlocal enabledelayedexpansion
echo.
echo REM Define installation directory
echo set INSTALL_DIR=%%LOCALAPPDATA%%\Programs\ttt.v0.1.0
echo.
echo echo Installing Tic Tac Toe...
echo echo.
echo echo Checking for existing installation...
echo if exist "%%INSTALL_DIR%%" ^(
echo     echo Found existing installation. Removing old version...
echo     rmdir /s /q "%%INSTALL_DIR%%"
echo     echo Old version removed.
echo     echo.
echo ^)
echo.
echo echo Creating installation directory...
echo if not exist "%%INSTALL_DIR%%" mkdir "%%INSTALL_DIR%%"
echo.
echo echo Copying files to %%INSTALL_DIR%%...
echo xcopy /Y /Q "%%~dp0*.*" "%%INSTALL_DIR%%\"
echo.
echo echo Creating virtual environment...
echo python -m venv "%%INSTALL_DIR%%\.venv"
echo if errorlevel 1 ^(
echo     echo.
echo     echo Failed to create virtual environment!
echo     echo Please make sure Python is installed and in your PATH.
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Activating virtual environment...
echo call "%%INSTALL_DIR%%\.venv\Scripts\activate.bat"
echo.
echo echo Installing package and dependencies...
echo pip install "%%INSTALL_DIR%%\%WHEEL_FILE%"
echo if errorlevel 1 ^(
echo     echo.
echo     echo Installation failed!
echo     pause
echo     exit /b 1
echo ^)
echo echo.
echo echo Creating desktop shortcut...
echo echo.
echo.
echo REM Get the desktop path ^(works with OneDrive^)
echo for /f "usebackq tokens=3*" %%%%A in ^(`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`^) do set DESKTOP=%%%%A %%%%B
echo set DESKTOP=%%DESKTOP:~0,-1%%
echo if "%%DESKTOP:~-1%%"==" " set DESKTOP=%%DESKTOP:~0,-1%%
echo.
echo REM Expand environment variables in path
echo call set DESKTOP=%%DESKTOP%%
echo.
echo REM Get current directory for paths
echo set SCRIPT_DIR=%%INSTALL_DIR%%\
echo set ICON_PATH=%%SCRIPT_DIR%%favicon.ico
echo set VBS_PATH=%%SCRIPT_DIR%%tic-tac-toe-starter.vbs
echo.
echo REM Create VBScript to make the shortcut
echo echo Set oWS = WScript.CreateObject("WScript.Shell"^) ^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo sLinkFile = "%%DESKTOP%%\Tic Tac Toe.lnk" ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo Set oLink = oWS.CreateShortcut(sLinkFile^) ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo oLink.TargetPath = "%%VBS_PATH%%" ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo oLink.IconLocation = "%%ICON_PATH%%" ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo oLink.WorkingDirectory = "%%SCRIPT_DIR%%" ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo echo oLink.Save ^>^> "%%TEMP%%\create_ttt_shortcut.vbs"
echo.
echo cscript //nologo "%%TEMP%%\create_ttt_shortcut.vbs"
echo del "%%TEMP%%\create_ttt_shortcut.vbs"
echo.
echo echo.
echo echo Installation complete!
echo echo Desktop shortcut created successfully.
echo echo You can now run the game from the desktop or by typing: tictactoe
echo echo.
echo pause
) > dist\installation.bat

REM Create tic-tac-toe-starter.vbs
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run """%%LOCALAPPDATA%%\Programs\ttt.v0.1.0\.venv\Scripts\pythonw.exe"" -m tictactoe", 0
echo Set WshShell = Nothing
) > dist\tic-tac-toe-starter.vbs

echo.
echo Build complete!
echo Wheel files, installation script, and starter are in the dist\ folder
echo.
pause
