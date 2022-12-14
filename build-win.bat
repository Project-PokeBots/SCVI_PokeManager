@echo off

cd /D "%~dp0"

pip install pyinstaller

pyinstaller ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --noconsole ^
    --name "SCVI_Pokemanager" ^
    --add-data "assets\Roboto-Regular.ttf;assets" ^
    --add-data "assets\logo.ico;assets" ^
    --icon "assets\logo.ico" ^
    --collect-all px8parse ^
    src\main.py

REM For those who execute the script without commandline
pause
