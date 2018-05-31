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

    # dump config as json file
    def conf_dump(self):
        with open("./usr/conf.json", "w+") as file:
            file.write(json.dumps(self.conf, sort_keys=True, indent=4, separators=(',', ': ')))

    # read config from json file
    def conf_read(self):
        try:
            with open("./usr/conf.json", "r") as file:
                self.conf=json.loads(file.read())
        except IOError as e:
            self.conf_dump()
        except json.JSONDecodeError as e:
            self.conf_dump()

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
            print('-k, --kill             kill the server process            (退出服务进程)')
            print('-h, --help             display this help and exit         (查看帮助)')
            print('-S, --short-desc       show sentence or not               (只看释义)')
            print('-s  --save             save currently querying word       (保存当前正在查询的词)')
            print('-a, --auto-save        auto save to notebook or not       (是否自动存入生词本)')
            print('-c  --config           show config                        (查看当前配置)')
            print('生词本文件: ' + os.path.abspath('./usr/') + '/notebook.txt')
            print('查询次数: ' + os.path.abspath('./usr/') + '/usr_word.json')
            exit(0)

        # close server
        if 'k' in self.param_list or '-kill' in self.param_list:
            self.client.close()
            sys.exit(0)

        # switch short desc
        if 'S' in self.param_list or '-short-desc' in self.param_list:
            if self.conf['short']:
                self.conf['short'] = False
                print('short desc: off')
                print('简略输出: 关')
            else:
                self.conf['short'] = True
                print('short desc: on')
                print('简略输出: 开')
            self.conf_dump()

        # switch auto save
        if 'a' in self.param_list or '-auto-save' in self.param_list:
            if self.conf['save']:
                self.conf['save'] = False
                print('auto save to notebook: off')
                print('自动保存到生词本: 关')
            else:
                self.conf['save'] = True
                print('auto save to notebook: on')
                print('自动保存到生词本: 开')
            self.conf_dump()

        # save currently word
        if 's' in self.param_list or '-save' in self.param_list:
            self.tmp = self.conf['save']
            self.conf['save'] = True
            self.query()
            self.conf['save'] = self.tmp
            print(self.word + ' 已被存入生词本')
            exit(0)


        # status
        if 'c' in self.param_list or '-status' in self.param_list:
            if self.conf['short']:
                print('short desc: on')
                print('简略输出: 开')
            else:
                print('short desc: off')
                print('简略输出: 关')
            print('')
            if self.conf['save']:
                print('auto save to notebook: on')
                print('自动保存到生词本: 开')
            else:
                print('auto save to notebook: off')
                print('自动保存到生词本: 关')
            print('')

        if not self.word:
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
                            print('No such word: %s found online' % (self.painter.RED_PATTERN % self.word))
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
                        print('Use ' + self.painter.RED_PATTERN % 'sudo pip3 install bs4 lxml' + ' or get bs4 online.')
                        exit(0)
                    except URLError:
                        print('Word not found, auto Online search...')
                        print('No Internet : connection time out.')
                else:
                    print('Word not found, auto Online search...')
                    print('No Internet : Please check your connection or try again.')
                    exit(0)
        if self.conf['save'] and not self.is_zh:
            self.history_manager.save_note(word_info)
        return

def main():
    app = WudaoCommand()
    app.conf_read()
    app.param_parse()
    app.query()


if __name__ == '__main__':
    main()
