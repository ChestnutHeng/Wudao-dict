#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys


from src.CommandDraw import CommandDraw
from src.UserHistory import *
from src.WudaoClient import WudaoClient
from src.tools import is_alphabet
from src.tools import ie
from src.UserConfig import UserConfig
from src.WudaoServer import WudaoServer


class WudaoCommand:
    def __init__(self):
        # Member
        self.UserConfig = UserConfig()
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
        # server
        self.server = WudaoServer(1, 'WudaoServer')
        self.server.start()

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
            print('-h, --help             display this help and exit         (查看帮助)')
            print('-S, --short-desc       show sentence or not               (只看释义)')
            print('-s  --save             save currently querying word       (保存当前正在查询的词)')
            print('-a, --auto-save        auto save to notebook or not       (是否自动存入生词本)')
            print('-n  --notebook         show notebook                      (输出生词本内容)')
            print('-d  --delete           delete word from notebook          (从单词本中删除指定单词)')
            print('-w  --word-count       show word count                    (输出查词计数)')
            print('-c  --config           show config                        (查看当前配置)')
            exit(0)

        # switch short desc
        if 'S' in self.param_list or '-short-desc' in self.param_list:
            if self.conf['short']:
                self.conf['short'] = False
                print('简略输出: 关')
            else:
                self.conf['short'] = True
                print('简略输出: 开')
            self.UserConfig.conf_dump(self.conf)
            exit(0)

        # switch auto save
        if 'a' in self.param_list or '-auto-save' in self.param_list:
            if self.conf['save']:
                self.conf['save'] = False
                print('自动保存到生词本: 关')
            else:
                self.conf['save'] = True
                print('自动保存到生词本: 开')
            self.UserConfig.conf_dump(self.conf)
            exit(0)

        # save currently word
        if 's' in self.param_list or '-save' in self.param_list:
            if self.is_zh:
                print('生词本只能保存英文单词')
                exit(2)
            self.query_without_print()
            if not self.conf['save']:  # 若默认自动保存生词，则不必重复保存
                self.history_manager.save_note(self.word_info)
            self.paint()
            print(self.word + ' 已被存入生词本')
            exit(0)

        # print notebook
        if 'n' in self.param_list or '-notebook' in self.param_list:
            try:
                note = self.history_manager.get_note()
            except notebookIsEmpty:
                print('生词本为空！')
                exit(3)
            for i in note:
                self.painter.draw_text(i, self.conf)
            exit(0)

        # delete word from notebook
        if 'd' in self.param_list or '-delete' in self.param_list:
            if self.word == '':
                print('请输入要删除的单词！')
                exit(4)
            self.query_without_print()
            try:
                self.history_manager.del_note(self.word_info)
            except notebookIsEmpty:
                print('生词本为空！')
                exit(3)
            print(self.word, '已从生词本中删除')
            exit(0)

        # print word count
        if 'w' in self.param_list or '-wordcount' in self.param_list:
            word_count = self.history_manager.get_word_count()
            print('您的查词次数为')
            for key, value in word_count.items():
                print(key + '\t' + str(value) + '次')
            exit(0)

        # status
        if 'c' in self.param_list or '-status' in self.param_list:
            self.conf = self.UserConfig.conf_read()
            if self.conf['short']:
                print('简略输出: 开')
            else:
                print('简略输出: 关')
            if self.conf['save']:
                print('自动保存到生词本: 开')
            else:
                print('自动保存到生词本: 关')
            exit(0)

        if not self.word:
            exit(0)

    # query word
    def query_without_print(self):
        self.word_info = {}
        server_contex = self.client.get_word_info(self.word).strip()
        if server_contex != 'None':
            self.word_info = json.loads(server_contex)
        else:
            self.word_info = self.history_manager.get_word_info(self.word)
            if not self.word_info:
                if ie():
                    try:
                        from src.WudaoOnline import get_text, get_zh_text
                        from urllib.error import URLError
                        import bs4
                        import lxml
                        self.word_info = get_text(self.word)
                        if not self.word_info['paraphrase']:
                            print('No such word: %s found online' % (self.painter.RED_PATTERN % self.word))
                            exit(0)
                        self.history_manager.add_word_info(self.word_info)
                    except ImportError:
                        print('Word not found, auto Online search...')
                        print('You need install bs4, lxml first.')
                        print('Use ' + self.painter.RED_PATTERN % 'sudo pip3 install bs4 lxml' + ' or get bs4 online.')
                        exit(0)
                    except URLError:
                        print('Word not found, auto Online search...')
                        print('No Internet : connection time out.')
                else:
                    print('Word not found, auto Online search...')
                    print('No Internet : Please check your connection or try again.')
                    exit(0)

    def paint(self):
        self.query_without_print()
        if self.is_zh:
            self.painter.draw_zh_text(self.word_info, self.conf)
        else:
            self.painter.draw_text(self.word_info, self.conf)
        if self.conf["save"] and not self.is_zh:
            self.history_manager.save_note(self.word_info)
        return

def main():
    app = WudaoCommand()
    app.conf = app.UserConfig.conf_read()
    app.param_parse()
    app.paint()

if __name__ == '__main__':
    main()
