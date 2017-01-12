#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd

def remove_duplic(seq, idfun=None):
   if idfun is None:
       def idfun(x):
           return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen:
           continue
       seen[marker] = 1
       result.append(item)
   return result

def fix_rank(path):
    for f in os.listdir(path):
        with open(path + f, 'r') as fr:
            os.remove(path + f) if os.path.exists(path + f) else None
            with open(path + f, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                for line in fr:
                    temp_arr = line.rstrip('\n').split(',')
                    writer.writerow(remove_duplic(temp_arr))

if __name__ == '__main__':
    rank_path = 'course/908/slide_done/1/page_to_rank/'
    fix_rank(rank_path)
