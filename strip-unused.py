#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import shutil

with open(sys.argv[1], "rb") as f:
    data = f.read()

lines = []
for line in data.split("\n"):
    for tag in ["UNUSED", "UNUSED_FUNCTION"]:
        #search_from = 0
        #altered = 1
        #while altered:
        #    altered = 0
        pos = -1
        while True:
        #while pos >= 0:
            tagp = tag + "("
            #pos = line.find(tag, search_from)
            pos = line.find(tagp, pos + 1)
            if pos < 0:
                break
            #search_from = pos + 1
            #altered = 1
            # avoid "fixing" other defined ending with UNUSED
            if line[pos-1] not in ", *":
                print("ignoring", repr(line[pos-1]))
                continue
            remain = line[pos+len(tagp):]
            line = line[:pos]
            level = 1
            for c in remain:
                #if c == "(" and level:
                #    level += 1
                #elif c == ")" and level:
                #    level -= 1
                #elif level == 0:
                if c == ")" and level:
                    level -= 1
                    continue
                line += c
        #assert tagp not in line
    #assert "UNUSED(" not in line
    lines.append(line)

data = "\n".join(lines)
with open(sys.argv[1], "wb") as f:
    f.write(data)
