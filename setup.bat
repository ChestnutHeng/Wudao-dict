@echo off
set DESKTOP_ENTRY='~\Desktop'
set PROGRAM=pythonw
set ARGUMENT=%cd%\wudao-dict\mainwindow.py
set LINK_NAME=无道词典
set WORK_DIR=%cd%\wudao-dict
set ICON=%cd%\wudao-dict\Logo.ico
set DESC=有道即无道，一个简洁的跨平台词典
cd %~dp0

echo %cd% | find /i "wudao-dict" && set flag=true || set flag=false
if %flag%==false (
	echo 请进入 Wudao-dict 文件夹再运行此脚本
	echo 终止安装
	pause
	exit 1
)

rem 安装依赖
pip3.exe install pyqt5 bs4 lxml

rem 用户词
if not exist .\wudao-dict\user (
 	mkdir .\wudao-dict\user\
)

rem 创建桌面图标
echo Set WshShell=CreateObject("WScript.Shell") >makelnk.vbs
echo strDesKtop=WshShell.SpecialFolders("DesKtop") >>makelnk.vbs
echo Set oShellLink=WshShell.CreateShortcut(strDesktop^&"\%LINK_NAME%.lnk") >>makelnk.vbs
echo oShellLink.TargetPath="%PROGRAM%" >>makelnk.vbs
echo oShellLink.Arguments="%ARGUMENT%" >>makelnk.vbs
echo oShellLink.WorkingDirectory="%WORK_DIR%" >>makelnk.vbs
echo oShellLink.WindowStyle=1 >>makelnk.vbs
echo oShellLink.IconLocation = "%ICON%" >>makelnk.vbs
echo oShellLink.Description="%DESC%" >>makelnk.vbs
echo oShellLink.Save >>makelnk.vbs
echo 桌面快捷方式创建成功！
makelnk.vbs
del /f /q makelnk.vbs
echo 安装完成！
echo 使用方式：双击桌面“无道词典”图标
echo Enjoy it!
pause
exit

