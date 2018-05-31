# -*- coding: utf-8 -*-

import json
import os


class UserHistory:
    MAX_LATEST_LEN = 20
    MAX_CACHE_LEN = 10000
    MAX_COUNT_LEN = 500000
    content = {}
    latest_word = []
    DICT_FILE = './usr/usr_word.json'
    LATEST_FILE = './usr/latest.txt'
    ONLINE_CACHE = './usr/online_cache.json'
    NOTE_FILE = './usr/notebook.txt'

    def __init__(self):
        # Create empty file
        if not os.path.exists(self.DICT_FILE):
            with open(self.DICT_FILE, 'w+') as file:
                tmp_dict = {}
                json.dump(tmp_dict, file)
        if not os.path.exists(self.LATEST_FILE):
            open(self.LATEST_FILE, 'w+').close()
        if not os.path.exists(self.ONLINE_CACHE):
            with open(self.ONLINE_CACHE, 'w+') as file:
                json.dump({}, file)
        with open(self.ONLINE_CACHE, 'r') as file:
            self.cache_dic = json.load(file)
        with open(self.DICT_FILE, 'r') as file:
            self.word_co_map = json.load(file)

    def add_item(self, word):
        # Update word dict
        if word in self.word_co_map:
            self.word_co_map[word] += 1
        else:
            self.word_co_map[word] = 1
        # Update latest word list
        with open(self.LATEST_FILE, 'r') as file:
            self.latest_word = [v.strip() for v in file.readlines()]
            if len(self.latest_word) < self.MAX_LATEST_LEN:
                self.latest_word.append(word)
            else:
                self.latest_word.pop(0)
                self.latest_word.append(word)
        with open(self.LATEST_FILE, 'w') as file:
            for v in self.latest_word:
                file.write(v + '\n')
        with open(self.DICT_FILE, 'w') as file:
            # too much usr word
            if len(self.word_co_map) <= self.MAX_COUNT_LEN:
                json.dump(self.word_co_map, file, indent=4)

    # add word info to online cache
    def add_word_info(self, word_info):
        # too much usr word
        if len(self.cache_dic) > self.MAX_CACHE_LEN:
            # remove
            self.cache_dic = {}
            os.remove(self.ONLINE_CACHE)
        with open(self.ONLINE_CACHE, 'w') as file:
            self.cache_dic[word_info['word'].lower()] = word_info
            json.dump(self.cache_dic, file)

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
            with open(self.NOTE_FILE, 'a+') as file:
                ph = ' '.join(word_struct['paraphrase']).replace('\n', ' ')
                spaces = ' '*(20 - len(word_struct['word']))
                file.write(word_struct['word'] + spaces + ' ' + ph + '\n')

