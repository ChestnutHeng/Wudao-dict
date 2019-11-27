#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os


from src.CommandDraw import CommandDraw
from src.UserHistory import UserHistory
from src.WudaoClient import WudaoClient
from src.tools import is_alphabet
from src.tools import ie


class WudaoCommand:
    def __init__(self):
        # Member
        self.word = ''
        self.param_list = []
        # Init
        self.param_separate()
        self.painter = CommandDraw()
        self.history_manager = UserHistory()
        self.conf = self.history_manager.conf
        # client
        self.client = WudaoClient()

    # init parameters
    def param_separate(self):
        if len(sys.argv) == 1:
            self.param_list.append('h')
        else:
            for v in sys.argv[1:]:
                if v.startswith('-'):
                    self.param_list.append(v)
                else:
                    self.word += ' ' + v
        self.word = self.word.strip()

    # process parameters
    def param_parse(self):
        if len(self.param_list) == 0:
            return
        # help
        if '-h' in self.param_list or '--help' in self.param_list:
            print('Usage: wd [OPTION]... [WORD]')
            print('Youdao is wudao, a powerful dict.')
            
            print('-k, --kill             kill the server process    (退出服务进程)')
            print('-h, --help             display this help and exit (查看帮助)')
            print('-s, --short            do/don\'t show sentences   (简明/完整模式)')
            print('-i, --inter            interaction mode           (交互模式)')
            print('-n, --note             save/not save to notebook  (保存/不保存到生词本)')
            print('生词本文件: ' + os.path.abspath('./usr/') + '/notebook.txt')
            print('查询次数: ' + os.path.abspath('./usr/') + '/usr_word.json')
            #print('-o, --online-search          search word online')
            exit(0)
        # interaction mode
        if '-i' in self.param_list or '--inter' in self.param_list:
            print('进入交互模式。直接键入词汇查询单词的含义。下面提供了一些设置：')
            print(':help                    本帮助')
            print(':note [filename]         设置生词本的名称')
            print(':long                    切换完整模式(:short切换回去)')
            self.interaction()
            sys.exit(0)
        # close server
        if '-k' in self.param_list or '--kill' in self.param_list:
            self.client.close()
            sys.exit(0)
        # conf change
        if '-s' in self.param_list or '--short' in self.param_list:
            self.conf['short'] = not self.conf['short']
            if self.conf['short']:
                print('简明模式已开启！再次键入 wd -s 切换到完整模式')
            else:
                print('完整模式已开启！再次键入 wd -s 切换到简明模式')
        if '-n' in self.param_list or '--note' in self.param_list:
            self.conf['save'] = not self.conf['save']
            if self.conf['save']:
                print('保存到生词本开启。路径：%s' % (self.history_manager.NOTE_NAME))
            else:
                print('保存到生词本关闭。再次键入 wd -n 开启')
        self.history_manager.save_conf(self.conf)
        # word check
        if not self.word:
            print('Usage: wd [OPTION]... [WORD]')
            exit(0)

    # query word
    def query(self, word, notename='notebook'):
        word_info = {}
        is_zh = False
        if word:
            if not is_alphabet(word[0]):
                is_zh = True
        # query on server
        server_context = self.client.get_word_info(word).strip()
        if not is_zh:
            self.history_manager.add_item(word)
        if server_context != 'None':
            word_info = json.loads(server_context)
            if is_zh:
                self.painter.draw_zh_text(word_info, self.conf)
            else:
                self.painter.draw_text(word_info, self.conf)
        else:
            # search in online cache first
            word_info = self.history_manager.get_word_info(word)
            if word_info:
                self.painter.draw_text(word_info, self.conf)
            else:
                if ie():
                    try:
                        # online search
                        from src.WudaoOnline import get_text, get_zh_text
                        from urllib.error import URLError
                        import bs4
                        import lxml
                        if is_zh:
                            word_info = get_zh_text(word)
                        else:
                            word_info = get_text(word)
                        if not word_info['paraphrase']:
                            print('No such word: %s found online' % (self.painter.RED_PATTERN % word))
                            return
                        # store struct
                        self.history_manager.add_word_info(word_info)
                        if not is_zh:
                            self.painter.draw_text(word_info, self.conf)
                        else:
                            self.painter.draw_zh_text(word_info, self.conf)
                    except ImportError:
                        print('Word not found, auto Online search...')
                        print('You need install bs4, lxml first.')
                        print('Use ' + self.painter.RED_PATTERN % 'sudo pip3 install bs4 lxml' + ' or get bs4 online.')
                        return
                    except URLError:
                        print('Word not found, auto Online search...')
                        print('No Internet : connection time out.')
                else:
                    print('Word not found, auto Online search...')
                    print('No Internet : Please check your connection or try again.')
                    return
        if self.conf['save'] and not is_zh:
            self.history_manager.save_note(word_info, notename)
    
    # interaction mode
    def interaction(self):
        self.conf = {'save':True, 'short':True, 'notename':'notebook'}
        while True:
            try:
                inp = input('~ ')
            except EOFError:
                sys.exit(0)
            if inp.startswith(':'):
                if inp == ':quit':
                    print('Bye!')
                    sys.exit(0)
                elif inp == ':short':
                    self.conf['short'] = True
                    print('简明模式（例句将会被忽略）')
                elif inp == ':long':
                    self.conf['short'] = False
                    print('完整模式（例句将会被显示）')
                elif inp == ':help':
                    print(':help                    本帮助')
                    print(':quit                    退出')
                    print(':note [filename]         设置生词本的名称')
                    print(':long                    切换完整模式(:short切换回去)')
                elif inp.startswith(':note'):
                    vec = inp.split()
                    if len(vec) == 2 and vec[1]:
                        self.conf['notename'] = vec[1]
                        print('生词本指定为: ./usr/%s.txt' % (vec[1]))
                    else:
                        print('Bad notebook name!')
                else:
                    print('Bad Command!')
                continue
            if inp.strip():
                self.query(inp.strip(), self.conf['notename'])
def main():
    app = WudaoCommand()
    app.param_parse()
    app.query(app.word)


if __name__ == '__main__':
    main()
