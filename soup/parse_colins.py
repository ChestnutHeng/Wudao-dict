import bs4
from soupselect import select as ss
import json
import sys

from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
    
def get_html(x):
    url = urlparse('http://dict.youdao.com/search?q=%s' % x)
    res = urlopen(url.geturl())
    xml = res.read().decode('utf-8')
    return xml

def multi_space_to_single(text):
    cursor = 0
    result = ""
    while cursor < len(text):
        if text[cursor] in ["\t", " ", "\n", "\r"]:
            while text[cursor] in ["\t", " ", "\n", "\r"]:
                cursor += 1
            result += " "
        else:
            result += text[cursor]
            cursor += 1
    return result



def get_text(word):
    content = get_html(word)
    word_struct = {"word":word}
    root = bs4.BeautifulSoup(content, "lxml")

    pron = {}

    for pron_item in ss(root, ".pronounce"):
        pron_lang = None
        pron_phonetic = None
        
        for sub_item in pron_item.children:
            if isinstance(sub_item, str) and pron_lang is None:
                pron_lang = sub_item
                continue
            if isinstance(sub_item, bs4.Tag) and sub_item.name.lower() == "span" and sub_item.has_attr("class") and "phonetic" in sub_item.get("class"):
                pron_phonetic = sub_item
                continue
        if pron_phonetic is None:
            raise SyntaxError("WHAT THE FUCK?")
        if pron_lang is None:
            pron_lang = ""
        pron_lang = pron_lang.strip()
        pron_phonetic = pron_phonetic.text
        
        pron[pron_lang] = pron_phonetic
        
    word_struct["pronunciation"] = pron
        
    #
    #  <--  BASIC DESCRIPTION
    #     
    nodes = ss(root, "#phrsListTab .trans-container ul")
    basic_desc = []

    if len(nodes) != 0:
        ul = nodes[0]
        for li in ul.children:
            if not (isinstance(li, bs4.Tag) and li.name.lower() == "li"):
                continue
            basic_desc.append(li.text.strip())
    word_struct["paraphrase"] = basic_desc
    #
    #  -->
    #

    #
    #  <--  RANK
    #

    rank = ""

    nodes = ss(root, ".rank")
    if len(nodes) != 0:
        rank = nodes[0].text.strip()
    word_struct["rank"] = rank
    #
    #  -->
    #

    #
    #  <-- PATTERN
    #
    #.collinsToggle .pattern

    pattern = ""

    nodes = ss(root, ".collinsToggle .pattern")
    if len(nodes) != 0:
    #    pattern = nodes[0].text.strip().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        pattern = multi_space_to_single(nodes[0].text.strip())
    word_struct["pattern"] = pattern

    #
    #  -->
    #


    #
    #  <-- VERY COMPLEX
    #
    word_struct["sentence"] = []
    for child in ss(root, ".collinsToggle .ol li"):
        p = ss(child, "p")
        if len(p) == 0:
            continue
        p = p[0]
        desc = ""
        cx = ""
        for node in p.children:
            if isinstance(node, str):
                desc += node
            if isinstance(node, bs4.Tag) and node.name.lower() == "span":
                cx = node.text
        desc = multi_space_to_single(desc.strip())
        
        examples = []

        for el in ss(child, ".exampleLists"):
            examp = []
            for p in ss(el, ".examples p"):
                examp.append(p.text.strip())
            examples.append(examp)
        word_struct["sentence"].append([desc, cx, examples])
    #
    #
    #  -->
    return word_struct
   
if __name__ == "__main__":
    import time

    f_index = open('ph_list.txt',"r")
    tot_list = []
    count = 0
    lines = f_index.readlines()

    for l in lines:
        count += 1
        sys.stdout.flush()
        try:
            ll = get_text(l.strip())
        except SyntaxError:
            time.sleep(0.5)
            print('Getting %d / %d HA_ERR: %s' % (count,len(lines), l.strip()))
            continue
        if not ll["paraphrase"]:
            time.sleep(0.5)
            print('Getting %d / %d STR_ERR: %s' % (count,len(lines), l.strip()))
            continue
        print('Getting %d / %d: %s' % (count,len(lines), l.strip()))
        tot_list.append(ll)
        time.sleep(0.5)
        if count % 100 == 0:
            fw = open('new_data.txt', 'w+')
            json.dump(tot_list, fw)
            fw.close()
    
    fw = open('new_data.txt', 'w+')
    json.dump(tot_list, fw)
    fw.close()
