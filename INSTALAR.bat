@echo off
echo ========================================
echo  INSTALANDO BOT INSTAGRAM - TWITTER
echo ========================================
echo.

REM Verificar Python
echo [1/3] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK
echo.

REM Instalar dependencias
echo [2/3] Instalando dependencias de Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo.

REM Instalar navegadores Playwright
echo [3/3] Instalando navegadores para Playwright...
playwright install chromium
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Playwright puede no funcionar correctamente
)
echo.

echo ========================================
echo  INSTALACION COMPLETADA!
echo ========================================
echo.
echo Proximo paso:
echo 1. Edita config.py con tus credenciales
echo 2. Ejecuta: PROBAR.bat
echo 3. Ejecuta: EJECUTAR.bat
echo.
pause
