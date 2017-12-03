#!/bin/bash

# 删除系统命令wd
sudo rm -f /usr/bin/wd

# 删除自动补全
sudo rm -f /etc/bash_completion.d/wd

echo 'Uninstall Finished! '

