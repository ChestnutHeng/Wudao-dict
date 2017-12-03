#!/usr/bin/python3

import zlib
import json


def draw_text(word, fw, fi, wid):
    # Word
    word_test = word['word']
    # pronunciation
    UK_phonetic = ""
    US_phonetic = ""
    unkown_phonetic = ""
    if word['pronunciation']:
        if '英' in word['pronunciation']:
            UK_phonetic = word['pronunciation']['英']
        if '美' in word['pronunciation']:
            US_phonetic = word['pronunciation']['美']
        if '' in word['pronunciation']:
            unkown_phonetic = word['pronunciation']['']
    
    # paraphrase
    paraphrase =json.dumps(word['paraphrase'],ensure_ascii=False)
    # short desc
    rank = ""
    pattern = ""
    if word['rank']:
        rank = word['rank']
    if word['pattern']:
        pattern =  word['pattern']
    sentence =json.dumps(word['sentence'],ensure_ascii=False)
    afline = ("%s|%s|%s|%s|%s|%s|%s|%s|%s" % (word_test, wid, US_phonetic, UK_phonetic, unkown_phonetic, paraphrase, rank, pattern, sentence))
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

