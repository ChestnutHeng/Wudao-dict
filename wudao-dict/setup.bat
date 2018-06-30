@echo off
if NOT exist usr md usr
if NOT exist %USERPROFILE%\bin md %USERPROFILE%\bin
echo @echo off >> wd.bat
echo set pwd=%%cd%% >> wd.bat
echo cd /d %cd% >> wd.bat
type _setup.txt >> wd.bat
move wd.bat %USERPROFILE%\bin
