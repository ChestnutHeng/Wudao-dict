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
        self.conf = {"short": False, "save": False}
        self.is_zh = False
        # Init
        self.param_separate()
        self.painter = CommandDraw()
        self.history_manager = UserHistory()
        # client
        self.client = WudaoClient()

    # init parameters
    def param_separate(self):
        if len(sys.argv) == 1:
            self.param_list.append('h')
        else:
            for v in sys.argv[1:]:
                if v.startswith('-'):
                    self.param_list.append(v[1:])
                else:
                    self.word += ' ' + v
        self.word = self.word.strip()
        if self.word:
            if not is_alphabet(self.word[0]):
                self.is_zh = True

    # process parameters
    def param_parse(self):
        if len(self.param_list) == 0:
            return
        if 'h' in self.param_list or '-help' in self.param_list:
            print('Usage: wd [OPTION]... [WORD]')
            print('Youdao is wudao, a powerful dict.')
            
            print('-k, --kill             kill the server process    (退出服务进程)')
            print('-h, --help             display this help and exit (查看帮助)')
            print('-s, --short-desc       do not show sentence       (只看释义)')
            print('-n, --not-save         query and save to notebook (不存入生词本)')
            print('生词本文件: ' + os.path.abspath('./usr/') + '/notebook.txt')
            print('查询次数: ' + os.path.abspath('./usr/') + '/usr_word.json')
            #print('-o, --online-search          search word online')
            exit(0)
        # close server
        if 'k' in self.param_list or '-kill' in self.param_list:
            self.client.close()
            sys.exit(0)
        # short conf
        if 's' in self.param_list or '-short-desc' in self.param_list:
            self.conf['short'] = True
        if 'n' in self.param_list or '-not-save' in self.param_list:
            self.conf['save'] = True
        if not self.word:
            print('Usage: wd [OPTION]... [WORD]')
            exit(0)

    # query word
    def query(self):
        word_info = {}
        # query on server
        server_context = self.client.get_word_info(self.word).strip()
        if not self.is_zh:
            self.history_manager.add_item(self.word)
        if server_context != 'None':
            word_info = json.loads(server_context)
            if self.is_zh:
                self.painter.draw_zh_text(word_info, self.conf)
            else:
                
                self.painter.draw_text(word_info, self.conf)
        else:
            # search in online cache first
            word_info = self.history_manager.get_word_info(self.word)
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
                        if self.is_zh:
                            word_info = get_zh_text(self.word)
                        else:
                            word_info = get_text(self.word)
                        if not word_info['paraphrase']:
                            print('No such word: %s found online' % self.word)
                            exit(0)
                        # store struct
                        self.history_manager.add_word_info(word_info)
                        if not self.is_zh:
                            self.painter.draw_text(word_info, self.conf)
                        else:
                            self.painter.draw_zh_text(word_info, self.conf)
                    except ImportError:
                        print('Word not found, auto Online search...')
                        print('You need install bs4, lxml first.')
                        print('Use \'sudo pip3 install bs4 lxml\' or get bs4 online.')
                else:
                    print('Word not found, auto Online search...')
                    print('No Internet : Please check your connection')
        if not self.conf['save'] and not self.is_zh:
            self.history_manager.save_note(word_info)

def main():
    app = WudaoCommand()
    app.param_parse()
    app.query()


if __name__ == '__main__':
    main()
