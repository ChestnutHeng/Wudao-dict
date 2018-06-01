# -*- coding: utf-8 -*-
import zlib
import json

class DictReader:
    def __init__(self):
        self.__main_dict = {}
        self.FILE_NAME = './dict/en.z'
        self.INDEX_FILE_NAME = './dict/en.ind'
        self.ZH_FILE_NAME = './dict/zh.z'
        self.ZH_INDEX_FILE_NAME = './dict/zh.ind'
        self.__index_dict = {}
        self.__zh_index_dict = {}
        with open(self.INDEX_FILE_NAME, 'r') as f:
            lines = f.readlines()
            prev_word, prev_no = lines[0].split('|')
            for v in lines[1:]:
                word, no = v.split('|')
                self.__index_dict[prev_word] = (int(prev_no), int(no) - int(prev_no))
                prev_word, prev_no = word, no
            self.__index_dict[word] = (int(no), f.tell() - int(no))
        with open(self.ZH_INDEX_FILE_NAME, 'r') as f:
            lines = f.readlines()
            prev_word, prev_no = lines[0].split('|')
            for v in lines[1:]:
                word, no = v.split('|')
                self.__zh_index_dict[prev_word] = (int(prev_no), int(no) - int(prev_no))
                prev_word, prev_no = word, no
            self.__zh_index_dict[word] = (int(no), f.tell() - int(no))

    # return strings of word info
    def get_word_info(self, query_word):
        with open(self.FILE_NAME, 'rb') as f:
            if query_word in self.__index_dict:
                word_offset = self.__index_dict[query_word]
                f.seek(word_offset[0])
                bytes_obj = f.read(word_offset[1])
                str_obj = zlib.decompress(bytes_obj).decode('utf8')
                list_obj = str_obj.split('|')
                word = {}
                word['word'] = list_obj[0]
                word['id'] = list_obj[1]
                word['pronunciation'] = {}
                if list_obj[2]:
                    word['pronunciation']['美'] = list_obj[2]
                if list_obj[3]:
                    word['pronunciation']['英'] = list_obj[3]
                if list_obj[4]:
                    word['pronunciation'][''] = list_obj[4]
                word['paraphrase'] = json.loads(list_obj[5])
                word['rank'] = list_obj[6]
                word['pattern'] = list_obj[7]
                word['sentence'] = json.loads(list_obj[8])
                return json.dumps(word)
            else:
                return None

    def get_zh_word_info(self, query_word):
        with open(self.ZH_FILE_NAME, 'rb') as f:
            if query_word in self.__zh_index_dict:
                word_offset = self.__zh_index_dict[query_word]
                f.seek(word_offset[0])
                bytes_obj = f.read(word_offset[1])
                str_obj = zlib.decompress(bytes_obj).decode('utf8')
                list_obj = str_obj.split('|')
                word = {}
                word['word'] = list_obj[0]
                word['id'] = list_obj[1]
                word['pronunciation'] = ''
                if list_obj[2]:
                    word['pronunciation'] = list_obj[2]
                word['paraphrase'] = json.loads(list_obj[3])
                word['desc'] = []
                if list_obj[4]:
                    word['desc'] = json.loads(list_obj[4])
                word['sentence'] = []
                if list_obj[5]:
                    word['sentence'] = json.loads(list_obj[5])
                return json.dumps(word)
            else:
                return None

