#!/bin/bash
DESKTOP_ENTRY="/usr/share/applications/"
INSTALL_PATH="/usr/bin"
COMPLETION_PATH="/etc/bash_completion.d"
COLOR_RED='\033[31m'
COLOR_RESET='\033[0m'

if [ ! `pwd | grep wudao` ]
then
    cd wudao-dict 2> /dev/null
    if [ ! `pwd | grep wudao` ] ; then
        echo -e "${COLOR_RED}请进入 Wudao-dict/wudao-dict 再运行此脚本${COLOR_RESET}"
        echo -e "${COLOR_RED}终止安装${COLOR_RESET}"
        exit 1
    fi
fi

# 用户词
if [ ! -d user ]
then
    mkdir user
fi

chmod -R 777 user

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
echo "Icon=$PWD/Logo.ico" >> ./wudao.desktop
echo 'Terminal=false' >> ./wudao.desktop
echo 'Type=Application' >> ./wudao.desktop
echo 'Categories=Utility' >> ./wudao.desktop
sudo rm $DESKTOP_ENTRY/wudao.desktop
sudo mv ./wudao.desktop $DESKTOP_ENTRY

# 添加自动补全
sudo rm -f $COMPLETION_PATH/wd
sudo cp wd_com $COMPLETION_PATH/wd
. $COMPLETION_PATH/wd

echo 'Setup Finished! '
echo 'use wd [OPTION]... [WORD] to query the word.'
echo '自动补全会在下次打开命令行时启用'
echo '或者手动运行 source ~/.bashrc'

