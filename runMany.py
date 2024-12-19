from pwn import *

import sys 
a = []
for i in range(int(sys.argv[1])):
    p = process(["python3","analytics.py",f"many{i}.json"])
    a.append(p)

for i in a:
    i.recvline()
