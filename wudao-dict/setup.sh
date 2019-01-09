#!/bin/bash

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

sysOS=`uname -s`
if [ $sysOS == "Darwin" ];then
    sudo cp ./wd /usr/local/bin/wd
    sudo chmod +x /usr/local/bin/wd
    # 添加bash自动补全
    sudo rm -f /usr/local/etc/bash_completion.d/wd
    sudo cp wd_com /usr/local/etc/bash_completion.d/wd
    . /usr/local/etc/bash_completion.d/wd
else
    sudo cp ./wd /usr/bin/wd
    sudo chmod +x /usr/bin/wd
    # 添加bash_completion自动补全
    sudo rm -f /etc/bash_completion.d/wd
    sudo cp wd_com /etc/bash_completion.d/wd
    . /etc/bash_completion.d/wd
fi

echo 'Setup Finished! '
echo 'use wd [OPTION]... [WORD] to query the word.'
echo '自动补全(仅支持bash)会在下次打开命令行时启用'
echo '或者手动运行 source ~/.bashrc'
