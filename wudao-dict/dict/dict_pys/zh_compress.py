#!/usr/bin/python3

import zlib
import json


def draw_text(word, fw, fi, wid):
    # Word
    word_test = word['word']
    # pronunciation
    phonetic = ""
    if word['pronunciation']:
        phonetic = word['pronunciation']
    
    # paraphrase
    paraphrase = json.dumps(word['paraphrase'])
    # desc
    desc = ''
    if word['desc']:
        while [] in word['desc']:
            word['desc'].remove([])
        desc =json.dumps(word['desc'],ensure_ascii=False)
    # sentence
    sentence = ''
    if word['sentence']:
        sentence =json.dumps(word['sentence'],ensure_ascii=False)
    afline = ("%s|%s|%s|%s|%s|%s" % (word_test, wid, phonetic, paraphrase, desc, sentence))
    acf_line = zlib.compress(afline.encode('utf8'), 6)
    fi.write(word['raw_word'] + '|' + str(fw.tell()) + '\n')
    fw.write(acf_line)
    

if __name__ == "__main__":
    f = open("c.txt", "r")
    fw = open("dict.zlib", "wb+")
    fi = open("dict.zlib.index", "w+")
    li = json.load(f)
    f.close()
    i = 1
    for v in li:
        draw_text(v, fw, fi, i)
        i += 1

