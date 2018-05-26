#!/bin/bash
DESKTOP_ENTRY="/usr/share/applications/"
INSTALL_PATH="/usr/bin"
COMPLETION_PATH="/etc/bash_completion.d"

# 用户词
if [ ! -d usr ]
then
    mkdir usr
fi

chmod -R 777 usr

# 添加系统命令wd
echo '#!/bin/bash'>./wd
echo 'save_path=$PWD'>>./wd
echo 'cd '$PWD >>./wd
echo './wdd $*'>>./wd
echo 'cd $save_path'>>./wd
sudo mv ./wd $INSTALL_PATH/wd
sudo chmod +x $INSTALL_PATH/wd

# 添加桌面GUI图标
echo '[Desktop Entry]' > ./wudao.desktop
echo 'Name=Wudao' >> ./wudao.desktop
echo 'Name[zh_CN]=无道词典' >> ./wudao.desktop
echo 'Comment=Youdao is wudao, a powerful dict.' >> ./wudao.desktop
echo 'Comment[zh_CN]=有道即无道，一个强大的词典。' >> ./wudao.desktop
echo "Exec=$PWD/start_gui.sh" >> ./wudao.desktop
echo "Path=$PWD" >> ./wudao.desktop
echo 'Terminal=false' >> ./wudao.desktop
echo 'Type=Application' >> ./wudao.desktop
echo 'Categories=Utility' >> ./wudao.desktop
sudo rm $DESKTOP_ENTRY/wudao.desktop
rm ~/.local/share/applications/wudao.desktop
sudo mv ./wudao.desktop $DESKTOP_ENTRY

# 添加自动补全
sudo rm -f $COMPLETION_PATH/wd
sudo cp wd_com $COMPLETION_PATH/wd
. $COMPLETION_PATH/wd

echo 'Setup Finished! '
echo 'use wd [OPTION]... [WORD] to query the word.'
echo '自动补全会在下次打开命令行时启用'
echo '或者手动运行 source ~/.bashrc'

