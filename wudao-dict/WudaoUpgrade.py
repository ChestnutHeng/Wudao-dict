from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import quote
import os
import urllib.error

RED_PATTERN = '\033[31m%s\033[0m'

def ie():
    try:
        urlopen('http://www.baidu.com', timeout=1)
        return True
    except urllib.error.URLError as err: 
        return False

def get_update():
    local_ver = None
    if os.path.exists('./Ver'):
        with open('./Ver', 'r') as f:
            local_ver =  float(f.read().strip())
    
    if ie():
        try:
            res = urlopen('http://chestnutheng.cn/Ver', timeout=1)
            xml = res.read().decode('utf-8')
            #xml = '1.0'
            web_ver = float(xml.strip())
            if web_ver > local_ver:
                print('-'*60)
                print(RED_PATTERN % '新的版本已经发布！请在wudao-dict下运行git pull更新。')
                print('-'*60)
        except:
            pass
          
if __name__ == '__main__':
    print(get_update())    
