# -*- coding: utf-8 -*-

import json
import os


class UserHistory:
    MAX_LATEST_LEN = 20
    MAX_CACHE_LEN = 10000
    MAX_COUNT_LEN = 500000
    content = {}
    latest_word = []
    DICT_FILE_NAME = './usr/usr_word.json'
    LATEST_FILE_NAME = './usr/latest.txt'
    ONLINE_CACHE = './usr/online_cache.json'
    NOTE_NAME = './usr/notebook.txt'

    def __init__(self):
        # Create empty file
        if not os.path.exists(self.DICT_FILE_NAME):
            with open(self.DICT_FILE_NAME, 'w+') as f:
                tmp_dict = {}
                json.dump(tmp_dict, f)
        if not os.path.exists(self.LATEST_FILE_NAME):
            open(self.LATEST_FILE_NAME, 'w+').close()
        if not os.path.exists(self.ONLINE_CACHE):
            with open(self.ONLINE_CACHE, 'w+') as f:
                json.dump({}, f)
        with open(self.ONLINE_CACHE, 'r') as f:
            self.cache_dic = json.load(f)
        with open(self.DICT_FILE_NAME, 'r') as f:
            self.word_co_map = json.load(f)
    def add_item(self, word):
        # Update word dict
        if word in self.word_co_map:
            self.word_co_map[word] += 1
        else:
            self.word_co_map[word] = 1
        # Update latest word list
        with open(self.LATEST_FILE_NAME, 'r') as f:
            self.latest_word = [v.strip() for v in f.readlines()]
            if len(self.latest_word) < self.MAX_LATEST_LEN:
                self.latest_word.append(word)
            else:
                self.latest_word.pop(0)
                self.latest_word.append(word)
        with open(self.LATEST_FILE_NAME, 'w') as f:
            for v in self.latest_word:
                f.write(v + '\n')
        with open(self.DICT_FILE_NAME, 'w') as f:
            # too much usr word
            if len(self.word_co_map) <= self.MAX_COUNT_LEN:
                json.dump(self.word_co_map, f, indent=4)

    # add word info to online cache
    def add_word_info(self, word_info):
        # too much usr word
        if len(self.cache_dic) > self.MAX_CACHE_LEN:
            # remove
            self.cache_dic = {}
            os.remove(self.ONLINE_CACHE)
        with open(self.ONLINE_CACHE, 'w') as f:
            self.cache_dic[word_info['word'].lower()] = word_info
            json.dump(self.cache_dic, f)

    # get word info from online cache
    def get_word_info(self, word):
        if word.lower() in self.cache_dic:
            return self.cache_dic[word.lower()]
        else:
            return None

    def save_note(self, word_struct):
        if False:#word_struct['word'] in self.word_co_map:
            return
        else:
            with open(self.NOTE_NAME, 'a+') as f:
                ph = ' '.join(word_struct['paraphrase']).replace('\n', ' ')
                spaces = ' '*(20 - len(word_struct['word']))
                f.write(word_struct['word'] + spaces + ' ' + ph + '\n')

