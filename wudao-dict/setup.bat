@echo off
if NOT exist usr md usr
echo @echo off >> _wd_.bat
echo set pwd=%%cd%% >> _wd_.bat
echo cd /d %cd% >> _wd_.bat
type _setup.txt >> _wd_.bat
