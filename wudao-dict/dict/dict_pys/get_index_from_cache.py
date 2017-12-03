import os
import sys
import json

mp = []
f = open(sys.argv[1], 'r')
lis = [x.strip() for x in f.readlines()]
f.close()

###
for fname in os.listdir('../dcache/'):
    if ' ' in fname:
        lis.append(fname)
###

for v in lis:
    if not os.path.exists('../dcache/' + v):
        if not os.path.exists('../bad_cache/' + v):
            print(v)
        continue
    try:
        f = open('../dcache/' + v ,'r')
        a = json.load(f)
        f.close()
        mp.append(a)
    except BaseException as e:
        print(e, v)

f = open('c.txt', 'w')
json.dump(mp,f)
f.close()
