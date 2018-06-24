#!/bin/bash
DESKTOP_ENTRY="/usr/share/applications/"
INSTALL_PATH="/usr/bin"
COMPLETION_PATH="/etc/bash_completion.d"

# 关闭服务
wd -k
# 删除系统命令wd
sudo rm -f $INSTALL_PATH/wd

# 删除自动补全
sudo rm -f $COMPLETION_PATH/wd

# 删除桌面图标
sudo rm -f $DESKTOP_ENTRY/wudao.desktop

echo 'Uninstall Finished! '
echo '请手动删除 Wudao-dict 文件夹'

