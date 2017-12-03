#coding=utf8
import json
import zlib
import sys

# build
f = open('dict.zlib.index','r')
dic = {}

lines = f.readlines()
prev_word, prev_no = lines[0].split('|')
for v in lines[1:]:
    word, no = v.split('|')
    dic[prev_word] = [int(prev_no), int(no) - int(prev_no)]
    prev_word, prev_no = v.split('|')
    

ww = dic[sys.argv[1]]
# parse
def decompressed(wordQ):
    word_offset = dic[wordQ]
    fr = open('dict.zlib','rb')
    fr.seek(word_offset[0])
    bytes_obj = fr.read(word_offset[1])
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
    print(word['desc'])
    word['sentence'] = []
    if list_obj[5]:
        word['sentence'] = json.loads(list_obj[5])
    return word    

res = decompressed(sys.argv[1])
#print(res)
from wd import draw_zh_text
draw_zh_text(res, True)
#a = json.loads(a_str)
#print(json.dumps(res, indent=4,ensure_ascii=False))
