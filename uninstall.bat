@echo off
set DESKTOP_ENTRY=~\Desktop
set LINK_NAME=无道词典.lnk

rem 删除图标
if exist %DESKTOP_ENTRY%\%LINK_NAME% (
	del /f /q %DESKTOP_ENTRY%\%LINK_NAME%
)

echo 卸载完成！
echo 请手动删除 Wudao-dict 文件夹