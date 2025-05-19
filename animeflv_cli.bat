@echo off
setlocal

cd /d "%~dp0"

set VENV_DIR=venv
set SCRIPT=animeflv_cli.py

:: Verificar si Python está instalado
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python no se encuentra en el PATH.
    echo Puedes instalarlo con:
    echo     scoop install python
    echo o descargarlo desde https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verificar si mpv está disponible
where mpv >nul 2>nul
if errorlevel 1 (
    echo [ERROR] mpv no se encuentra en el PATH.
    echo Puedes instalarlo con: scoop install mpv
    pause
    exit /b 1
)

:: Verificar si yt-dlp está disponible
where yt-dlp >nul 2>nul
if errorlevel 1 (
    echo [ERROR] yt-dlp no se encuentra en el PATH.
    echo Puedes instalarlo con: scoop install yt-dlp
    pause
    exit /b 1
)

:: Verificar si el entorno virtual no existe
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Entorno virtual no encontrado. Creando...
    python -m venv %VENV_DIR%

    echo [INFO] Activando entorno virtual...
    call "%VENV_DIR%\Scripts\activate.bat"

    echo [INFO] Instalando dependencias...
    pip install --upgrade pip
    pip install -r requirements.txt

    echo [INFO] Instalando navegadores para Playwright...
    playwright install firefox
)

echo [INFO] Activando entorno virtual...
call "%VENV_DIR%\Scripts\activate.bat"

:: Ejecutar el script principal
echo [INFO] Ejecutando %SCRIPT%...
python "%SCRIPT%" %*

endlocal
