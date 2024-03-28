@echo off
cd /d %~dp0\..\..

call venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;src
cd src\compath
python main.py %*
