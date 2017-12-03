import bs4
from soupselect import select as ss
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
import sys
import json


def get_html(x):
    url = urlparse('http://dict.youdao.com/search?q=%s' % urllib.parse.quote(x))
    res = urlopen(url.geturl())
    xml = res.read().decode('utf-8')
    return xml
    

def get_text(word):
    content = get_html(word)
    word_struct = {"word": word}
    root = bs4.BeautifulSoup(content, "lxml")

    pron = ''
    
    # pronunciation
    for item in ss(root, ".phonetic"):
        if item.name.lower() == "span":
            pron = item.text
            break

    word_struct["pronunciation"] = pron
    #
    #  <--  BASIC DESCRIPTION
    #
    nodes = ss(root, "#phrsListTab .trans-container ul p")
    basic_desc = []

    if len(nodes) != 0:
        for li in nodes:
            basic_desc.append(li.text.strip().replace('\n',' '))
    word_struct["paraphrase"] = basic_desc
    
    ## DESC
    desc = []
    for child in ss(root, '#authDictTrans ul li ul li'):
        single = []
        sp = ss(child, 'span')
        if sp:
            span = sp[0].text.strip().replace(':','')
            if span:
                single.append(span)
        ps = []
        for p in ss(child, 'p'):
            ps.append(p.text.strip())
        if ps:
            single.append(ps)
        desc.append(single)
            
            
    word_struct["desc"] = desc
    ##
    
    
    #
    #  -->
    #  <-- VERY COMPLEX
    #
    word_struct["sentence"] = []
    # 21 new year
    for v in root.select("#bilingual ul li"):
        p = ss(v, "p")
        ll = []
        for p in ss(v, "p"):
            if len(p) == 0:
                continue
            if 'class' not in p.attrs:
                ll.append(p.text.strip())
        if len(ll) != 0:
            word_struct["sentence"].append(ll)
    #  -->
    return word_struct

if __name__ == "__main__":
    import time

    f_index = open('chi.txt',"r")
    tot_list = []
    count = 0
    lines = f_index.readlines()

    for l in lines:
        sys.stdout.flush()
        try:
            ll = get_text(l.strip())
        except SyntaxError as err:
        
            time.sleep(0.5)
            print('Getting %d / %d HA_ERR: %s' % (count,len(lines), l.strip()))
            raise err
            #continue
        if not ll["paraphrase"]:
            time.sleep(0.5)
            print('Getting %d / %d STR_ERR: %s' % (count,len(lines), l.strip()))
            
            continue
        print('Getting %d / %d: %s' % (count,len(lines), l.strip()))
        tot_list.append(ll)
        time.sleep(0.5)
        count += 1
        if count % 1000 == 0:
            fw = open('new_data.txt', 'w+')
            json.dump(tot_list, fw)
            fw.close()
    
    fw = open('new_data.txt', 'w+')
    json.dump(tot_list, fw)
    fw.close()
