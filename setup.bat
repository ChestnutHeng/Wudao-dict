@echo off
set DESKTOP_ENTRY='~\Desktop'
set PROGRAM=pythonw
set ARGUMENT=%cd%\wudao-dict\mainwindow.py
set LINK_NAME=�޵��ʵ�
set WORK_DIR=%cd%\wudao-dict
set ICON=%cd%\wudao-dict\Logo.ico
set DESC=�е����޵���һ�����Ŀ�ƽ̨�ʵ�
cd %~dp0

echo %cd% | find /i "wudao-dict" && set flag=true || set flag=false
if %flag%==false (
	echo ����� Wudao-dict �ļ��������д˽ű�
	echo ��ֹ��װ
	pause
	exit 1
)

rem ��װ����
pip3.exe install pyqt5 bs4 lxml

rem �û���
if not exist .\wudao-dict\user (
 	mkdir .\wudao-dict\user\
)

rem ��������ͼ��
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
echo �����ݷ�ʽ�����ɹ���
makelnk.vbs
del /f /q makelnk.vbs
echo ��װ��ɣ�
echo ʹ�÷�ʽ��˫�����桰�޵��ʵ䡱ͼ��
echo Enjoy it!
pause
exit

