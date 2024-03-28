@echo off
set ROOT_DIR=%~dp0\..\..
cd /d %ROOT_DIR%

call venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;%ROOT_DIR%\src
cd src\compmath
python main.py %*
